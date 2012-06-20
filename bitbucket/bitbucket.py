# -*- coding: utf-8 -*-
# git+git://github.com/Sheeprider/Py-BitBucket.git

__all__ = ['Bitbucket', ]

from tempfile import NamedTemporaryFile
from zipfile import ZipFile
import json

from requests import Request


class Bitbucket(object):
    """ This class lets you interact with the bitbucket public API.
        It depends on Requests.

        Curently, only repositories, services (hooks) and ssh keys
        related functionalities are available.
    """
    def __init__(self, username='', password='', repo_name_or_slug=''):
        self.username = username
        self.password = password
        self.repo_slug = repo_name_or_slug.lower().replace(r'[^a-z0-9_-]+', '-')
        self.repo_tree = {}

    # =============
    # = Utilities =
    # =============
    def dispatch(self, method, url, auth=None, **kwargs):
        """ Send HTTP request, with given method,
            credentials and data to the given URL,
            and return the status code and the result on success.
        """
        r = Request(
            method=method,
            url=url,
            auth=auth,
            data=kwargs)
        if r.send():
            return (r.response.status_code, r.response.text)
        else:
            return False

    def url(self, action, **kwargs):
        """ Construct and return the URL for a specific API service. """
        # TODO : should be static method ?
        return self.URLS['BASE'] % self.URLS[action] % kwargs

    def get_files_in_dir(self, repo_slug=None, dir='/'):
        repo_slug = repo_slug or self.repo_slug or ''
        dir = dir.lstrip('/')
        url = self.url(
            'GET_ARCHIVE',
            username=self.username,
            repo_slug=repo_slug,
            format='src')
        dir_url = url + dir
        response = self.dispatch('GET', dir_url, auth=self.auth)
        if response and response[0] == 200:
            repo_tree = json.loads(response[1])
            url = self.url(
                'GET_ARCHIVE',
                username=self.username,
                repo_slug=repo_slug,
                format='raw')
            # Download all files in dir
            for file in repo_tree['files']:
                file_url = url + '/'.join((file['path'],))
                response = self.dispatch('GET', file_url, auth=self.auth)
                self.repo_tree[file['path']] = response[1]
            # recursively download in dirs
            for directory in repo_tree['directories']:
                dir_path = '/'.join((dir, directory))
                self.get_files_in_dir(repo_slug=repo_slug, dir=dir_path)

    @property
    def auth(self):
        """ Return credentials for current Bitbucket user. """
        return (self.username, self.password)

    def username():
        """Your username."""
        def fget(self):
            return self._username

        def fset(self, value):
            self._username = '%s' % value

        def fdel(self):
            del self._username
        return locals()
    username = property(**username())

    def password():
        """Your password."""
        def fget(self):
                return self._password

        def fset(self, value):
                self._password = '%s' % value

        def fdel(self):
                del self._password
        return locals()
    password = property(**password())

    def repo_slug():
        """Your repository slug name."""
        def fget(self):
                return self._repo_slug

        def fset(self, value):
            value = '%s' % value
            self._repo_slug = value.lower().replace(r'[^a-z0-9_-]+', '-')

        def fdel(self):
                del self._repo_slug
        return locals()
    repo_slug = property(**repo_slug())

    # =======
    # = API =
    # =======
    def get_user(self, username=None):
        """ Returns user informations.
            If username is not defined, tries to return own informations.
        """
        username = username or self.username or ''
        url = self.url('GET_USER', username=username)
        response = self.dispatch('GET', url)
        if response:
            return json.loads(response[1])['user']

    def public_repos(self, username=None):
        """ Returns all public repositories from an user.
            If username is not defined, tries to return own public repos.
        """
        username = username or self.username or ''
        url = self.url('GET_USER', username=username)
        response = self.dispatch('GET', url)
        if response:
            return json.loads(response[1])['repositories']

    def get_repositories(self):
        """ Return own repositories."""
        url = self.url('GET_USER', username=self.username)
        response = self.dispatch('GET', url, auth=self.auth)
        if response:
            return json.loads(response[1])['repositories']

    def get_repository(self, repo_slug=None):
        """ Get a single repository on Bitbucket and return it."""
        repo_slug = repo_slug or self.repo_slug or ''
        url = self.url('GET_REPO', username=self.username, repo_slug=repo_slug)
        response = self.dispatch('GET', url, auth=self.auth)
        if response:
            return json.loads(response[1])

    def get_tags(self, repo_slug=None):
        """ Get a single repository on Bitbucket and return its tags."""
        repo_slug = repo_slug or self.repo_slug or ''
        url = self.url('GET_TAGS', username=self.username, repo_slug=repo_slug)
        response = self.dispatch('GET', url, auth=self.auth)
        if response:
            return json.loads(response[1])

    def get_branches(self, repo_slug=None):
        """ Get a single repository on Bitbucket and return its branches."""
        repo_slug = repo_slug or self.repo_slug or ''
        url = self.url('GET_BRANCHES', username=self.username, repo_slug=repo_slug)
        response = self.dispatch('GET', url, auth=self.auth)
        if response:
            return json.loads(response[1])

    def create_repository(self, repo_name, scm='git', private=True):
        """ Creates a new repository on own Bitbucket account and return it."""
        url = self.url('CREATE_REPO')
        response = self.dispatch('POST', url, auth=self.auth, name=repo_name, scm=scm, is_private=private)
        if response:
            return json.loads(response[1])

    def update_repository(self, repo_slug=None, **kwargs):
        """ Updates repository on own Bitbucket account and return it."""
        url = self.url('UPDATE_REPO', username=self.username, repo_slug=repo_slug)
        response = self.dispatch('PUT', url, self.auth, **kwargs)
        if response:
            return json.loads(response[1])

    def delete_repository(self, repo_slug=None):
        """ Delete a repository on own Bitbucket account.
            Please use with caution as there is NO confimation and NO undo.
        """
        repo_slug = repo_slug or self.repo_slug or ''
        url = self.url('DELETE_REPO', username=self.username, repo_slug=repo_slug)
        response = self.dispatch('DELETE', url, auth=self.auth)
        return response

    def add_service(self, service, repo_slug=None, **kwargs):
        """ Add a service (hook) to one of your repositories.
            Each type of service require a different set of additionnal fields,
            you can pass them as keyword arguments (fieldname='fieldvalue').
        """
        repo_slug = repo_slug or self.repo_slug or ''
        url = self.url('SET_SERVICE', username=self.username, repo_slug=repo_slug)
        response = self.dispatch('POST', url, auth=self.auth, type=service, **kwargs)
        if response:
            return json.loads(response[1])

    def get_service(self, service_id, repo_slug=None):
        """ Get a service (hook) from one of your repositories.
        """
        repo_slug = repo_slug or self.repo_slug or ''
        url = self.url('GET_SERVICE', username=self.username, repo_slug=repo_slug, service_id=service_id)
        response = self.dispatch('GET', url, auth=self.auth)
        if response:
            return json.loads(response[1])

    def update_service(self, service_id, repo_slug=None, **kwargs):
        """ Update a service (hook) from one of your repositories.
        """
        repo_slug = repo_slug or self.repo_slug or ''
        url = self.url('UPDATE_SERVICE', username=self.username, repo_slug=repo_slug, service_id=service_id)
        response = self.dispatch('PUT', url, auth=self.auth, **kwargs)
        if response:
            return json.loads(response[1])

    def delete_service(self, service_id, repo_slug=None):
        """ Delete a service (hook) from one of your repositories.
            Please use with caution as there is NO confimation and NO undo.
        """
        repo_slug = repo_slug or self.repo_slug or ''
        url = self.url('DELETE_SERVICE', username=self.username, repo_slug=repo_slug, service_id=service_id)
        response = self.dispatch('DELETE', url, auth=self.auth)
        return bool(response)

    def get_services(self, repo_slug=None):
        """ Get all services (hook) from one of your repositories.
        """
        repo_slug = repo_slug or self.repo_slug or ''
        url = self.url('GET_SERVICES', username=self.username, repo_slug=repo_slug)
        response = self.dispatch('GET', url, auth=self.auth)
        if response:
            return json.loads(response[1])

    def get_archive(self, repo_slug=None, format='zip', prefix=''):
        """ Get one of your repositories and compress it as an archive.
            Return the path of the archive.

            format parameter is curently not supported.
        """
        prefix = '%s'.lstrip('/') % prefix
        self.get_files_in_dir(repo_slug=repo_slug, dir='/')
        with NamedTemporaryFile(delete=False) as archive:
            with ZipFile(archive, 'w') as zip_archive:
                for name, file in self.repo_tree.items():
                    with NamedTemporaryFile() as temp_file:
                        temp_file.write(file)
                        zip_archive.write(temp_file.name, prefix + name)
        return archive.name

    def get_ssh_keys(self):
        """ Get all ssh keys associated with your account.
        """
        url = self.url('GET_SSH_KEYS')
        response = self.dispatch('GET', url, auth=self.auth)
        if response:
            return json.loads(response[1])

    def get_ssh_key(self, key_id=1):
        """ Get one of the ssh keys associated with your account.
        """
        url = self.url('GET_SSH_KEY', key_id=key_id)
        response = self.dispatch('GET', url, auth=self.auth)
        if response:
            return json.loads(response[1])

    def set_ssh_key(self, key=None, label=None):
        """ Associate an ssh key with your account and return it.
        """
        key = '%s' % key
        url = self.url('SET_SSH_KEY')
        response = self.dispatch('POST', url, auth=self.auth, key=key, label=label)
        if response:
            return json.loads(response[1])

    def delete_ssh_key(self, key_id=None):
        """ Delete one of the ssh keys associated with your account.
            Please use with caution as there is NO confimation and NO undo.
        """
        url = self.url('DELETE_SSH_KEY', key_id=key_id)
        response = self.dispatch('DELETE', url, auth=self.auth)
        return response

    #  ========
    #  = URLs =
    #  ========
    URLS = {
        'BASE': 'https://api.bitbucket.org/1.0/%s',
        # Get user profile and repos
        'GET_USER': 'users/%(username)s/',
        # Get archive
        'GET_ARCHIVE': 'repositories/%(username)s/%(repo_slug)s/%(format)s/master/',
        # Search repo
        # 'SEARCH_REPO': 'repositories/?name=%(search)s',
        # Set repo
        'CREATE_REPO': 'repositories/',
        'GET_REPO': 'repositories/%(username)s/%(repo_slug)s/',
        'GET_TAGS': 'repositories/%(username)s/%(repo_slug)s/tags/',
        'GET_BRANCHES': 'repositories/%(username)s/%(repo_slug)s/branches/',
        'UPDATE_REPO': 'repositories/%(username)s/%(repo_slug)s/',
        'DELETE_REPO': 'repositories/%(username)s/%(repo_slug)s/',
        # Get services (hooks)
        'GET_SERVICE': 'repositories/%(username)s/%(repo_slug)s/services/%(service_id)s/',
        'GET_SERVICES': 'repositories/%(username)s/%(repo_slug)s/services/',
        # Set services (hooks)
        'SET_SERVICE': 'repositories/%(username)s/%(repo_slug)s/services/',
        'UPDATE_SERVICE': 'repositories/%(username)s/%(repo_slug)s/services/%(service_id)s/',
        'DELETE_SERVICE': 'repositories/%(username)s/%(repo_slug)s/services/%(service_id)s/',
        # SSH keys
        'GET_SSH_KEYS': 'ssh-keys/',
        'GET_SSH_KEY': 'ssh-keys/%(key_id)s',
        'SET_SSH_KEY': 'ssh-keys/',
        'DELETE_SSH_KEY': 'ssh-keys/%(key_id)s',

    }

#  ============
#  = Services =
#  ============
# SERVICES = {
#   'Basecamp': ('Username', 'Password', 'Discussion URL',),
#   'CIA.vc': ('Module', 'Project',),
#   'Email Diff': ('Email',),
#   'Email': ('Email',),
#   'FogBugz': ('Repository ID', 'CVSSubmit URL',),
#   'FriendFeed': ('Username', 'Remote Key', 'Format',),
#   'Geocommit': (None,),
#   'Issues': (None,),
#   'Lighthouse': ('Project ID', 'API Key', 'Subdomain',),
#   'Pivotal Tracker': ('Token',),
#   'POST': ('URL',),
#   'Rietveld': ('Email', 'Password', 'URL',),
#   'Superfeedr': (None,),
# }
