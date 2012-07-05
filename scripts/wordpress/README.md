Wordpress
=========

Imports wordpress export as a Booktype book. It will import published Wordpress posts and download _all_ images referenced as <img> tag in the post. 
This is just an example of how this could be done and is missing some functionality at the moment. 

Start it
--------

You must load environment variables for your Booktype project first! If you don't have your own
Wordpress export you can use example file "posts.xml" (i downloaded it from here http://wpcandy.com/made/the-sample-post-collection)


```wordpress_import.py --help
wordpress_import.py -o aerkalov posts.xml
wordpress_import.py -o aerkalov -t "My Wordpress book" posts.xml
wordpress_import.py -u "wordpressbook" posts.xml```


Author
------

Aleksandar Erkalovic [http://www.binarni.net/](http://www.binarni.net/) [@aerkalov](http://twitter.com/aerkalov/)

Copyright © 2012 Aleksandar Erkalovic | GNU AFFERO GENERAL PUBLIC LICENSE


