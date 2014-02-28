# -*- coding: utf-8 -*-
from .issue_comment import IssueComment


URLS = {
    # Issues
    'GET_ISSUES': 'repositories/%(username)s/%(repo_slug)s/issues/',
    'GET_ISSUE': 'repositories/%(username)s/%(repo_slug)s/issues/%(issue_id)s/',
    'CREATE_ISSUE': 'repositories/%(username)s/%(repo_slug)s/issues/',
    'UPDATE_ISSUE': 'repositories/%(username)s/%(repo_slug)s/issues/%(issue_id)s/',
    'DELETE_ISSUE': 'repositories/%(username)s/%(repo_slug)s/issues/%(issue_id)s/',
}


class Issue(object):
    """ This class provide issue-related methods to Bitbucket objects."""

    def __init__(self, bitbucket, issue_id=None):
        self.bitbucket = bitbucket
        self.bitbucket.URLS.update(URLS)
        self.issue_id = issue_id
        self.comment = IssueComment(self)

    @property
    def issue_id(self):
        """Your repository slug name."""
        return self._issue_id

    @issue_id.setter
    def issue_id(self, value):
        if value:
            self._issue_id = int(value)
        elif value is None:
            self._issue_id = None

    @issue_id.deleter
    def issue_id(self):
        del self._issue_id

    def all(self, repo_slug=None, params=None):
        """ Get issues from one of your repositories.
        """
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('GET_ISSUES', username=self.bitbucket.username, repo_slug=repo_slug)
        return self.bitbucket.dispatch('GET', url, auth=self.bitbucket.auth, params=params)

    def get(self, issue_id, repo_slug=None):
        """ Get an issue from one of your repositories.
        """
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('GET_ISSUE', username=self.bitbucket.username, repo_slug=repo_slug, issue_id=issue_id)
        return self.bitbucket.dispatch('GET', url, auth=self.bitbucket.auth)

    def create(self, repo_slug=None, **kwargs):
        """
        Add an issue to one of your repositories.
        Each issue require a different set of attributes,
        you can pass them as keyword arguments (attributename='attributevalue').
        Attributes are:

            * title: The title of the new issue.
            * content: The content of the new issue.
            * component: The component associated with the issue.
            * milestone: The milestone associated with the issue.
            * version: The version associated with the issue.
            * responsible: The username of the person responsible for the issue.
            * status: The status of the issue (new, open, resolved, on hold, invalid, duplicate, or wontfix).
            * kind: The kind of issue (bug, enhancement, or proposal).
        """
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('CREATE_ISSUE', username=self.bitbucket.username, repo_slug=repo_slug)
        return self.bitbucket.dispatch('POST', url, auth=self.bitbucket.auth, **kwargs)

    def update(self, issue_id, repo_slug=None, **kwargs):
        """
        Update an issue to one of your repositories.
        Each issue require a different set of attributes,
        you can pass them as keyword arguments (attributename='attributevalue').
        Attributes are:

            * title: The title of the new issue.
            * content: The content of the new issue.
            * component: The component associated with the issue.
            * milestone: The milestone associated with the issue.
            * version: The version associated with the issue.
            * responsible: The username of the person responsible for the issue.
            * status: The status of the issue (new, open, resolved, on hold, invalid, duplicate, or wontfix).
            * kind: The kind of issue (bug, enhancement, or proposal).
        """
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('UPDATE_ISSUE', username=self.bitbucket.username, repo_slug=repo_slug, issue_id=issue_id)
        return self.bitbucket.dispatch('PUT', url, auth=self.bitbucket.auth, **kwargs)

    def delete(self, issue_id, repo_slug=None):
        """ Delete an issue from one of your repositories.
        """
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('DELETE_ISSUE', username=self.bitbucket.username, repo_slug=repo_slug, issue_id=issue_id)
        return self.bitbucket.dispatch('DELETE', url, auth=self.bitbucket.auth)
