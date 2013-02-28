# -*- coding: utf-8 -*-
import os
from zipfile import is_zipfile

from bitbucket.tests.private.private import AuthenticatedBitbucketTest
from bitbucket.tests.private import REPO_SLUG

TEST_REPO_SLUG = 'test_bitbucket_api'


class RepositoryAuthenticatedMethodsTest(AuthenticatedBitbucketTest):
    """ Testing bitbucket.repository methods."""

    def test_all(self):
        """ Test get all repositories."""
        success, result = self.bb.repository.all()
        self.assertTrue(success)
        self.assertIsInstance(result, list)

    def test_get(self):
        """ Test get a repository."""
        success, result = self.bb.repository.get()
        self.assertTrue(success)
        self.assertIsInstance(result, dict)

    def test_create(self):
        """ Test repository creation."""
        success, result = self.bb.repository.create(TEST_REPO_SLUG)
        self.assertTrue(success)
        self.assertIsInstance(result, dict)

    def test_update(self):
        """ Test repository update."""
        success, result = self.bb.repository.get()
        old_desc = result[u'description']
        # Try to change description
        test_description = 'Test Description'
        success, result = self.bb.repository.update(REPO_SLUG,
            description=test_description)
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        self.assertEqual(test_description, result[u'description'])
        # Put back old Description
        self.bb.repository.update(REPO_SLUG,
            description=old_desc)

    def test_delete(self):
        """ Test repository deletion."""
        success, result = self.bb.repository.delete(TEST_REPO_SLUG)
        self.assertTrue(success)
        self.assertEqual(result, '')

        success, result = self.bb.repository.get(TEST_REPO_SLUG)
        self.assertFalse(success)

    def test_archive(self):
        """ Test repository download as archive."""
        success, archive_path = self.bb.repository.archive()
        self.assertTrue(success)
        self.assertTrue(os.path.exists(archive_path))
        self.assertTrue(is_zipfile(archive_path))
        # delete temporary file
        os.unlink(archive_path)
