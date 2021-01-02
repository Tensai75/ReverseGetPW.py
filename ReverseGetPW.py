#!/usr/bin/python3
##############################################################################
### NZBGET POST-PROCESSING SCRIPT                                          ###

# Reverse Get Password
#
#
# Renames the final destination directory to "title{{password}}" if a password was provided.
#
# This might be usefull in some special usecases where having the password in the name of the destination folder might be desired.
#
# NOTE: If you have other post-processing scripts running, this extension script should probably be the last post-processing script to run
#
#
# NOTE: This script requires Python 3.x to be installed on the system running NZBGet.

### NZBGET QUEUE SCRIPT                                                    ###
##############################################################################

import re
import sys
import os

password = os.environ.get('NZBPR_*Unpack:Password')
if (password):
    print('[INFO] Unpack password is set to: %s' %(password))
    if os.environ.get('NZBPP_FINALDIR'):
        directory = os.environ.get('NZBPP_FINALDIR')
    else:
        directory = os.environ.get('NZBPP_DIRECTORY')
    print('[INFO] Current destination directory is set to: %s' %(directory))
    pattern = re.compile("^.*\{\{" + re.escape(password) + "\}\}$")
    match = pattern.search(directory)
    if (not match):
        pattern = re.compile("[" + re.escape(':*/"?>|<') + "]")
        match = pattern.search(password)
        if (match):
            print('[ERROR] The password contains invalid characters! Cannot rename the destination directory.')
            sys.exit(94)
        else:
            newdirectory = directory + "{{" + password + "}}"
            try:
                print('[INFO] Renaming the destination directory to: %s' %(newdirectory))
                os.rename(directory, newdirectory)
                print('[NZB] DIRECTORY=%s' %(newdirectory))
                print('[NZB] FINALDIR=%s' %(newdirectory))
                print('[INFO] Destination directory sucessfully renamed to: %s' %(newdirectory))
                sys.exit(93)
            except Exception as e:
                print('[ERROR] Cannot rename directory "%s". Error: %s' %(directory, str(e)))
                sys.exit(94)
    else:
        print('[INFO] The destination directory already contains the password in currly braces. No rename required.')
else:
    print('[INFO] No unpack password was set. No rename required.')
sys.exit(95)
