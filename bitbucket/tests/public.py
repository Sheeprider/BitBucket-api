# -*- coding: utf-8 -*-
# run with `site-packages$> python -m bitbucket.tests.public`
import unittest
from bitbucket.bitbucket import Bitbucket


httpbin = 'http://httpbin.org/'
foo = u'foo'
bar = u'bar'
username = 'baptistemillou'


class AnonymousBitbucketTest(unittest.TestCase):
    """ Bitbucket test base class."""
    def setUp(self):
        """Create a new annonymous Bitbucket..."""
        self.bb = Bitbucket()

    def tearDown(self):
        """Destroy the Bitbucket..."""
        self.bb = None


class BitbucketUtilitiesTest(AnonymousBitbucketTest):
    """ Test Bitbucket utilities functions."""

    def test_default_credential(self):
        self.assertEqual(self.bb.username, '')
        self.assertEqual(self.bb.password, '')
        self.assertEqual(self.bb.repo_slug, '')

    def test_dispatch_get(self):
        success, result = self.bb.dispatch('GET', httpbin + 'get')
        self.assertTrue(success)
        self.assertIsInstance(result, dict)

    def test_dispatch_post(self):
        success, result = self.bb.dispatch('POST', httpbin + 'post', foo='bar')
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['form'], {foo: bar})

    def test_dispatch_put(self):
        success, result = self.bb.dispatch('PUT', httpbin + 'put', foo='bar')
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['form'], {foo: bar})

    def test_dispatch_delete(self):
        success, result = self.bb.dispatch('DELETE', httpbin + 'delete')
        self.assertTrue(success)
        self.assertIsInstance(result, dict)

    def test_url_simple(self):
        base = self.bb.URLS['BASE']
        create_repo = self.bb.URLS['CREATE_REPO']
        self.assertEqual(self.bb.url('CREATE_REPO'), base % create_repo)

    def test_url_complex(self):
        base = self.bb.URLS['BASE']
        get_branches = self.bb.URLS['GET_BRANCHES']
        self.assertEqual(
            self.bb.url('GET_BRANCHES',
                username=self.bb.username,
                repo_slug=self.bb.repo_slug),
            base % get_branches % {'username': '', 'repo_slug': ''})

    def test_auth(self):
        self.assertEqual(self.bb.auth, (self.bb.username, self.bb.password))

    def test_username(self):
        self.bb.username = foo
        self.assertEqual(self.bb.username, foo)

        del self.bb.username
        with self.assertRaises(AttributeError):
            self.bb.username

    def test_password(self):
        self.bb.password = foo
        self.assertEqual(self.bb.password, foo)

        del self.bb.password
        with self.assertRaises(AttributeError):
            self.bb.password

    def test_repo_slug(self):
        self.bb.repo_slug = foo
        self.assertEqual(self.bb.repo_slug, foo)

        del self.bb.repo_slug
        with self.assertRaises(AttributeError):
            self.bb.repo_slug


class BitbucketAnnonymousMethodsTest(AnonymousBitbucketTest):
    """ Test Bitbucket annonymous methods."""

    def test_get_user(self):
        """ Test get_user on specific user."""
        success, result = self.bb.get_user(username=username)
        self.assertTrue(success)
        self.assertIsInstance(result, dict)

    def test_get_self_user(self):
        """ Test get_user on self username."""
        self.bb.username = username
        success, result = self.bb.get_user()
        self.assertTrue(success)
        self.assertIsInstance(result, dict)

    def test_get_none_user(self):
        """ Test get_user with no username."""
        self.bb.username = None
        success, result = self.bb.get_user()
        self.assertFalse(success)
        self.assertEqual(result, 'Service not found.')

    def test_get_public_repos(self):
        """ Test public_repos on specific user."""
        success, result = self.bb.repository.public(username=username)
        self.assertTrue(success)
        self.assertIsInstance(result, (dict, list))

    def test_get_self_public_repos(self):
        """ Test public_repos on specific user."""
        self.bb.username = username
        success, result = self.bb.repository.public()
        self.assertTrue(success)
        self.assertIsInstance(result, (dict, list))

    def test_get_none_public_repos(self):
        """ Test public_repos on specific user."""
        self.bb.username = None
        success, result = self.bb.repository.public()
        self.assertFalse(success)
        self.assertEqual(result, 'Service not found.')

if __name__ == "__main__":
    unittest.main()
