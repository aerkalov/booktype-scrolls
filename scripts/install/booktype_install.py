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

from optparse import OptionParser
import os
import sys
import subprocess

platform = None

projectDir = 'mybooktype'

PACKAGES = {'debian': ['python', 'python-dev', 'sqlite3', 'git-core',
                       'python-pip', 'python-virtualenv',
                       'redis-server', 'libxml2-dev', 'libxslt-dev'],
            'ubuntu': ['python', 'python-dev', 'sqlite3', 'git-core',
                       'python-pip', 'python-virtualenv',
                       'libjpeg-dev', 'zlib1g-dev',
                       'redis-server', 'libxml2-dev', 'libxslt-dev'],
            'centos': ['python', 'python-devel', 'sqlite', 'git',
                       'python-virtualenv', 'python-pip', 'redis',
                       'libxml2-devel', 'libxslt-devel',
                       'libjpeg', 'libjpeg-devel', 'zlib', 'zlib-devel']
           }

COLOR = {'green': '32',
         'red': '31',
         'yellow': '33',
         'blue': '34',
         'white': '37',
         'magenta': '35',
         'cyan': '36',
         'crimson': '38', 
         'gray': '30'}

def fmt(s, color="gray", bold = False):
    if not sys.stdout.isatty():
        return s

    attr = [COLOR.get(color, 'gray')]

    if bold:
        attr.append('1')

    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), s)


def showIntro():
    s = """     _______
    /      /,   Booktype Easy Install v0.0.1 
   /      //          
  /______//     https://github.com/aerkalov/booktype-scrolls
 (______(/         
   """ 
    print s


def showNotSupported():
    print fmt("\n[ERROR] I am sorry but your platform is not supported at the moment.", 'red')
    print fmt("""[SUPPORTED] It has been tested on:
              * Ubuntu 10.04
              * Ubuntu 12.04
              * CentOS 6.3
              * Debian 6\n""", "yellow")

def _ubuntuPackageInstalled(packageName):
    ret = subprocess.call('dpkg-query -s %s 1>/dev/null 2>/dev/null' % packageName, shell=True)
    return ret


def _debianPackageInstalled(packageName):
    ret = subprocess.call('dpkg-query -s %s 1>/dev/null 2>/dev/null' % packageName, shell=True)
    return ret

def _debianInstallPackages(packages):
    print "Your system is missing couple of required packages. Let's install them!", 

    command = 'sudo apt-get install %s' % ' '.join(needToInstall)

    print fmt('\n$ ' + command + '\n', 'blue')
    ret = subprocess.call(command, shell=True)

    return ret

def _debianCheckManually(packages):
    if 'python-pip' in packages:
        ret = subprocess.call('pip 1>/dev/null 2>/dev/null', shell=True)
        if ret == 2:
            packages.remove('python-pip')
            
    if 'python-virtualenv' in packages:
        ret = subprocess.call('virtualenv 1>/dev/null 2>/dev/null', shell=True)
        if ret == 2:
            packages.remove('python-virtualenv')

    return packages

def _debianCheckPrerequisite():
    ret = subprocess.call('gcc 1>/dev/null 2>/dev/null', shell=True)
    if ret == 127:
        print fmt("\n[ERROR] Looks like you don't have developement tools installed. Install them and try again.", "red", True)
        print fmt("[HOW TO FIX] sudo apt-get install build-essential", "yellow")
        sys.exit(1)


def _centosPackageInstalled(packageName):
    ret = subprocess.call('rpm -q %s 1>/dev/null 2>/dev/null' % packageName, shell=True)
    return ret

def _centosInstallPackages(packages):
    print "Your system is missing couple of required packages. Let's install them!", 

    command = "su -c 'yum -y install %s'" % ' '.join(needToInstall)

    print fmt('\n$ ' + command + '\n', 'blue')
    ret = subprocess.call(command, shell=True)

    return ret

