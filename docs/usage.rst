Usage
-----

Public
^^^^^^
You can access any public repository on Bitbucket, but some actions won't be available without credentials. ::

	>>> from bitbucket.bitbucket import Bitbucket
	>>> bb = Bitbucket(USERNAME, repo_name_or_slug='public_slug')
	>>> success, result = bb.repository.delete()
	>>> print success
	False


Private
^^^^^^^
With the correct credentials you can access private repositories on Bitbucket. ::

	>>> from bitbucket.bitbucket import Bitbucket
	>>> bb = Bitbucket(USERNAME, PASSWORD, 'private_slug')
	>>> success, result = bb.repository.get()
	>>> print success, result
	True {...}

Examples
^^^^^^^^
Connect using Oauth ::

	>>> import webbrowser
	>>> from bitbucket.bitbucket import Bitbucket
	>>> bb = Bitbucket(USERNAME)
	>>> # First time we need to open up a browser to enter the verifier
	>>> if not OAUTH_ACCESS_TOKEN and not OAUTH_ACCESS_TOKEN_SECRET:
	>>>     bb.authorize(CONSUMER_KEY, CONSUMER_SECRET, 'http://localhost/')
	>>>     # open a webbrowser and get the token
	>>>     webbrowser.open(bb.url('AUTHENTICATE', token=bb.access_token))
	>>>     # Copy the verifier field from the URL in the browser into the console
	>>>     oauth_verifier = raw_input('Enter verifier from url [oauth_verifier]')
	>>>     bb.verify(oauth_verifier)
	>>>     OAUTH_ACCESS_TOKEN = bb.access_token
	>>>     OAUTH_ACCESS_TOKEN_SECRET = bb.access_token_secret
	>>> else:
	>>>     bb.authorize(CONSUMER_KEY, CONSUMER_SECRET, 'http://localhost/', OAUTH_ACCESS_TOKEN, OAUTH_ACCESS_TOKEN_SECRET)

List all repositories for a user (from `@matthew-campbell`_)::

	>>> from bitbucket.bitbucket import Bitbucket
	>>> bb = Bitbucket(USERNAME, PASSWORD)
	>>> success, repositories = bb.repository.all()
	>>> for repo in sorted(repositories):
	>>>     p = '+'
	>>>     if repo['is_private']:
	>>>         p ='-'
	>>>     print('({}){}, {}, {}'.format(p, repo['name'], repo['last_updated'], repo['scm']))
	>>> print('Total {}'.format(len(repositories)))

.. _@matthew-campbell: https://gist.github.com/matthew-campbell/5471630
