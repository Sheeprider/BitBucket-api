# -*- coding: utf-8 -*-
import unittest

from bitbucket.bitbucket import Bitbucket
from bitbucket.tests.private import USERNAME, PASSWORD

TEST_REPO_SLUG = 'test_bitbucket_api'


class AuthenticatedBitbucketTest(unittest.TestCase):
    """ Bitbucket test base class for authenticated methods."""
    def setUp(self):
        """Creating a new authenticated Bitbucket..."""
        self.bb = Bitbucket(USERNAME, PASSWORD)
        # Create a repository.
        success, result = self.bb.repository.create(TEST_REPO_SLUG, has_issues=True)
        # Save repository's id
        assert success
        self.bb.repo_slug = result[u'slug']

    def tearDown(self):
        """Destroying the Bitbucket..."""
        # Delete the repository.
        self.bb.repository.delete()
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
