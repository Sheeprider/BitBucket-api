# -*- coding: utf-8 -*-
URLS = {
    # SSH keys
    'GET_SSH_KEYS': 'ssh-keys/',
    'GET_SSH_KEY': 'ssh-keys/%(key_id)s',
    'SET_SSH_KEY': 'ssh-keys/',
    'DELETE_SSH_KEY': 'ssh-keys/%(key_id)s',
}


class SSH(object):
    """ This class provide ssh-related methods to Bitbucket objects."""

    def __init__(self, bitbucket):
        self.bitbucket = bitbucket
        self.bitbucket.URLS.update(URLS)

    def all(self):
        """ Get all ssh keys associated with your account.
        """
        url = self.bitbucket.url('GET_SSH_KEYS')
        return self.bitbucket.dispatch('GET', url, auth=self.bitbucket.auth)

    def get(self, key_id=None):
        """ Get one of the ssh keys associated with your account.
        """
        url = self.bitbucket.url('GET_SSH_KEY', key_id=key_id)
        return self.bitbucket.dispatch('GET', url, auth=self.bitbucket.auth)

    def create(self, key=None, label=None):
        """ Associate an ssh key with your account and return it.
        """
        key = '%s' % key
        url = self.bitbucket.url('SET_SSH_KEY')
        return self.bitbucket.dispatch('POST', url, auth=self.bitbucket.auth, key=key, label=label)

    def delete(self, key_id=None):
        """ Delete one of the ssh keys associated with your account.
            Please use with caution as there is NO confimation and NO undo.
        """
        url = self.bitbucket.url('DELETE_SSH_KEY', key_id=key_id)
        return self.bitbucket.dispatch('DELETE', url, auth=self.bitbucket.auth)
