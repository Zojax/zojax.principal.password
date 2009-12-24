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
from zope import interface, schema
from zojax.principal.password.interfaces import _
from zojax.principal.password.field import Password


class CurrentPassword(schema.Password):
    """ field for checking current password """


class PasswordFormError(schema.ValidationError):
    __doc__ = _("Password and Confirm Password should be the same.")


class CurrentPasswordError(schema.ValidationError):
    __doc__ = _(u'Does not match current password.')


class IPersonalPasswordForm(interface.Interface):

    principal_login = interface.Attribute('Principal login')

    current_password = CurrentPassword(
        title = _(u'Current password'),
        description = _(u'Enter your current password.'),
        missing_value = u'',
        required = True)


class IPrincipalPasswordForm(interface.Interface):
    """ password form """

    password = Password(
        title = _(u'New password'),
        description = _(u'Enter new password. '\
                        u'No spaces or special characters, should contain '\
                        u'digits and letters in mixed case.'),
        default = u'',
        required = True)

    confirm_password = Password(
        title = _(u'Confirm password'),
        description = _(u'Re-enter the password. '
                        u'Make sure the passwords are identical.'),
        missing_value = u'',
        required = True)
