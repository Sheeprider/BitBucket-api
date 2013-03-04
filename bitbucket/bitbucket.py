# -*- coding: utf-8 -*-
# git+git://github.com/Sheeprider/BitBucket-api.git

__all__ = ['Bitbucket', ]

import json

from requests import Request

from repository import Repository
from service import Service
from ssh import SSH
from issue import Issue


class Bitbucket(object):
    """ This class lets you interact with the bitbucket public API.
        It depends on Requests.
    """
    def __init__(self, username='', password='', repo_name_or_slug=''):
        self.username = username
        self.password = password
        self.repo_slug = repo_name_or_slug.lower().replace(r'[^a-z0-9_-]+', '-')
        self.repo_tree = {}

        self.repository = Repository(self)
        self.service = Service(self)
        self.ssh = SSH(self)
        self.issue = Issue(self)

    #  ===================
    #  = Getters/Setters =
    #  ===================

    @property
    def auth(self):
        """ Return credentials for current Bitbucket user. """
        return (self.username, self.password)

    @property
    def username(self):
        """Your username."""
        return self._username

    @username.setter
    def username(self, value):
        if isinstance(value, basestring):
            self._username = unicode(value)
        if value is None:
            self._username = None

    @username.deleter
    def username(self):
        del self._username

    @property
    def password(self):
        """Your password."""
        return self._password

    @password.setter
    def password(self, value):
        if isinstance(value, basestring):
            self._password = unicode(value)
        if value is None:
            self._password = None

    @password.deleter
    def password(self):
        del self._password

    @property
    def repo_slug(self):
        """Your repository slug name."""
        return self._repo_slug

    @repo_slug.setter
    def repo_slug(self, value):
        if isinstance(value, basestring):
            value = unicode(value)
        self._repo_slug = value.lower().replace(r'[^a-z0-9_-]+', '-')
        if value is None:
            self._repo_slug = None

    @repo_slug.deleter
    def repo_slug(self):
        del self._repo_slug

    #  ======================
    #  = High lvl functions =
    #  ======================

    def dispatch(self, method, url, auth=None, params=None, **kwargs):
        """ Send HTTP request, with given method,
            credentials and data to the given URL,
            and return the status code and the result on success.
        """
        r = Request(
            method=method,
            url=url,
            auth=auth,
            params=params,
            data=kwargs)
        send = r.send()
        status = r.response.status_code
        text = r.response.text
        error = r.response.error
        if send:
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
                return (False, 'Unauthorized access, '
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
        url = self.url('GET_BRANCHES', username=self.username, repo_slug=repo_slug)
        return self.dispatch('GET', url, auth=self.auth)

    #  ========
    #  = URLs =
    #  ========
    URLS = {
        'BASE': 'https://api.bitbucket.org/1.0/%s',
        # Get user profile and repos
        'GET_USER': 'users/%(username)s/',
        # Search repo
        # 'SEARCH_REPO': 'repositories/?name=%(search)s',
        # Get tags & branches
        'GET_TAGS': 'repositories/%(username)s/%(repo_slug)s/tags/',
        'GET_BRANCHES': 'repositories/%(username)s/%(repo_slug)s/branches/',
    }
