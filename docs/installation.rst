Installation
------------

Pip
^^^
Installing Bitbucket-API is simple with pip: ::

	pip install Bitbucket-API

Get the Code & contribute
^^^^^^^^^^^^^^^^^^^^^^^^^
Bitbucket-API is hosted on GitHub, where the code is always available.

You can either clone the public repository: ::

	git clone git@github.com:Sheeprider/BitBucket-api.git

Download the tarball: ::

	curl -OL https://github.com/Sheeprider/BitBucket-api/tarball/master

Or, download the zipball: ::

	curl -OL https://github.com/Sheeprider/Bitbucket-API/zipball/master

Test
^^^^
Run public tests::

	site-packages$> python -m bitbucket.tests.public

Run private tests. Require **USERNAME** and **PASSWORD** or **USERNAME**, **CONSUMER_KEY** and **CONSUMER_SECRET** in *bitbucket/tests/private/settings.py*::

	site-packages$> python -m bitbucket.tests.private
