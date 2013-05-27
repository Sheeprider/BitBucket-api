# -*- coding: utf-8 -*-
from functools import wraps
from zipfile import is_zipfile
import os
import random
import sh
import string
import unittest

from bitbucket.tests.private.private import AuthenticatedBitbucketTest

TEST_REPO_SLUG = "test_repository_creation"


def skipUnlessHasGit(f):
    """ This decorator pass the test if git is not found."""
    @wraps(f)
    def _decorator():
        try:
            sh.git(version=True, _out='/dev/null')
            return f()
        except sh.CommandNotFound:
            return unittest.skip("Git is not installed")
    return _decorator


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


class ArchiveRepositoryAuthenticatedMethodsTest(AuthenticatedBitbucketTest):
    """
    Testing bitbucket.repository.archive method, which require
    custom setUp and tearDown methods.

    test_archive require a commit to download the repository.
    """

    def setUp(self):
        """ Clone the test repo locally, then add and push a commit."""
        super(ArchiveRepositoryAuthenticatedMethodsTest, self).setUp()
        # Clone test repository localy.
        repo_origin = 'git@bitbucket.org:%s/%s.git' % (self.bb.username, self.bb.repo_slug)
        # TODO : Put the temp folder on the right place for windows.
        repo_folder = os.path.join(
            '/tmp',
            'bitbucket-' + ''.join(random.choice(string.digits + string.letters) for x in range(10)))
        sh.mkdir(repo_folder)
        sh.cd(repo_folder)
        self.pwd = sh.pwd().strip()
        sh.git.init()
        sh.git.remote('add', 'origin', repo_origin)
        # Add commit with empty file.
        sh.touch('file')
        sh.git.add('.')
        sh.git.commit('-m', '"Add empty file."')
        sh.git.push('origin', 'master')

    def tearDown(self):
        """ Delete the git folder."""
        super(ArchiveRepositoryAuthenticatedMethodsTest, self).tearDown()
        sh.rm('-rf', self.pwd)

    @skipUnlessHasGit
    def test_archive(self):
        """ Test repository download as archive."""
        success, archive_path = self.bb.repository.archive()
        self.assertTrue(success)
        self.assertTrue(os.path.exists(archive_path))
        self.assertTrue(is_zipfile(archive_path))
        # delete temporary file
        os.unlink(archive_path)
