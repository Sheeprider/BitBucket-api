# -*- coding: utf-8 -*-
import unittest
import webbrowser

from bitbucket.bitbucket import Bitbucket

TEST_REPO_SLUG = 'test_bitbucket_api'

# Store oauth credentials between tests
OAUTH_ACCESS_TOKEN = ''
OAUTH_ACCESS_TOKEN_SECRET = ''


class AuthenticatedBitbucketTest(unittest.TestCase):
    """ Bitbucket test base class for authenticated methods."""
    def setUp(self):
        """Creating a new authenticated Bitbucket..."""
        try:
            # Try and get OAuth credentials first, if that fails try basic auth
            from settings import USERNAME, CONSUMER_KEY, CONSUMER_SECRET
            PASSWORD = None
        except ImportError:
            try:
                # TODO : check validity of credentials ?
                from settings import USERNAME, PASSWORD
                CONSUMER_KEY = None
                CONSUMER_SECRET = None
            except ImportError:
                # Private tests require username and password of an existing user.
                raise ImportError('Please provide either USERNAME and PASSWORD or USERNAME, CONSUMER_KEY and CONSUMER_SECRET in bitbucket/tests/private/settings.py.')

        if USERNAME and PASSWORD:
            self.bb = Bitbucket(USERNAME, PASSWORD)
        elif USERNAME and CONSUMER_KEY and CONSUMER_SECRET:
            # Try Oauth authentication
            global OAUTH_ACCESS_TOKEN, OAUTH_ACCESS_TOKEN_SECRET
            self.bb = Bitbucket(USERNAME)

            # First time we need to open up a browser to enter the verifier
            if not OAUTH_ACCESS_TOKEN and not OAUTH_ACCESS_TOKEN_SECRET:
                self.bb.authorize(CONSUMER_KEY, CONSUMER_SECRET, 'http://localhost/')
                # open a webbrowser and get the token
                webbrowser.open(self.bb.url('AUTHENTICATE', token=self.bb.access_token))
                # Copy the verifier field from the URL in the browser into the console
                token_is_valid = False
                while not token_is_valid:
                    # Ensure a valid oauth_verifier before starting tests
                    oauth_verifier = raw_input('Enter verifier from url [oauth_verifier]')
                    token_is_valid = bool(oauth_verifier and self.bb.verify(oauth_verifier)[0])
                    if not token_is_valid:
                        print('Invalid oauth_verifier, please try again or quit with CONTROL-C.')
                OAUTH_ACCESS_TOKEN = self.bb.access_token
                OAUTH_ACCESS_TOKEN_SECRET = self.bb.access_token_secret
            else:
                self.bb.authorize(CONSUMER_KEY, CONSUMER_SECRET, 'http://localhost/', OAUTH_ACCESS_TOKEN, OAUTH_ACCESS_TOKEN_SECRET)

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
        # test with invalid repository name
        success, result = self.bb.get_tags(repo_slug='azertyuiop')
        self.assertFalse(success)

    def test_get_branches(self):
        """ Test get_branches."""
        success, result = self.bb.get_branches()
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        # test with invalid repository name
        success, result = self.bb.get_branches(repo_slug='azertyuiop')
        self.assertFalse(success)
