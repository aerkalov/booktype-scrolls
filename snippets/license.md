License snippets
================

Snippets are small pieces of Python code you can use from your Django shell.

Setup
-----

    $ source ./booki.env
    $ django-admin.py shell


How popular is license
----------------------


    >> from booki.editor import models
    >> from django.db.models import Count
    >> for lic in models.License.objects.order_by("-count").annotate(count=Count("book")):
    ..     print lic.name, lic.count
