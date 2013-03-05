# -*- coding: utf-8 -*-
from bitbucket.tests.private.private import AuthenticatedBitbucketTest
from bitbucket.tests.public import httpbin


class ServiceAuthenticatedMethodsTest(AuthenticatedBitbucketTest):
    """ Testing bitbucket.service methods."""

    def test_all(self):
        """ Test get all services."""
        success, result = self.bb.service.all()
        self.assertTrue(success)
        self.assertIsInstance(result, list)

    def _create_service(self):
        # Test create an invalid service
        with self.assertRaises(TypeError):
            self.bb.service.create()
        # Test create an service
        success, result = self.bb.service.create(
            service=u'POST',
            URL=httpbin + 'post',)
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        # Save latest service's id
        self.service_id = result[u'id']

    def _get_service(self):
        # Test get an service.
        success, result = self.bb.service.get(service_id=self.service_id)
        self.assertTrue(success)
        self.assertIsInstance(result, list)
        # Test get an invalid service.
        success, result = self.bb.service.get(service_id=99999999999)
        self.assertTrue(success)
        self.assertEqual(result, [])

    def _update_service(self):
        # Test service update.
        test_url = httpbin + 'get'
        success, result = self.bb.service.update(service_id=self.service_id,
            URL=test_url)
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        self.assertEqual(test_url, result[u'service'][u'fields'][0][u'value'])

    def _delete_service(self):
        # Test service delete.
        success, result = self.bb.service.delete(service_id=self.service_id)
        self.assertTrue(success)
        self.assertEqual(result, '')

        success, result = self.bb.service.get(service_id=self.service_id)
        self.assertTrue(success)
        self.assertEqual(result, [])

    def test_CRUD(self):
        """ Test service create/read/update/delete."""
        self._create_service()
        self._get_service()
        self._update_service()
        self._delete_service()
