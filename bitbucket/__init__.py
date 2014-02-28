# -*- coding: utf-8 -*-
__version__ = '0.5.0'

__doc__ = """
Bitbucket has a REST API publicly available, this package provide methods to interact with it.
It allows you to access repositories and perform various actions on them.

Various usages : ::

    from bitbucket.bitbucket import Bitbucket

    # Access a public repository
    bb = Bitbucket(USERNAME, repo_name_or_slug="public_repository")

    # Access a private repository
    bb = Bitbucket(USERNAME, PASSWORD, repo_name_or_slug="private_repository")

    # Access a private repository through oauth
    bb = Bitbucket(USERNAME, repo_name_or_slug="public_repository")
    bb.authorize(CONSUMER_KEY, CONSUMER_SECRET, 'http://localhost/')


    # Access your working repository
    success, result = bb.repository.get()

    # Create a repository, and define it as your working repository
    success, result = bb.repository.create("repository_slug")
    bb.repo_slug = "repository_slug"

    # Update your working repository
    success, result = bb.repository.update(description='new description')

    # Delete a repository
    success, result = bb.repository.delete("repository_slug")

    # Download a repository as an archive
    success, archive_path = bb.repository.archive()

    # Access user informations
    success, result = bb.get_user(username=USERNAME)

    # Access tags and branches
    success, result = bb.get_tags()
    success, result = bb.get_branches()

    # Access, create, update or delete a service (hook)
    success, result = bb.service.get(service_id=SERVICE_ID)
    success, result = bb.service.create(service=u'POST', URL='http://httpbin.org/')
    success, result = bb.service.update(service_id=SERVICE_ID, URL='http://google.com')
    success, result = bb.service.delete(service_id=SERVICE_ID)

    # Access, create or delete an SSH key
    success, result = bb.ssh.get(key_id=SSH_ID)
    success, result = bb.ssh.create(key=r'ssh-rsa a1b2c3d4e5', label=u'my key')
    success, result = bb.ssh.delete(key_id=SSH_ID)

    # Access, create, update or delete an issue
    success, result = bb.issue.get(issue_id=ISSUE_ID)
    success, result = bb.issue.create(
        title=u'Issue title',
        content=u'Issue content',
        responsible=bb.username,
        status=u'new',
        kind=u'bug')
    success, result = bb.issue.update(issue_id=ISSUE_ID, content='New content')
    success, result = bb.issue.delete(issue_id=ISSUE_ID)

    # Access, create, update or delete an issue comment
    success, result = bb.issue.comment.get(comment_id=COMMENT_ID)
    success, result = bb.issue.comment.create(content='Content')
    success, result = bb.issue.comment.update(
        comment_id=COMMENT_ID,
        content='New content')
    success, result = bb.issue.comment.delete(comment_id=COMMENT_ID)

"""
