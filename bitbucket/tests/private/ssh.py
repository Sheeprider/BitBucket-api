# -*- coding: utf-8 -*-
from bitbucket.tests.private.private import AuthenticatedBitbucketTest


class SSHAuthenticatedMethodsTest(AuthenticatedBitbucketTest):
    """ Testing bitbucket.ssh methods."""

    def test_all(self):
        """ Test get all sshs."""
        success, result = self.bb.ssh.all()
        self.assertTrue(success)
        self.assertIsInstance(result, list)

    def _create_ssh(self):
        # Test create an invalid ssh
        success, result = self.bb.ssh.create()
        self.assertFalse(success)
        # Test create an ssh
        success, result = self.bb.ssh.create(
            key=r'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDftGyHMtFSVkIxESnJQQDGy+uXT3LuUqkaLKKjb+WeXxJEabVyur8z4urzRQyHSenrrAyd9GTLtx1zmxCn7LP626ztrIYqjdK2WBhx+wjBsF39+DNvokwLAzHpQVZnywZZXaf8aeKdwiLmUpBSpfk7dSYsjQvfkmsjBpDJz9z9NsOzVK3fIVjEdnu7nPgINiJ/DlqB9zfdXpu0o98tH/WfhDo+PvkIWYrkH/cms9LIsc4zNZIKJF6i0hDAAnC0V27GQKRXpXcnj32PZvk2eXF8TxiO0rGjkEBSd1J638GHvgLI9d8iQUAVIOm69x/trQhUKcGlcHcbU0VzaFaIYawr baptiste@smoothie-creative.com\
',
            label=u'test key',)
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        # Save latest ssh's id
        self.ssh_id = result[u'pk']

    def _get_ssh(self):
        # Test get an ssh.
        success, result = self.bb.ssh.get(key_id=self.ssh_id)
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        # Test get an invalid ssh.
        success, result = self.bb.ssh.get(key_id=99999999999)
        self.assertFalse(success)

    def _delete_ssh(self):
        # Test ssh delete.
        success, result = self.bb.ssh.delete(key_id=self.ssh_id)
        self.assertTrue(success)
        self.assertEqual(result, '')

        success, result = self.bb.ssh.get(key_id=self.ssh_id)
        self.assertFalse(success)

    def test_CRUD(self):
        """ Test ssh create/read/delete."""
        self._create_ssh()
        self._get_ssh()
        self._delete_ssh()