def _centosCheckManually(packages):
    if 'python-pip' in packages:
        ret = subprocess.call('pip 1>/dev/null 2>/dev/null', shell=True)
        if ret == 2:
            packages.remove('python-pip')
            
    if 'python-virtualenv' in packages:
        ret = subprocess.call('virtualenv 1>/dev/null 2>/dev/null', shell=True)
        if ret == 2:
            packages.remove('python-virtualenv')

    return packages


def _centosCheckPrerequisite():
    # check if EPEL installed
    ret = subprocess.call('rpm -q epel-release 1>/dev/null 2>/dev/null', shell=True)
    if ret != 0:
        print fmt("\n[ERROR] You must add EPEL repository! Add and try again.", "red")
        print fmt("[HOW TO FIX] For CentOS 6.x:", "yellow")
        print fmt("                su -c 'rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-7.noarch.rpm'", "yellow")
        sys.exit(1)

    # check if gcc installed
    ret = subprocess.call('gcc 1>/dev/null 2>/dev/null', shell=True)
    if ret == 127:
        print fmt("\n[ERROR] Looks like you don't have developement tools installed. Install them and try again.", "red", True)
        print fmt("[HOW TO FIX] su -c 'yum groupinstall \"Development Tools\"'", "yellow")
        sys.exit(1)

CALLBACKS = {'debian': {'package_installed': _debianPackageInstalled,
                        'install_packages': _debianInstallPackages,
                        'check_if_manually': _debianCheckManually,
                        'check_prerequisite': _debianCheckPrerequisite
                       },

             'ubuntu': {'package_installed': _ubuntuPackageInstalled,
                        'install_packages': _debianInstallPackages,
                        'check_if_manually': _debianCheckManually,
                        'check_prerequisite': _debianCheckPrerequisite
                       },


             'centos': {'package_installed': _centosPackageInstalled,
                        'install_packages': _centosInstallPackages,
                        'check_if_manually': _centosCheckManually,
                        'check_prerequisite': _centosCheckPrerequisite
                       }
            }

