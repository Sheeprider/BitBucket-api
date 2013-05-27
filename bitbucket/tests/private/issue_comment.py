# -*- coding: utf-8 -*-
from bitbucket.tests.private.private import AuthenticatedBitbucketTest


class IssueCommentAuthenticatedMethodsTest(AuthenticatedBitbucketTest):
    """ Testing bitbucket.issue.comments methods."""

    def setUp(self):
        """ Add an issue to the test repository and save it's id."""
        super(IssueCommentAuthenticatedMethodsTest, self).setUp()
        # Create an issue.
        success, result = self.bb.issue.create(
            title=u'Test Issue Bitbucket API',
            content=u'Test Issue Bitbucket API',
            responsible=self.bb.username,
            status=u'new',
            kind=u'bug',)
        # Save latest issue's id
        assert success
        self.bb.issue.comment.issue_id = result[u'local_id']

    def tearDown(self):
        """ Delete the issue."""
        self.bb.issue.delete(issue_id=self.bb.issue.comment.issue_id)
        super(IssueCommentAuthenticatedMethodsTest, self).tearDown()

    def test_all(self):
        """ Test get all issue comments."""
        success, result = self.bb.issue.comment.all()
        self.assertTrue(success)
        self.assertIsInstance(result, list)

    def _create_issue_comment(self):
        content = u'Test Issue comment Bitbucket API'
        # Test create an issue comment
        success, result = self.bb.issue.comment.create(
            content=content)
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        self.assertEqual(result[u'content'], content)
        # Save latest issue comment's id
        self.comment_id = result[u'comment_id']

    def _get_issue_comment(self):
        # Test get an issue comment.
        success, result = self.bb.issue.comment.get(comment_id=self.comment_id)
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        # Test get an invalid issue comment.
        success, result = self.bb.issue.comment.get(comment_id=99999999999)
        self.assertFalse(success)

    def _update_issue_comment(self):
        # Test issue comment update.
        test_content = 'Test content'
        success, result = self.bb.issue.comment.update(
            comment_id=self.comment_id,
            content=test_content)
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        self.assertEqual(test_content, result[u'content'])

    def _delete_issue_comment(self):
        # Test issue comment delete.
        success, result = self.bb.issue.comment.delete(
            comment_id=self.comment_id)
        self.assertTrue(success)
        self.assertEqual(result, '')

        success, result = self.bb.issue.comment.get(comment_id=self.comment_id)
        self.assertFalse(success)

    def test_CRUD(self):
        """ Test issue comment create/read/update/delete."""
        self._create_issue_comment()
        self._get_issue_comment()
        self._update_issue_comment()
        self._delete_issue_comment()
