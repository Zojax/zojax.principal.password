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
import unittest, doctest
from zope import interface
from zope.publisher.browser import BrowserRequest
from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.principal.password.testing import zojaxPrincipalPassword


def test_suite():
    interface.classImplements(BrowserRequest, ILayoutFormLayer)

    configlet = doctest.DocFileSuite(
        "configlet.txt",
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    configlet.layer = zojaxPrincipalPassword

    reset = doctest.DocFileSuite(
        "reset.txt",
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    reset.layer = zojaxPrincipalPassword

    preference = doctest.DocFileSuite(
        "preference.txt",
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    preference.layer = zojaxPrincipalPassword
    return unittest.TestSuite((preference, configlet, reset))
