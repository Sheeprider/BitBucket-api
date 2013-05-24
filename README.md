#BitBucket-API

[![Build Status](https://secure.travis-ci.org/Sheeprider/BitBucket-api.png)](http://travis-ci.org/Sheeprider/BitBucket-api)

BitBucket-api is an ISC Licensed library, written in Python.

Bitbucket has a REST API publicly available, this package provide methods to interact with it.
It allows you to access most repositories, services (hooks) and ssh keys related functionalities.

##Features

* Access public user informations
* Access public or private repositories, tags or branches
* Create, update or delete one of your repository
* Access, create, update or delete a service (hook)
* Access, create or delete an SSH key
* Download a repository as an archive
* Access, create, update or delete an issue
* Access, create, update or delete an issue comment

##Installation

To install bitbucket-api, simply:

	$ pip install bitbucket-api


##Requirements

Bitbucket-api require [requests](https://github.com/kennethreitz/requests), [sh](https://github.com/amoffat/sh) and [requests-oauthlib](https://github.com/requests/requests-oauthlib)to work, but dependencies should be handled by pip.

##Documentation
Documentation is available on [Read The Docs](https://bitbucket-api.readthedocs.org/en/latest/index.html).
