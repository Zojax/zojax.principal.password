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
from zope import component, interface
from zope.proxy import removeAllProxies
from zope.app.security.interfaces import ILoginPassword
from zope.app.security.loginpassword import LoginPassword
from zope.app.security.principalregistry import Principal

from zojax.authentication.interfaces import IPrincipalLogin


class DictLoginPassword(LoginPassword):
    component.adapts(dict)
    interface.implementsOnly(ILoginPassword)


class PrincipalLogin(object):
    component.adapts(Principal)
    interface.implements(IPrincipalLogin)

    def __init__(self, principal):
        self.login = removeAllProxies(principal).getLogin()
