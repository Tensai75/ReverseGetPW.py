#!/usr/bin/python2.7
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
# NOTE: This script requires Python to be installed on the system running NZBGet.

### NZBGET QUEUE SCRIPT                                                    ###
##############################################################################

import re
import sys
import os

# errorHandler function
def errorHandler(m, e):
    print '[ERROR] %s. Error: %s'%(m, e)
    sys.exit(94)


if os.environ.get('NZBPP_FINALDIR'):
    directory = os.environ.get('NZBPP_FINALDIR')
else:
    directory = os.environ.get('NZBPP_DIRECTORY')
password = os.environ.get('NZBPR_*Unpack:Password')
if (directory and password):
    pattern = re.compile("^.*\{\{" + re.escape(password) + "\}\}$")
    match = pattern.search(directory)
    if (not match):
        newdirectory = directory + "{{" + password + "}}"
        try:
            os.rename(directory, newdirectory)
        except Exception, e:
            errorHandler('Cannot rename directory ' + directory, str(e))
        print '[NZB] DIRECTORY=' + newdirectory
        print '[NZB] FINALDIR=' + newdirectory
sys.exit(93)
