#!/usr/bin/env python2

# Install ArchLinux AUR packages
# Author: Quoc Vu


DOCUMENTATION = '''
---
module: AUR
short_description: install AUR packages
'''

EXAMPLES = '''
- aur: name=gnome
'''

import json
import subprocess
import urllib
import tarfile

from ansible.module_utils.basic import *


def download(package_name):
    uri = 'https://aur.archlinux.org/cgit/aur.git/snapshot/%s.tar.gz' % (package_name)
    temp_file = '/tmp/%s.tar.gz' % (package_name)
    urllib.urlretrieve(uri, temp_file)

def unpack(package_name):
    temp_file = '/tmp/%s.tar.gz' % (package_name)
    temp_dir = '/tmp/%s' % (package_name)
    tar = tarfile.open(temp_file, "r:gz")
    tar.extractall()
    tar.close()

def install(package_name):
    temp_dir = '/tmp/%s' % (package_name)
    result = subprocess.check_output(['makepkg', '-s,' '-i', '--noconfirm'], cwd=temp_dir, shell=True)


def main():

    module = AnsibleModule(
        argument_spec = {
            'name': { 'required': True },
        },
        supports_check_mode = True,
    )

    params = module.params
    package_name = module.params['name']


    if not module.check_mode:
        download(package_name)
        unpack(package_name)
        install(package_name)

    module.exit_json()


if __name__ == '__main__':
    main()
