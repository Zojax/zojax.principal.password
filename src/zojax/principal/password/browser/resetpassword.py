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
from zope import interface, schema, event
from zope.component import getUtility, queryMultiAdapter
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL
from zope.app.pagetemplate import ViewPageTemplateFile

from zojax.mail.interfaces import IMailer
from zojax.authentication.utils import updateCredentials
from zojax.authentication.utils import getPrincipalByLogin
from zojax.authentication.interfaces import IPrincipalLogin

from zojax.layoutform import button, Fields, PageletForm
from zojax.statusmessage.interfaces import IStatusMessage

from zojax.principal.password.interfaces import _, PasswordResetingEvent
from zojax.principal.password.interfaces import IPasswordTool, PasswordResetingError

from interfaces import IPrincipalPasswordForm


class ResetPassword(PageletForm):
    interface.implements(IPrincipalPasswordForm)

    passcode = None
    principal = None

    ignoreContext = True

    fields = Fields(IPrincipalPasswordForm)

    confirm = ViewPageTemplateFile('resetpasswordconfirm.pt')
    resetform = ViewPageTemplateFile('resetpassword.pt')

    def __init__(self, context, request):
        super(ResetPassword, self).__init__(context, request)
        self.passwordtool = getUtility(IPasswordTool)

    def publishTraverse(self, request, name):
        view = queryMultiAdapter((self, request), name=name)
        if view is not None:
            return view

        principal = self.passwordtool.getPrincipal(name)
        if principal is not None:
            self.passcode = name
            self.principal = principal
            return self
        else:
            IStatusMessage(request).add(_("Passcode is invalid."), 'warning')

        return self

    def portalEmail(self):
        configlet = getUtility(IMailer)
        return {'name': configlet.email_from_name,
                'address': configlet.email_from_address}

    def render(self):
        if self.passcode is None:
            return self.resetform()
        else:
            return self.confirm()

    def update(self):
        super(ResetPassword, self).update()

        if self.passcode is None:
            context = self.context
            request = self.request

            if request.form.has_key('button.send'):
                loginid = request.get('loginid', '')

                principal = getPrincipalByLogin(loginid)

                try:
                    passcode = self.passwordtool.generatePasscode(principal)
                    event.notify(PasswordResetingEvent(principal, passcode))
                    IStatusMessage(request).add(
                        _(u'Your password has been reset and is being emailed to you.'))
                    self.redirect(absoluteURL(getSite(), request))

                except PasswordResetingError:
                    IStatusMessage(request).add(
                        _(u"System can't restore password for this principal."))

    @button.buttonAndHandler(_("Change password"))
    def changePassword(self, action):
        request = self.request

        service = IStatusMessage(request)

        data, errors = self.extractData()

        if errors:
            service.add(self.formErrorsMessage, 'error')
        else:
            self.passwordtool.resetPassword(self.passcode, data['password'])

            login = IPrincipalLogin(self.principal, None)
            if login is not None:
                login = login.login

            updateCredentials(request, login, data['password'])

            service.add(_('You have successfully changed your password.'))
            self.redirect(absoluteURL(getSite(), request))
