# -*- coding: utf-8 -*-
try:
    # Try and get OAuth credentials first, if that fails try basic auth
    from settings import USERNAME, CONSUMER_KEY, CONSUMER_SECRET
    PASSWORD = None
except ImportError:
    try:
        # TODO : check validity of credentials ?
        from settings import USERNAME, PASSWORD
        CONSUMER_KEY = None
        CONSUMER_SECRET = None
    except ImportError:
        # Private tests require username and password of an existing user.
        exit('Please provide either USERNAME and PASSWORD or USERNAME, CONSUMER_KEY and CONSUMER_SECRET in bitbucket/tests/private/settings.py.')

