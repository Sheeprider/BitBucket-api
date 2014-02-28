# -*- coding: utf-8 -*-
# git+git://github.com/Sheeprider/BitBucket-api.git

__all__ = ['Bitbucket', ]

try:
    from urlparse import parse_qs
except ImportError:
    from urllib.parse import parse_qs

import json
import re

from requests import Request, Session
from requests_oauthlib import OAuth1
import requests

from .issue import Issue
from .repository import Repository
from .service import Service
from .ssh import SSH
from .deploy_key import DeployKey


#  ========
#  = URLs =
#  ========
URLS = {
    'BASE': 'https://bitbucket.org/!api/1.0/%s',
    # Get user profile and repos
    'GET_USER': 'users/%(username)s/',
    'GET_USER_PRIVILEGES': 'user/privileges',
    # Search repo
    # 'SEARCH_REPO': 'repositories/?name=%(search)s',
    # Get tags & branches
    'GET_TAGS': 'repositories/%(username)s/%(repo_slug)s/tags/',
    'GET_BRANCHES': 'repositories/%(username)s/%(repo_slug)s/branches/',

    'REQUEST_TOKEN': 'oauth/request_token/',
    'AUTHENTICATE': 'oauth/authenticate?oauth_token=%(token)s',
    'ACCESS_TOKEN': 'oauth/access_token/'
}


class Bitbucket(object):
    """ This class lets you interact with the bitbucket public API. """
    def __init__(self, username='', password='', repo_name_or_slug=''):
        self.username = username
        self.password = password
        self.repo_slug = repo_name_or_slug
        self.repo_tree = {}
        self.URLS = URLS

        self.repository = Repository(self)
        self.service = Service(self)
        self.ssh = SSH(self)
        self.issue = Issue(self)
        self.deploy_key = DeployKey(self)

        self.access_token = None
        self.access_token_secret = None
        self.consumer_key = None
        self.consumer_secret = None
        self.oauth = None

    #  ===================
    #  = Getters/Setters =
    #  ===================

    @property
    def auth(self):
        """ Return credentials for current Bitbucket user. """
        if self.oauth:
            return self.oauth
        return (self.username, self.password)

    @property
    def username(self):
        """Return your repository's username."""
        return self._username

    @username.setter
    def username(self, value):
        try:
            if isinstance(value, basestring):
                self._username = unicode(value)
        except NameError:
            self._username = value

        if value is None:
            self._username = None

    @username.deleter
    def username(self):
        del self._username

    @property
    def password(self):
        """Return your repository's password."""
        return self._password

    @password.setter
    def password(self, value):
        try:
            if isinstance(value, basestring):
                self._password = unicode(value)
        except NameError:
            self._password = value

        if value is None:
            self._password = None

    @password.deleter
    def password(self):
        del self._password

    @property
    def repo_slug(self):
        """Return your repository's slug name."""
        return self._repo_slug

    @repo_slug.setter
    def repo_slug(self, value):
        if value is None:
            self._repo_slug = None
        else:
            try:
                if isinstance(value, basestring):
                    value = unicode(value)
            except NameError:
                pass
            value = value.lower()
            self._repo_slug = re.sub(r'[^a-z0-9_-]+', '-', value)

    @repo_slug.deleter
    def repo_slug(self):
        del self._repo_slug

    #  ========================
    #  = Oauth authentication =
    #  ========================

    def authorize(self, consumer_key, consumer_secret, callback_url=None,
                  access_token=None, access_token_secret=None):
        """
        Call this with your consumer key, secret and callback URL, to
        generate a token for verification.
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        if not access_token and not access_token_secret:
            if not callback_url:
                return (False, "Callback URL required")
            oauth = OAuth1(
                consumer_key,
                client_secret=consumer_secret,
                callback_uri=callback_url)
            r = requests.post(self.url('REQUEST_TOKEN'), auth=oauth)
            if r.status_code == 200:
                creds = parse_qs(r.content)

                self.access_token = creds.get('oauth_token')[0]
                self.access_token_secret = creds.get('oauth_token_secret')[0]
            else:
                return (False, r.content)
        else:
            self.finalize_oauth(access_token, access_token_secret)

        return (True, None)

    def verify(self, verifier, consumer_key=None, consumer_secret=None,
               access_token=None, access_token_secret=None):
        """
        After converting the token into verifier, call this to finalize the
        authorization.
        """
        # Stored values can be supplied to verify
        self.consumer_key = consumer_key or self.consumer_key
        self.consumer_secret = consumer_secret or self.consumer_secret
        self.access_token = access_token or self.access_token
        self.access_token_secret = access_token_secret or self.access_token_secret

        oauth = OAuth1(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
            verifier=verifier)
        r = requests.post(self.url('ACCESS_TOKEN'), auth=oauth)
        if r.status_code == 200:
            creds = parse_qs(r.content)
        else:
            return (False, r.content)

        self.finalize_oauth(creds.get('oauth_token')[0],
                            creds.get('oauth_token_secret')[0])
        return (True, None)

    def finalize_oauth(self, access_token, access_token_secret):
        """ Called internally once auth process is complete. """
        self.access_token = access_token
        self.access_token_secret = access_token_secret

        # Final OAuth object
        self.oauth = OAuth1(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret)

    #  ======================
    #  = High lvl functions =
    #  ======================

    def dispatch(self, method, url, auth=None, params=None, **kwargs):
        """ Send HTTP request, with given method,
            credentials and data to the given URL,
            and return the success and the result on success.
        """
        r = Request(
            method=method,
            url=url,
            auth=auth,
            params=params,
            data=kwargs)
        s = Session()
        resp = s.send(r.prepare())
        status = resp.status_code
        text = resp.text
        error = resp.reason
        if status >= 200 and status < 300:
            if text:
                try:
                    return (True, json.loads(text))
                except TypeError:
                    pass
                except ValueError:
                    pass
            return (True, text)
        elif status >= 300 and status < 400:
            return (
                False,
                'Unauthorized access, '
                'please check your credentials.')
        elif status >= 400 and status < 500:
            return (False, 'Service not found.')
        elif status >= 500 and status < 600:
                return (False, 'Server error.')
        else:
            return (False, error)

    def url(self, action, **kwargs):
        """ Construct and return the URL for a specific API service. """
        # TODO : should be static method ?
        return self.URLS['BASE'] % self.URLS[action] % kwargs

    #  =====================
    #  = General functions =
    #  =====================

    def get_user(self, username=None):
        """ Returns user informations.
            If username is not defined, tries to return own informations.
        """
        username = username or self.username or ''
        url = self.url('GET_USER', username=username)
        response = self.dispatch('GET', url)
        try:
            return (response[0], response[1]['user'])
        except TypeError:
            pass
        return response

    def get_tags(self, repo_slug=None):
        """ Get a single repository on Bitbucket and return its tags."""
        repo_slug = repo_slug or self.repo_slug or ''
        url = self.url('GET_TAGS', username=self.username, repo_slug=repo_slug)
        return self.dispatch('GET', url, auth=self.auth)

    def get_branches(self, repo_slug=None):
        """ Get a single repository on Bitbucket and return its branches."""
        repo_slug = repo_slug or self.repo_slug or ''
        url = self.url('GET_BRANCHES',
                       username=self.username,
                       repo_slug=repo_slug)
        return self.dispatch('GET', url, auth=self.auth)

    def get_privileges(self):
        """ Get privledges for this user. """
        url = self.url('GET_USER_PRIVILEGES')
        return self.dispatch('GET', url, auth=self.auth)
