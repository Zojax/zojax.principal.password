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
from zope import schema, interface
from zope.exceptions import UserError
from zope.schema.interfaces import IPassword
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zojax.principal.password')


class PasswordResetingError(UserError):
    """ Can't reset password """


class InvalidPascode(UserError):
    """ Passcode is Invalide """


class PasswordError(schema.ValidationError):
    """ password validation error """


class IPassword(IPassword):
    """ password field """


class IPasswordTool(interface.Interface):
    """ password tool """

    passwordManager = schema.Choice(
        title = _(u'Password manager'),
        vocabulary = u'Password Manager Names',
        required = True,
        default = u'MD5')

    passwordChecker = schema.Choice(
        title = _('Password checker'),
        vocabulary = u'zojax.principal.password-checkers',
        required = True,
        default = u'default')

    def encodePassword(password, *args, **kw):
        """ encode password """

    def checkPassword(encodedPassword, password):
        """ check password """

    def validatePassword(password):
        """ validate password """

    def passwordStrength(password):
        """ check password strength """

    def getPasscode(pid):
        """ return passcode by principal """

    def getPrincipal(passcode):
        """ return principal by passcode """

    def generatePasscode(principal):
        """ generate passcode for principal """

    def resetPassword(passcode, password):
        """ reset password """


class IPasswordChecker(interface.Interface):
    """ password checker """

    title = schema.TextLine(
        title = u'Title',
        required = True)

    def validate(password):
        """ validate password """

    def passwordStrength(password):
        """ return password strength (float)"""


class IDefaultPasswordCheckerConfiglet(interface.Interface):
    """ default password checker """

    min_length = schema.Int(
        title = _(u'Minimum length'),
        description = _(u'Minimun length of password.'),
        default = 5,
        required = True)

    letters_digits = schema.Bool(
        title = _(u'Letters and digits'),
        description = _(u'Password should contain both letters and digits.'),
        default = False,
        required = True)

    letters_mixed_case = schema.Bool(
        title = _(u'Letters case'),
        description = _(u'Password should contain letters in mixed case.'),
        default = False,
        required = True)


class IPasswordResetingEvent(interface.Interface):

    principal = interface.Attribute('Principal')

    passcode = interface.Attribute('Passcode')


class PasswordResetingEvent(object):
    interface.implements(IPasswordResetingEvent)

    def __init__(self, principal, passcode):
        self.principal = principal
        self.passcode = passcode


class IPasswordPreference(interface.Interface):
    """ password preference """

    def checkPassword(password):
        """ check password """

    def changePassword(password):
        """ set new password """


# principal password changer
class IPasswordChanger(interface.Interface):
    """ password changer for principal """

    def __init__(principal):
        """ adapter constructor """

    def checkPassword(password):
        """ check current password """

    def changePassword(password):
        """ change password """
