#!/usr/bin/env python
# This file is part of booktype-scrolls.
# Copyright (c) 2012 Aleksandar Erkalovic <aleksandar.erkalovic@sourcefabric.org>
#
# Booktype is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Booktype is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with booktype-scrolls.  If not, see <http://www.gnu.org/licenses/>.


from django.conf import settings

import sys

from optparse import OptionParser

from booki.editor import models

if __name__ == '__main__':
    # optparse just because i have python 2.6 on this machine

    usage = "usage: %prog [options] before after"
    parser = OptionParser(usage)
    parser.add_option('-b', '--book', dest='book', metavar='BOOK', action="store", type="string", help="Book name.")

    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("Ahhh... I don't know what i should replace with what!")

    if not options.book:
        print 'You must specify book name.'
        sys.exit(-1)

    try:
        book = models.Book.objects.get(url_title__iexact=options.book)
    except models.Book.DoesNotExist:
        print 'Can not find book %s ! Here is a list of all the books:' % options.book

        for book in models.Book.objects.all().order_by('url_title'):
            print '    >> %s' % book.url_title

        sys.exit(-1)

    # We change content only in last version of this book
    for chapter in models.Chapter.objects.filter(version=book.getVersion()):
        print '  >> ', chapter.url_title

        chapter.content = chapter.content.replace(args[0], args[1])
        chapter.save()
