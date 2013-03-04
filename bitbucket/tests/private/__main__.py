# -*- coding: utf-8 -*-
# run with `site-packages$> python -m bitbucket.tests.private`
import unittest

from bitbucket.tests.private import USERNAME, PASSWORD
from bitbucket.tests.private.private import BitbucketAuthenticatedMethodsTest
from bitbucket.tests.private.repository import RepositoryAuthenticatedMethodsTest
from bitbucket.tests.private.issue import IssueAuthenticatedMethodsTest
from bitbucket.tests.private.issue_comment import IssueCommentAuthenticatedMethodsTest
from bitbucket.tests.private.service import ServiceAuthenticatedMethodsTest
from bitbucket.tests.private.ssh import SSHAuthenticatedMethodsTest

private_test_suite = unittest.TestLoader().loadTestsFromTestCase(BitbucketAuthenticatedMethodsTest)
repository_test_suite = unittest.TestLoader().loadTestsFromTestCase(RepositoryAuthenticatedMethodsTest)
issue_test_suite = unittest.TestLoader().loadTestsFromTestCase(IssueAuthenticatedMethodsTest)
issue_comment_test_suite = unittest.TestLoader().loadTestsFromTestCase(IssueCommentAuthenticatedMethodsTest)
service_test_suite = unittest.TestLoader().loadTestsFromTestCase(ServiceAuthenticatedMethodsTest)
ssh_test_suite = unittest.TestLoader().loadTestsFromTestCase(SSHAuthenticatedMethodsTest)
alltests = unittest.TestSuite([private_test_suite, repository_test_suite, issue_test_suite, issue_comment_test_suite, service_test_suite, ssh_test_suite])

unittest.TextTestRunner(verbosity=2).run(alltests)
