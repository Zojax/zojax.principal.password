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
from zope import interface, component, schema
from zope.component import getUtility
from zope.app.security.interfaces import IAuthentication

from z3c.form import interfaces, validator

from zojax.principal.password.interfaces import _

from interfaces import CurrentPassword
from interfaces import PasswordFormError, CurrentPasswordError
from interfaces import IPrincipalPasswordForm, IPersonalPasswordForm


class PasswordFormValidator(validator.InvariantsValidator):
    component.adapts(
        interface.Interface,
        interface.Interface,
        IPrincipalPasswordForm,
        interface.interfaces.IInterface,
        interface.Interface)

    def validate(self, data):
        if self.schema != IPrincipalPasswordForm:
            return super(PasswordFormValidator, self).validate(data)

        password = self.view.widgets['password']
        cpassword = self.view.widgets['confirm_password']

        errors = []

        if password.error is None and cpassword.error is None:
            if data['password'] != data['confirm_password']:
                error = PasswordFormError()
                errors.append(error)

                view = component.getMultiAdapter(
                    (error, self.request, password, password.field,
                     self.view, self.context), interfaces.IErrorViewSnippet)
                view.update()
                password.error = view

                view = component.getMultiAdapter(
                    (error, self.request, cpassword, cpassword.field,
                     self.view, self.context), interfaces.IErrorViewSnippet)
                view.update()
                cpassword.error = view

        return tuple(errors) + super(PasswordFormValidator, self).validate(data)


class CurrentPasswordValidator(validator.SimpleFieldValidator):
    component.adapts(
        interface.Interface,
        interface.Interface,
        IPersonalPasswordForm,
        CurrentPassword,
        interface.Interface)

    def validate(self, value):
        super(CurrentPasswordValidator, self).validate(value)

        # check current password
        if self.context.checkPassword(value):
            return

        raise CurrentPasswordError()
