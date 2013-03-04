# -*- coding: utf-8 -*-
try:
    # TODO : check validity of credentials ?
    from settings import USERNAME, PASSWORD
except ImportError:
    # Private tests require username and password of an existing user.
    exit('Please provide USERNAME and PASSWORD in bitbucket/tests/private/settings.py .')
