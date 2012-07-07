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

    >>> from django.contrib.auth.models import User
    >>> from django.db.models import Count
    >>> users = User.objects.all().order_by("-count").annotate(count=Count("book"))
    >>> users[0].count

List user registration by month
-------------------------------

This only works with PostgreSQL.

    >>> from django.db.models import Count
    >>> from django.contrib.auth.models import User
    >>> 
    >>> for u in User.objects.extra(select={'year':'EXTRACT(year FROM date_joined)', 'month': 'EXTRACT(month FROM date_joined)'}).values('year', 'month').annotate(Count('username')).order_by("-year", "-month"):
    ...     print '%d/%d  users: %d' % (u['month'], u['year'], u['username__count'])

    
