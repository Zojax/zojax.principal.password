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
from zope import interface
from zope.component import getUtility
from interfaces import IPasswordTool, IPasswordChanger, IPasswordPreference


class PasswordPreference(object):
    interface.implements(IPasswordPreference)

    def __bind__(self, principal=None, parent=None):
        clone = super(PasswordPreference, self).__bind__(principal, parent)
        clone.changer = IPasswordChanger(clone.__principal__, None)
        return clone

    def checkPassword(self, password):
        return self.changer.checkPassword(password)

    def changePassword(self, password):
        passwordTool = getUtility(IPasswordTool)
        self.changer.changePassword(passwordTool.encodePassword(password))

    def isAvailable(self):
        if self.changer is None:
            return False
        else:
            return super(PasswordPreference, self).isAvailable()
