BitBucket-API
============

[![Build Status](https://secure.travis-ci.org/Sheeprider/Py-BitBucket.png?branch=master)](http://travis-ci.org/Sheeprider/Py-BitBucket)

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

##Installation
	
To install bitbucket-api, simply:

	$ pip install bitbucket-api


##Requirements

Bitbucket-api require [requests](https://github.com/kennethreitz/requests) to work, but dependencies should be handled by pip.
