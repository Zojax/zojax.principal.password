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
from zope.component import getUtilitiesFor
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from interfaces import IPasswordChecker


class CheckersVocabulary(object):
    """
    >>> from zojax.principal.password.vocabulary import CheckersVocabulary
    >>> vocFactory = CheckersVocabulary()

    >>> voc = vocFactory(None)
    >>> len(voc)
    0

    >>> from zope import interface
    >>> from zope.component import provideUtility
    >>> from zojax.principal.password.interfaces import IPasswordChecker

    >>> class Checker(object):
    ...     interface.implements(IPasswordChecker)
    ...     title = u'My checker'
    ...     def validate(self, password):
    ...         pass

    >>> checker = Checker()
    >>> provideUtility(checker, name='default')

    >>> voc = vocFactory(None)
    >>> len(voc)
    1

    >>> 'default' in voc
    True

    >>> voc.getTerm('default').title
    u'My checker'

    """
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        result = []
        for name, checker in getUtilitiesFor(IPasswordChecker):
            result.append((checker.title, name))

        result.sort()
        return SimpleVocabulary(
            [SimpleTerm(name, name, title) for title, name in result])
