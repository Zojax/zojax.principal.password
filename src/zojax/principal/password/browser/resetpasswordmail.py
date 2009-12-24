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
from datetime import datetime
from email.Utils import formataddr

from zope import component
from zope.security.management import queryInteraction
from zope.component import getUtility, getMultiAdapter
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL

from zojax.formatter.utils import getFormatter
from zojax.mail.interfaces import IMailer, IMailAddress
from zojax.mailtemplate.interfaces import IMailTemplate
from zojax.principal.password.interfaces import IPasswordResetingEvent


class ResetPasswordTemplate(object):

    def update(self):
        request = self.request
        principal = self.context.principal

        formatter = getFormatter(request, 'dateTime')
        self.date = formatter.format(datetime.now())

        configlet = getUtility(IMailer)
        self.email_from_name = configlet.email_from_name
        self.email_from_address = configlet.email_from_address

        remoteAddr = request.get('REMOTE_ADDR', '')
        forwardedFor = request.get('HTTP_X_FORWARDED_FOR', None)

        self.from_ip = (forwardedFor and '%s/%s' %
                        (remoteAddr, forwardedFor) or remoteAddr)

        self.url = '%s/resetpassword.html/%s/'%(
            absoluteURL(getSite(), request), self.context.passcode)


@component.adapter(IPasswordResetingEvent)
def resetingPassword(event):
    email = IMailAddress(event.principal, None)
    if email is None:
        return

    request = queryInteraction().participations[0]
    template = getMultiAdapter((event, request), IMailTemplate)
    template.send((formataddr((event.principal.title, email.address)),))
