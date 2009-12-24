##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from BTrees.OOBTree import OOBTree

from zope import interface
from zope.component import getUtility, queryUtility
from zope.app.authentication.interfaces import IPasswordManager

from zojax.authentication.utils import getPrincipal

from utils import genPassword2

from interfaces import IPasswordChanger
from interfaces import IPasswordTool, IPasswordChecker
from interfaces import InvalidPascode, PasswordResetingError


class PasswordTool(object):
    interface.implements(IPasswordTool)

    def checkPassword(self, encodedPassword, password):
        pm = getUtility(IPasswordManager, self.passwordManager)
        return pm.checkPassword(encodedPassword, password)

    def encodePassword(self, password, *args, **kw):
        pm = getUtility(IPasswordManager, self.passwordManager)
        return pm.encodePassword(password, *args, **kw)

    def validatePassword(self, password):
        checker = queryUtility(IPasswordChecker, self.passwordChecker)
        if checker is not None:
            checker.validate(password)

    def passwordStrength(self, password):
        checker = queryUtility(IPasswordChecker, self.passwordChecker)
        if checker is not None:
            return checker.passwordStrength(password)
        return 100.0

    def _get_mappers(self):
        # get pid->passcode mapper
        pid_passcode = self.data.get('pid_passcode')
        if pid_passcode is None:
            pid_passcode = OOBTree()
            self.data['pid_passcode'] = pid_passcode

        # get passcode->pid mapper
        passcode_pid = self.data.get('passcode_pid')
        if passcode_pid is None:
            passcode_pid = OOBTree()
            self.data['passcode_pid'] = passcode_pid

        return pid_passcode, passcode_pid

    def getPasscode(self, pid):
        pid_passcode, passcode_pid = self._get_mappers()
        return pid_passcode.get(pid)

    def getPrincipal(self, passcode):
        pid_passcode, passcode_pid = self._get_mappers()
        return getPrincipal(passcode_pid.get(passcode, ''))

    def generatePasscode(self, principal):
        if isinstance(principal, basestring):
            principal = getPrincipal(principal)

        changer = IPasswordChanger(principal, None)
        if changer is None:
            raise PasswordResetingError(
                "IPasswordChanger adapter is not available.")

        principalId = principal.id

        pid_passcode, passcode_pid = self._get_mappers()

        # remove old mapping
        if principalId in pid_passcode:
            if pid_passcode[principalId] in passcode_pid:
                del passcode_pid[pid_passcode[principalId]]
            del pid_passcode[principalId]

        passcode = genPassword2(32)
        pid_passcode[principalId] = passcode
        passcode_pid[passcode] = principalId
        return passcode

    def resetPassword(self, passcode, password):
        pid_passcode, passcode_pid = self._get_mappers()

        pid = passcode_pid.get(passcode)
        principal = getPrincipal(pid)

        if principal is None:
            raise InvalidPascode()

        IPasswordChanger(principal).changePassword(self.encodePassword(password))

        # remove old mapping
        del passcode_pid[pid_passcode[pid]]
        del pid_passcode[pid]
