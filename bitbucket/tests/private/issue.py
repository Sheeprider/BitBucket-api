# -*- coding: utf-8 -*-
from bitbucket.tests.private.private import AuthenticatedBitbucketTest


class IssueAuthenticatedMethodsTest(AuthenticatedBitbucketTest):
    """ Testing bitbucket.issue methods."""

    def test_all(self):
        """ Test get all issues."""
        success, result = self.bb.issue.all()
        self.assertTrue(success)
        self.assertIsInstance(result, dict)

    def _create_issue(self):
        # Test create an invalid issue
        success, result = self.bb.issue.create()
        self.assertFalse(success)
        # Test create an issue
        success, result = self.bb.issue.create(
            title=u'Test Issue Bitbucket API',
            content=u'Test Issue Bitbucket API',
            responsible=self.bb.username,
            status=u'new',
            kind=u'bug',)
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        # Save latest issue's id
        self.issue_id = result[u'local_id']

    def _get_issue(self):
        # Test get an issue.
        success, result = self.bb.issue.get(issue_id=self.issue_id)
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        # Test get an invalid issue.
        success, result = self.bb.issue.get(issue_id=99999999999)
        self.assertFalse(success)

    def _update_issue(self):
        # Test issue update.
        test_content = 'Test content'
        success, result = self.bb.issue.update(issue_id=self.issue_id,
            content=test_content)
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        self.assertEqual(test_content, result[u'content'])

    def _delete_issue(self):
        # Test issue delete.
        success, result = self.bb.issue.delete(issue_id=self.issue_id)
        self.assertTrue(success)
        self.assertEqual(result, '')

        success, result = self.bb.issue.get(issue_id=self.issue_id)
        self.assertFalse(success)

    def test_CRUD(self):
        """ Test issue create/read/update/delete."""
        self._create_issue()
        self._get_issue()
        self._update_issue()
        self._delete_issue()
