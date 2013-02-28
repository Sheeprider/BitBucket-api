# -*- coding: utf-8 -*-
import unittest

from bitbucket.bitbucket import Bitbucket
from bitbucket.tests.private import USERNAME, PASSWORD, REPO_SLUG


class AuthenticatedBitbucketTest(unittest.TestCase):
    """ Bitbucket test base class."""
    def setUp(self):
        """Creating a new authenticated Bitbucket..."""
        self.bb = Bitbucket(USERNAME, PASSWORD, REPO_SLUG)

    def tearDown(self):
        """Destroying the Bitbucket..."""
        self.bb = None


class BitbucketAuthenticatedMethodsTest(AuthenticatedBitbucketTest):
    """ Testing Bitbucket annonymous methods."""

    def test_get_tags(self):
        """ Test get_tags."""
        success, result = self.bb.get_tags()
        self.assertTrue(success)
        self.assertIsInstance(result, dict)

    def test_get_branches(self):
        """ Test get_branches."""
        success, result = self.bb.get_branches()
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
