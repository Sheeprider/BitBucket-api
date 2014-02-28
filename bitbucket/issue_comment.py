# -*- coding: utf-8 -*-
URLS = {
    # Issue comments
    'GET_COMMENTS': 'repositories/%(username)s/%(repo_slug)s/issues/%(issue_id)s/comments/',
    'GET_COMMENT': 'repositories/%(username)s/%(repo_slug)s/issues/%(issue_id)s/comments/%(comment_id)s/',
    'CREATE_COMMENT': 'repositories/%(username)s/%(repo_slug)s/issues/%(issue_id)s/comments/',
    'UPDATE_COMMENT': 'repositories/%(username)s/%(repo_slug)s/issues/%(issue_id)s/comments/%(comment_id)s/',
    'DELETE_COMMENT': 'repositories/%(username)s/%(repo_slug)s/issues/%(issue_id)s/comments/%(comment_id)s/',
}


class IssueComment(object):
    """ This class provide issue's comments related methods to Bitbucket objects."""

    def __init__(self, issue):
        self.issue = issue
        self.bitbucket = self.issue.bitbucket
        self.bitbucket.URLS.update(URLS)
        self.issue_id = issue.issue_id

    def all(self, issue_id=None, repo_slug=None):
        """ Get issue comments from one of your repositories.
        """
        issue_id = issue_id or self.issue_id
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('GET_COMMENTS',
                                 username=self.bitbucket.username,
                                 repo_slug=repo_slug,
                                 issue_id=issue_id)
        return self.bitbucket.dispatch('GET', url, auth=self.bitbucket.auth)

    def get(self, comment_id, issue_id=None, repo_slug=None):
        """ Get an issue from one of your repositories.
        """
        issue_id = issue_id or self.issue_id
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('GET_COMMENT',
                                 username=self.bitbucket.username,
                                 repo_slug=repo_slug,
                                 issue_id=issue_id,
                                 comment_id=comment_id)
        return self.bitbucket.dispatch('GET', url, auth=self.bitbucket.auth)

    def create(self, issue_id=None, repo_slug=None, **kwargs):
        """ Add an issue comment to one of your repositories.
            Each issue comment require only the content data field
            the system autopopulate the rest.
        """
        issue_id = issue_id or self.issue_id
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('CREATE_COMMENT',
                                 username=self.bitbucket.username,
                                 repo_slug=repo_slug,
                                 issue_id=issue_id)
        return self.bitbucket.dispatch('POST', url, auth=self.bitbucket.auth, **kwargs)

    def update(self, comment_id, issue_id=None, repo_slug=None, **kwargs):
        """ Update an issue comment in one of your repositories.
            Each issue comment require only the content data field
            the system autopopulate the rest.
        """
        issue_id = issue_id or self.issue_id
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('UPDATE_COMMENT',
                                 username=self.bitbucket.username,
                                 repo_slug=repo_slug,
                                 issue_id=issue_id,
                                 comment_id=comment_id)
        return self.bitbucket.dispatch('PUT', url, auth=self.bitbucket.auth, **kwargs)

    def delete(self, comment_id, issue_id=None, repo_slug=None):
        """ Delete an issue from one of your repositories.
        """
        issue_id = issue_id or self.issue_id
        repo_slug = repo_slug or self.bitbucket.repo_slug or ''
        url = self.bitbucket.url('DELETE_COMMENT',
                                 username=self.bitbucket.username,
                                 repo_slug=repo_slug,
                                 issue_id=issue_id,
                                 comment_id=comment_id)
        return self.bitbucket.dispatch('DELETE', url, auth=self.bitbucket.auth)