def getDistribution():
    # Check if this is Debian based system
    try:
        p = subprocess.Popen("lsb_release -i", shell=True, 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        dist = p.stdout.read()

        if 'Ubuntu' in dist:
            return 'ubuntu'

        if 'Debian' in dist:
            return 'debian'
    except OSError:
        pass

    # Check if we are centos
    ret = subprocess.call('rpm -q centos-release 1>/dev/null 2>/dev/null', shell=True)

    if ret == 0:
        return 'centos'

    return None

if __name__ == '__main__':
    usage = "usage: %prog [options]"

    parser = OptionParser(usage)
    parser.add_option('-p', '--project', dest='project', metavar='PROJECT', action="store", type="string", help="Project name")
    parser.add_option('-o', '--os', dest='platform', metavar='OS', action="store", type="string", help="OS platform (ubuntu, debian, centos, ...)")

    (options, args) = parser.parse_args()

    showIntro()

    if options.project:
        projectDir = options.project

    if options.platform:
        platform = options.platform
    else:
        platform = getDistribution()

    if not platform:
        showNotSupported()
        sys.exit(1)

    CALLBACKS[platform]['check_prerequisite']()

    needToInstall = filter(CALLBACKS[platform]['package_installed'], PACKAGES[platform])

    needToInstall = CALLBACKS[platform]['check_if_manually'](needToInstall)

    if len(needToInstall) > 0:
        ret = CALLBACKS[platform]['install_packages'](needToInstall)

        if ret != 0:
            print fmt("\n[ERROR] Could not install packages.\n")
            if platform == "centos":
                print fmt("[INFO] Do you have EPAL repository installed?", "yellow")
            sys.exit(1)

    if os.path.exists(projectDir):
        print fmt("\n[WARNING] You have already installed Booktype in this directory!", "red", True)
        print fmt("[WHAT TO DO] Remove directory '%s', install it at another location or choose a different project name..\n" % projectDir, "yellow")
        sys.exit(1)

    command = 'virtualenv %s' % projectDir
    print fmt('\n$ ' + command + '\n', 'blue')
    ret = subprocess.call(command, shell=True)
    if ret != 0:
        print fmt("\n[ERROR] Could not install virtual environment!", "red", True)
        print fmt("[WHAT TO DO] Check your virtualenv installation and try again.\n", "yellow")
        sys.exit(1)

    if platform in ['debian', 'ubuntu']:
        command = '. %s/bin/activate && pip install Django==1.3 South==0.7.5 unidecode lxml PIL' % projectDir
    else:
        command = '. %s/bin/activate && pip install Django==1.3 South==0.7.5 unidecode lxml PIL' % projectDir

    print fmt('\n$ ' + command +'\n', 'blue')
    ret = subprocess.call(command, shell=True)
    if ret != 0:
        print fmt("\n[ERROR] Could not install Python modules!\n", "red", True)
        sys.exit(1)

    command = 'cd %s && git clone https://github.com/sourcefabric/Booktype.git' % projectDir
    print fmt('\n$ ' + command +'\n', 'blue')
    ret = subprocess.call(command, shell=True)
    if ret != 0:
        print fmt("\n[ERROR] Could not download Booktype!\n", "red", True)
        sys.exit(1)

    command = '. %(project)s/bin/activate && %(project)s/Booktype/scripts/createbooki --database sqlite ./%(project)s/mybook/' % {'project': projectDir}
    print fmt('\n$ ' + command +'\n', 'blue')
    ret = subprocess.call(command, shell=True)
    if ret != 0:
        print fmt("\n[ERROR] Could not create Booktype project!\n", "red", True)
        sys.exit(1)

    script = '''. %(project)s/bin/activate
. %(project)s/mybook/booki.env
django-admin.py syncdb --noinput
django-admin.py migrate
''' % {'project': projectDir}

    try:
        file('%s/tmp.sh' % projectDir, 'w').write(script)
    except:
        print fmt("\n[ERROR] Could not write to a file!", "red")
        print fmt("[WHAT TO DO] Check permissions on '%s' directory. Check if your disk is full.\n" % projectDir, "yellow")
        sys.exit(1)

    command = 'sh %s/tmp.sh' % projectDir
    ret = subprocess.call(command, shell=True)
    os.remove('%s/tmp.sh' % projectDir)

    workingDir = os.getcwd()

    script = '''#!/usr/bin/env bash

. %(cwd)s/%(project)s/bin/activate
. %(cwd)s/%(project)s/mybook/booki.env

django-admin.py runserver 0.0.0.0:%(port)d
''' % {'cwd': workingDir, 'project': projectDir, 'port': 8080}

    try:
        file('%s/start.sh' % projectDir, 'w').write(script)
    except:
        print fmt("\n[ERROR] Could not write to a file!", "red")
        print fmt("[WHAT TO DO] Check permissions on '%s' directory. Check if your disk is full.\n" % projectDir, "yellow")
        sys.exit(1)


    script = '''#!/usr/bin/env bash

. %(cwd)s/%(project)s/bin/activate
. %(cwd)s/%(project)s/mybook/booki.env

django-admin.py createsuperuser
echo "---------------------------------------------------------"
echo "Use this command to start Booktype:"
echo "   %(project)s/start.sh"
echo "---------------------------------------------------------"
''' % {'cwd': workingDir, 'project': projectDir}

    try:
        file('%s/create.sh' % projectDir, 'w').write(script)
    except:
        print fmt("\n[ERROR] Could not write to a file!", "red")
        print fmt("[WHAT TO DO] Check permissions on '%s' directory. Check if your disk is full.\n" % projectDir, "yellow")
        sys.exit(1)

    ret = subprocess.call('chmod u+x %s/start.sh %s/create.sh' % (projectDir, projectDir), shell=True)
    if ret != 0:
        print fmt("\n[ERROR] Could not set permissions on start file", "red")
        print fmt("[WHAT TO DO] chmod u+x %s/start.sh" % projectDir, shell=True) 


    print fmt("Booktype has been installed in '%s' directory. We need to create superuser now. Please start this command:" % projectDir, "yellow")
    print fmt("     %s/create.sh\n" % projectDir, "blue")

