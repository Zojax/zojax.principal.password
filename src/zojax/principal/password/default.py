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
from zope.schema import ValidationError
from zope.component import getUtility

from interfaces import _, PasswordError
from interfaces import IPasswordChecker, IDefaultPasswordCheckerConfiglet


class LengthPasswordError(PasswordError):
    __doc__ = _('Password min length exceeded.')

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return str(self.message)

    def doc(self):
        return self.message


class LettersDigitsPasswordError(PasswordError):
    __doc__ = _('Password should contain both letters and digits.')


class LettersCasePasswordError(PasswordError):
    __doc__ = _('Password should contain letters in mixed case.')


class DefaultPasswordChecker(object):
    """
    >>> import zope.interface.verify
    >>> from zope import interface, component
    >>> from zojax.principal.password import interfaces, default

    >>> zope.interface.verify.verifyClass(
    ...     interfaces.IPasswordChecker, default.DefaultPasswordChecker)
    True

    Default password checker uses IDefaultPasswordCheckerConfiglet utility
    to get configuration. We use controlpanel configlet for this but
    in this code we should create it.

    >>> class Configlet(object):
    ...     interface.implements(interfaces.IDefaultPasswordCheckerConfiglet)
    ...     min_length = 5
    ...     letters_digits = False
    ...     letters_mixed_case = False

    >>> configlet = Configlet()
    >>> component.provideUtility(configlet)

    >>> checker = default.DefaultPasswordChecker()
    >>> zope.interface.verify.verifyObject(interfaces.IPasswordChecker, checker)
    True

    >>> checker.validate('passw')

    >>> checker.validate('ps1')
    Traceback (most recent call last):
    ...
    LengthPasswordError: ...

    >>> configlet.min_length = 6
    >>> checker.validate('passw')
    Traceback (most recent call last):
    ...
    LengthPasswordError: ...

    >>> checker.validate('password')

    >>> configlet.letters_digits = True

    >>> checker.validate('password')
    Traceback (most recent call last):
    ...
    LettersDigitsPasswordError

    >>> checker.validate('66665555')
    Traceback (most recent call last):
    ...
    LettersDigitsPasswordError

    >>> checker.validate('pass5word')

    >>> configlet.letters_mixed_case = True
    >>> checker.validate('pass5word')
    Traceback (most recent call last):
    ...
    LettersCasePasswordError

    >>> checker.validate('PASS5WORD')
    Traceback (most recent call last):
    ...
    LettersCasePasswordError

    >>> checker.validate('Pass5word')

    By default password strength is always 100%

    >>> checker.passwordStrength('Pass5word')
    100.0

    """
    interface.implements(IPasswordChecker)

    title = _(u'Default password checker')

    def validate(self, password):
        config = getUtility(IDefaultPasswordCheckerConfiglet)

        if len(password) < config.min_length:
            raise LengthPasswordError(
                _('Password should be at least ${count} characters.',
                  mapping={'count': config.min_length}))
        elif config.letters_digits and \
                 (password.isalpha() or password.isdigit()):
            raise LettersDigitsPasswordError()
        elif config.letters_mixed_case and \
                 (password.isupper() or password.islower()):
            raise LettersCasePasswordError()

    def passwordStrength(self, password):
        return 100.0


def isAvailable(prefs):
    return prefs.__name__ == prefs.__parent__.passwordChecker
