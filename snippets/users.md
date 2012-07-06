User snippets
=============

Snippets are small pieces of Python code you can use from your Django shell.

Setup
-----

    $ source ./booki.env
    $ django-admin.py shell


Sort book owners
----------------

How many books each user has, and sort them accordingly.

    >> from django.contrib.auth.models import User
    >> from django.db.models import Count
    >> users = User.objects.all().order_by("-count").annotate(count=Count("book"))
    >> users[0].count
    