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
""" change password form

$Id$
"""
from zope import interface
from zope.cachedescriptors.property import Lazy

from zojax.authentication.utils import updateCredentials
from zojax.authentication.interfaces import IPrincipalLogin

from zojax.layoutform import button, Fields, PageletEditForm
from zojax.statusmessage.interfaces import IStatusMessage

from zojax.principal.password.interfaces import _
from interfaces import IPrincipalPasswordForm, IPersonalPasswordForm


class PrincipalPassword(PageletEditForm):
    """ change password form """
    interface.implements(IPrincipalPasswordForm, IPersonalPasswordForm)

    ignoreContext = True

    label = _('Change password')

    def update(self, *args, **kw):
        principal = self.context.__principal__

        login = IPrincipalLogin(principal, None)
        if login is not None:
            login = login.login

        self.principal_login = login
        self.principal_title = principal.title

        self.isManagement = self.request.principal.id != principal.id
        return super(PrincipalPassword, self).update()

    @Lazy
    def fields(self):
        if self.isManagement:
            # if in management panel we don't need check current password
            return Fields(IPrincipalPasswordForm)
        else:
            return Fields(IPersonalPasswordForm, IPrincipalPasswordForm)

    @button.buttonAndHandler(_(u"Change password"))
    def applyChanges(self, action):
        service = IStatusMessage(self.request)

        data, errors = self.extractData()

        if errors:
            service.add(self.formErrorsMessage, 'error')
        elif data['password']:
            self.context.changePassword(data['password'])
            service.add(_('Password has been changed for ${title}.',
                          mapping = {'title': self.principal_title}))

            if not self.isManagement:
                if not updateCredentials(
                    self.request, self.principal_login, data['password']):
                    service.add(
                        _("Sorry, system can't update your creadential data. "\
                          "You should logout and login with new password."))
