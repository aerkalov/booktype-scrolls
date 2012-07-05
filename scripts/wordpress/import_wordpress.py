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

import feedparser
import datetime
import urllib
import urllib2
import httplib
import shutil
import urlparse
import os
import sys

from lxml import etree, html
from cStringIO import StringIO

from optparse import OptionParser

from django.core.files import File
from django.contrib.auth.models import User

from booki.utils.misc import bookiSlugify
from booki.utils import config
from booki.editor import common, models
from booki.editor import models


def downloadFile(url):
    """
    Downloads file from the URL. Returns None in case of any error.
    """

    try:
        r = urllib2.urlopen(urllib2.Request(url))
    except httplib.HTTPException:
        return None
    except ValueError:
        return None
    except urllib2.HTTPError:
        return None
    except IOError:
        return None

    try:
        data = r.read()
    except:
        return None
    finally:
        r.close()

    return data

def importFeed(document, conf):
    """
    Imports content of Wordpress export into Booktype.
    """

    # To create a book we use "createBook" function. It will do good part of magic for us in the background.
    # We have to provide:
    #   - owner of the book; every book must have an owner
    #   - book title; this is full book name
    #   - book status; every book has a status, let us just use "new" for now
    #   - book url; book must have unique name and in Booktype world it is book url name

    from booki.utils.book import createBook

    book = createBook(conf['user'], 
                      conf['bookTitle'], 
                      status = "new", 
                      bookURL = conf['bookTitleURL'])

    # We use config API to check if books are by default visible or not
    isVisible = config.getConfiguration('CREATE_BOOK_VISIBLE', True)
    book.hidden = not isVisible

    book.save()

    # "createBook" function has already created default list of statuses. Let's just fetch "new" status because
    # we will need it for Chapters later
    stat = models.BookStatus.objects.filter(book=book, name="new")[0]

    # What is default URL for Wordpress blog
    wpLink = document['feed']['link']

    attachments = []

    for item in document['items']:
        # We only care about posts which have "publish" status. Ignore everything else for now.
        if item['wp_status'] !=  u'publish':
            continue

        chapterTitle = item['title']
        print '>> ', chapterTitle

        # So... let's clean our Wordpress post a bit. Here we ASSUME that empty line is used to separate paragraphs in Wordpress post.
        content = item['content'][0]['value'].replace('\r\n', '\n')
        content = '\n'.join(['<p>%s</p>' % p  for p in content.split('\n\n') if p.strip() != ''])

        # Every Booktype chapter starts with Chapter title embded in H2 tag. 
        content = u'<h2>%s</h2>%s' % (chapterTitle, content)

        tree = html.document_fromstring(content)

        for e in tree.iter():

            # We only care about images now
            if e.tag == 'img':
                src = e.get('src')
            
                if src:
                    if src.startswith('/'):
                        src = wpLink+src

                    # We don't need to download picture if it was already downloaed
                    if not src in attachments:
                        attachments.append(src)

                        u = urlparse.urlsplit(src)

                        # Get the file name and take care of funny stuff like %20 in file names
                        fileName = os.path.basename(urllib.unquote(u.path))
                    
                        print '      >> ', fileName
                        
                        # Download image
                        data = downloadFile(src)
                        
                        # Let us create this attachment if we managed to download something
                        if data:
                            # Create new Attachment. "book" argument is part of legacy here, we really should care only about "version".
                            # Expect this to be removed in the future. Also, every Attachment can have different status. Not that it is
                            # used anywhere at the moment, but it has to be here.
                            
                            att = models.Attachment(book = book,
                                                    version = book.version,
                                                    status = stat)
                            
                            # We use standard method for saving the data.
                            f2 = File(StringIO(data))
                            f2.size = len(data)
                            att.attachment.save(fileName, f2, save=True)
                            
                            # If filename with the same name already exists then Django will add prefix to the name.
                            # For instance: Image.jpg would become Image_1.jpg. That is why we check the new name.

                            fileName = os.path.basename(att.attachment.path)

                            # Set whatever we got as a new attachment name. Also notice all images are referenced as
                            # "static/image.jpg" in Booktype so we have to change the source also.
                            e.set('src', 'static/%s' % fileName)


        content =  etree.tostring(tree, encoding='UTF-8', method='html')

        # Create new chapter. New chapter will be in "Hold chapters". If you want it to be in "Table of contents" you would
        # need to do some extra magic. But we don't care about it now. We also don't really care about writing anything to
        # log files...

        now = datetime.datetime.now()
        chapter = models.Chapter(book = book,
                                 version = book.version,
                                 url_title = bookiSlugify(chapterTitle),
                                 title = chapterTitle,
                                 status = stat,
                                 content = content,
                                 created = now,
                                 modified = now)
        chapter.save()
        

if __name__ == '__main__':
    # optparse just because i have python 2.6 on this machine

    usage = "usage: %prog [options] wordpress_expore_file"
    parser = OptionParser(usage)
    parser.add_option('-o', '--owner', dest='owner', metavar='OWNER', action="store", type="string", default="booktype", help="Owner of the book")
    parser.add_option('-t', '--title', dest='title', metavar='TITLE', action="store", type="string", help="New book title")
    parser.add_option('-u', '--url', dest='url', metavar='URL', action="store", type="string", help="New book url")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("You must specify a file name for Wordpress export")

    # parse the export file
    # don't really care about validation

    document = feedparser.parse(args[0])

    try:
        user = User.objects.get(username=options.owner)
    except User.DoesNotExist:
        print 'No such user %s' % options.owner
        sys.exit(-1)
        
    if options.title:
        bookTitle = options.title
        bookTitleURL = bookiSlugify(options.title)
    else:
        bookTitle = document['feed']['title']
        
    if options.url:
        bookTitleURL = options.url
    elif not options.title:
        bookTitleURL = bookiSlugify(document['feed']['title'])

    # So we don't spend best years of our lives waiting

    import socket
    socket.setdefaulttimeout(10)

    # Import the feed
    
    importFeed(document, {'user': user,
                          'bookTitle': bookTitle,
                          'bookTitleURL': bookTitleURL})
    
