# -*- coding: utf-8 -*-
import os
from zipfile import is_zipfile

from bitbucket.tests.private.private import AuthenticatedBitbucketTest

TEST_REPO_SLUG = "test_repository_creation"


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
        # TODO : test private/public repository creation
        success, result = self.bb.repository.create(TEST_REPO_SLUG)
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        # Delete repo
        success, result = self.bb.repository.delete(repo_slug=TEST_REPO_SLUG)
        assert success

    def test_update(self):
        """ Test repository update."""
        # Try to change description
        test_description = 'Test Description'
        success, result = self.bb.repository.update(description=test_description)
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        self.assertEqual(test_description, result[u'description'])

    def test_delete(self):
        """ Test repository deletion."""
        # Create repo
        success, result = self.bb.repository.create(TEST_REPO_SLUG)
        assert success
        # Delete it
        success, result = self.bb.repository.delete(repo_slug=TEST_REPO_SLUG)
        self.assertTrue(success)
        self.assertEqual(result, '')

        success, result = self.bb.repository.get(repo_slug=TEST_REPO_SLUG)
        self.assertFalse(success)

    def test_archive(self):
        """ Test repository download as archive."""
        # TODO : add a commit, to be able to download the repo
        success, archive_path = self.bb.repository.archive()
        self.assertTrue(success)
        self.assertTrue(os.path.exists(archive_path))
        self.assertTrue(is_zipfile(archive_path))
        # delete temporary file
        os.unlink(archive_path)
