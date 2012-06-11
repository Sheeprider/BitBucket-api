# -*- coding: utf-8 -*-

__version__ = '0.1'
__all__ = ['Bitbucket',]

import json

from requests import Request

class Bitbucket(object):
  """ Bitbucket is an abstraction class for bitbucket API.
      It depends on Requests.
  """
  def __init__(self, username='', password='', repo_name_or_slug=''):
    self.username = username
    self.password = password
    self.repo_slug = repo_name_or_slug.lower().replace(r'[^a-z0-9_-]+', '-')

  # =============
  # = Utilities =
  # =============
  def dispatch(self, method, url, auth=None, **kwargs):
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
    # TODO : should be static method ?
    return self.URLS['BASE'] % self.URLS[action] % kwargs
  @property
  def auth(self):
    return (self.username, self.password)

  def username():
      doc = "Your username."
      def fget(self):
          return self._username
      def fset(self, value):
          self._username = '%s' % value
      def fdel(self):
          del self._username
      return locals()
  username = property(**username())
  def password():
      doc = "Your password."
      def fget(self):
          return self._password
      def fset(self, value):
          self._password = '%s' % value
      def fdel(self):
          del self._password
      return locals()
  password = property(**password())
  def repo_slug():
      doc = "Your repository slug name."
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
  def user(self, username=None):
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
  def own_repos(self):
    """ Return own repositories.
    """
    username = self.username
    url = self.url('GET_USER', username=username)
    response = self.dispatch('GET', url, auth=self.auth)
    if response:
      return json.loads(response[1])['repositories']
  def create_repository(self, repo_name, scm='git', private=True):
    """ Creates a new repository on own Bitbucket account and return it."""
    url = self.url('CREATE_REPO')
    response = self.dispatch('POST', url, auth=self.auth, name=repo_name, scm=scm, is_private=private)
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

  #  ========
  #  = URLs =
  #  ========
  URLS = {
    'BASE': 'https://api.bitbucket.org/1.0/%s',
    # Get user profile and repos
    'GET_USER': 'users/%(username)s/',
    # Search repo
    # 'SEARCH_REPO': 'repositories/?name=%(search)s',
    # Set repo
    'CREATE_REPO' :'repositories/',
    # 'UPDATE_REPO' :'repositories/%(username)s/%(repo_slug)s/',
    'DELETE_REPO' :'repositories/%(username)s/%(repo_slug)s/',
    # Get services (hooks)
    'GET_SERVICE': 'repositories/%(username)s/%(repo_slug)s/services/%(service_id)s/',
    'GET_SERVICES': 'repositories/%(username)s/%(repo_slug)s/services/',
    # Set services (hooks)
    'SET_SERVICE': 'repositories/%(username)s/%(repo_slug)s/services/',
    'UPDATE_SERVICE': 'repositories/%(username)s/%(repo_slug)s/services/%(service_id)s/',
    'DELETE_SERVICE': 'repositories/%(username)s/%(repo_slug)s/services/%(service_id)s/',
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
