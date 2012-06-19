#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from bitbucket import Bitbucket

class BitbucketTestSuite(unittest.TestCase):
  """ Bitbucket's repository test cases."""
  def setUp(self):
    self.bb = Bitbucket()

if __name__ == '__main__':
    unittest.main()
