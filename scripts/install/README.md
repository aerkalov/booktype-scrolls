Booktype Easy Install v0.1
==========================

This script will help you install and setup Booktype. It will take care of known problems on different platforms and manage setup process for you. 

Tested on
---------
* Ubuntu 10.04
* Ubuntu 12.04
* CentOS 6.3
* Debian 6
* Mac OS X 10.5/10.6/10.8 [with Homebrew]

Start it
--------
Download the script and execute it. It will download and install required packages. When it is done it will tell you how to create user account and start Booktype. 

    wget https://raw.github.com/aerkalov/booktype-scrolls/master/scripts/install/booktype_install.py 
    python booktype_install.py

By default it will create _mybooktype_ directory (your user must have permissions to do so) in your current directory.

Arguments
---------
Get list of all the arguments:

    python booktype_install.py --help

Create it inside of "myproject" directory:

    python booktype_install.py -p myproject

Create it inside of "book" directory for "ubuntu" platform:

    python booktype_install.py -o ubuntu -p book

More info
---------
* http://www.binarni.net/2013/01/booktype-scrolls-ubuntu-installation/
* http://www.binarni.net/2012/07/booktype-easy-install/


Author
------

Aleksandar Erkalovic [http://www.binarni.net/](http://www.binarni.net/) [@aerkalov](http://twitter.com/aerkalov/)

Copyright © 2012 Aleksandar Erkalovic | GNU AFFERO GENERAL PUBLIC LICENSE

