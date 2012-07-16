Install
=======



Wiki page:
* https://github.com/aerkalov/booktype-scrolls/wiki/Booktype-Easy-Install

Tested on
---------
* Ubuntu 10.04
* Ubuntu 12.04
* CentOS 6.3
* Debian 6

Start it
--------
Download the script and execute it. It will download and install required packages. When it is done it will tell you how to create user account and start Booktype. You don’t need to be root to start this install script but you do need sudo permissions in case it must install some system packages. You will need to confirm installation of new packages and you will be informed which commands are being executed in the background. Without your permission new packages will not be installed on the system. Feel free to analyze the script before you start it.

    wget https://raw.github.com/aerkalov/booktype-scrolls/master/scripts/install/booktype_install.py 
    python booktype_install.py

Arguments
---------
Get list of all the arguments:

    python booktype_install.py --help

Create it inside of "myproject" directory:

    python booktype_install.py -p myproject

Create it inside of "book" directory for "ubuntu" platform:

    python booktype_install.py -o ubuntu -p book


Author
------

Aleksandar Erkalovic [http://www.binarni.net/](http://www.binarni.net/) [@aerkalov](http://twitter.com/aerkalov/)

Copyright © 2012 Aleksandar Erkalovic | GNU AFFERO GENERAL PUBLIC LICENSE

