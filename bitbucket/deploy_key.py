# -*- coding: utf-8 -*-
URLS = {
    # deploy keys
    'GET_DEPLOY_KEYS': 'repositories/%(username)s/%(repo_slug)s/deploy-keys',
    'SET_DEPLOY_KEY': 'repositories/%(username)s/%(repo_slug)s/deploy-keys',
    'GET_DEPLOY_KEY': 'repositories/%(username)s/%(repo_slug)s/deploy-keys/%(key_id)s',
    'DELETE_DEPLOY_KEY': 'repositories/%(username)s/%(repo_slug)s/deploy-keys/%(key_id)s',
}


class DeployKey(object):
    """ This class provide services-related methods to Bitbucket objects."""

    def __init__(self, bitbucket):
        self.bitbucket = bitbucket
        self.bitbucket.URLS.update(URLS)

    def all(self, repo_slug=None):
        """ Get all ssh keys associated with a repo
        """
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('GET_DEPLOY_KEYS',
                                 username=self.bitbucket.username,
                                 repo_slug=repo_slug)
        return self.bitbucket.dispatch('GET', url, auth=self.bitbucket.auth)

    def get(self, repo_slug=None, key_id=None):
        """ Get one of the ssh keys associated with this repo
        """
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('GET_DEPLOY_KEY',
                                 key_id=key_id,
                                 username=self.bitbucket.username,
                                 repo_slug=repo_slug)
        return self.bitbucket.dispatch('GET', url, auth=self.bitbucket.auth)

    def create(self, repo_slug=None, key=None, label=None):
        """ Associate an ssh key with your repo and return it.
        """
        key = '%s' % key
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('SET_DEPLOY_KEY',
                                 username=self.bitbucket.username,
                                 repo_slug=repo_slug)
        return self.bitbucket.dispatch('POST',
                                       url,
                                       auth=self.bitbucket.auth,
                                       key=key,
                                       label=label)

    def delete(self, repo_slug=None, key_id=None):
        """ Delete one of the ssh keys associated with your repo.
            Please use with caution as there is NO confimation and NO undo.
        """
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('DELETE_DEPLOY_KEY',
                                 key_id=key_id,
                                 username=self.bitbucket.username,
                                 repo_slug=repo_slug)
        return self.bitbucket.dispatch('DELETE', url, auth=self.bitbucket.auth)
