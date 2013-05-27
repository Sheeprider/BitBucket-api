# -*- coding: utf-8 -*-
# run with `site-packages$> python -m bitbucket.tests.private`
import unittest

from bitbucket.tests.private.private import BitbucketAuthenticatedMethodsTest
from bitbucket.tests.private.repository import RepositoryAuthenticatedMethodsTest, ArchiveRepositoryAuthenticatedMethodsTest
from bitbucket.tests.private.issue import IssueAuthenticatedMethodsTest
from bitbucket.tests.private.issue_comment import IssueCommentAuthenticatedMethodsTest
from bitbucket.tests.private.service import ServiceAuthenticatedMethodsTest
from bitbucket.tests.private.ssh import SSHAuthenticatedMethodsTest

if __name__ == '__main__':
    unittest.main()
