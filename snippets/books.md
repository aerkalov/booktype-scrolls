Books snippets
==============

Snippets are small pieces of Python code you can use from your Django shell.

Setup
-----

    $ source ./booki.env
    $ django-admin.py shell


List book creation by month
-------------------------------

This only works with PostgreSQL.

    >>> from django.db.models import Count
    >>> from booki.editor import models
    >>> 
    >>> for b in models.Book.objects.extra(select={'year': 'EXTRACT(year FROM created)', 'month': 'EXTRACT(month FROM created)'}).values('year', 'month').annotate(Count('id')).order_by('-year', '-month'):
    ...     print '%d/%d  books:%d ' % (b['month'], b['year'], b['id__count'])

    
