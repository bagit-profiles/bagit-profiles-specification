#!/usr/bin/env python

# @todo: Improve exception handling so non-fatal exceptions do not kill script.

"""
A simple Python module for validating BagIt profiles. See https://github.com/ruebot/bagit-profiles
for more information.

This module is intended for use with https://github.com/edsu/bagit but does not extend it.

Usage:

import bagit
import bagit_profile

# Instantiate an existing Bag using https://github.com/edsu/bagit.
bag = bagit.Bag('mydir')

# Instantiate a profile, supplying its URI.
my_profile = bagit_profile.Profile('http://example.com/bagitprofile.json')

# Validate 'Serialization' and 'Accept-Serialization'. This must be done 
# before .validate(bag) is called. 'mydir' is the path to the Bag.
if my_profile.validate_serialization('mydir'):
    print "Serialization validates"
else:
    print "Serialization does not validate"

# Validate the rest of the profile.
if my_profile.validate(bag):
    print "Validates"
else:
    print "Does not validate"

"""
import os
import sys
import json
import urllib
import mimetypes
import logging
import optparse

# Define an exceptin class for use within this module.
class ProfileValidationError(Exception):
    pass

# Define the Profile class.
class Profile(object):
    def __init__(self, url):
        self.url = url
        self.get_profile()

    def get_profile(self):
        try:
            f = urllib.urlopen(self.url)
            profile = f.read()
            profile = json.loads(profile)
            self.profile = profile
        except:
            print "Cannot retrieve profile from", self.url
            logging.error("Cannot retrieve profile from" + self.url)
            # This is a fatal error.
            sys.exit(1) 

        self.validate_bagit_profile_info(profile)
        return self.profile

    # Call all the validate functions other than validate_bagit_profile_info(),
    # which we've already called. 'Serialization' and 'Accept-Serialization'
    #  are validated in validate_serialization().
def validate(self, bag):
    self.validate_bag_info(bag)
    self.validate_manifests_required(bag)
    self.validate_allow_fetch(bag)
    self.validate_accept_bagit_version(bag)
    return True

    # Check self.profile['bag-profile-info'] to see if "Source-Organization", 
    # "External-Description", "Version" and "BagIt-Profile-Identifier" are present. 
    # Errors here are fatal.
    def validate_bagit_profile_info(self, profile):
        if 'Source-Organization' not in profile['BagIt-Profile-Info']:
            raise ProfileValidationError("Required 'Source-Organization' tag is not in 'BagIt-Profile-Info'.")
            logging.error(profile + "Required 'Source-Organization' tag is not in 'BagIt-Profile-Info'." + '\n')
        if 'Version' not in profile['BagIt-Profile-Info']:
            raise ProfileValidationError("Required 'Version' tag is not in 'BagIt-Profile-Info'.")
            logging.error(profile + "Required 'Version' tag is not in 'BagIt-Profile-Info'." + '\n')
        if 'BagIt-Profile-Identifier' not in profile['BagIt-Profile-Info']:
            raise ProfileValidationError("Required 'BagIt-Profile-Identifier' tag is not in 'BagIt-Profile-Info'.")
            logging.error(profile + "Required 'BagIt-Profile-Identifier' tag is not in 'BagIt-Profile-Info'." + '\n')

    # Validate tags in self.profile['Bag-Info']. Profile data for this constrain looks like:
    # u'Bag-Info': {   u'Bagging-Date': {   u'required': True},
    #                 u'Contact-Phone': {   u'required': True},
    #                 u'Source-Organization': {   u'required': True,
    #                                             u'values': [   u'Simon Fraser University',
    #                                                            u'York University']}},
    def validate_bag_info(self, bag):
        # First, check for the required 'BagIt-Profile-Identifier' tag and ensure it has the same value
        # as self.url.
        if 'BagIt-Profile-Identifier' not in bag.info:
            raise ProfileValidationError("Required 'BagIt-Profile-Identifier' tag is not in bag-info.txt.")
            logging.error(bag + "Required 'BagIt-Profile-Identifier' tag is not in bag-info.txt." + '\n') 
        else:
            if bag.info['BagIt-Profile-Identifier'] != self.url:
                raise ProfileValidationError("'BagIt-Profile-Identifier' tag does not contain this profile's URI.")
                logging.error(bag + "'BagIt-Profile-Identifier' tag does not contain this profile's URI." + '\n')
        # Then, iterate through self.profile['Bag-Info'] and if a key has a dict containing a 'required' key that is
        # True, check to see if that key exists in bag.info. 
        for tag in self.profile['Bag-Info']:
            config = self.profile['Bag-Info'][tag]
            if 'required' in config and config['required'] is True: 
                if tag not in bag.info:
                    raise ProfileValidationError("Required tag '%s' is not present in bag-info.txt." + tag)
                    logging.error(bag + "Required tag '%s' is not present in bag-info.txt." + tag + '\n')
                # If the tag is in bag-info.txt, check to see if the value is constrained.
                else:
                    if 'values' in config: 
                        if bag.info[tag] not in config['values']:
                            raise ProfileValidationError("Required tag '%s' is present in bag-info.txt but does not have an allowed value ('%s')." % (tag, bag.info[tag]))
                            logging.error(bag + "Required tag '%s' is present in bag-info.txt but does not have an allowed value ('%s')." + tag + bag.info[tag] + '\n')

    # For each member of self.profile['manifests_required'], throw an exception if 
    # the manifest file is not present.
    def validate_manifests_required(self, bag):
        for manifest_type in self.profile['Manifests-Required']:
            path_to_manifest = os.path.join(bag.path, 'manifest-' + manifest_type + '.txt')
            if not os.path.exists(path_to_manifest):
                raise ProfileValidationError("Required manifest type '%s' is not present in Bag." + manifest_type)
                logging.error(bag + "Required manifest type '%s' is not present in Bag." +  manifest_type + '\n')

    # Check to see if this constraint is False, and if it is, then check to see
    # if the fetch.txt file exists. If it does, throw an exception.
    def validate_allow_fetch(self, bag):
        if self.profile['Allow-Fetch.txt'] is False: 
            path_to_fetchtxt = os.path.join(bag.path, 'fetch.txt')
            if os.path.exists(path_to_fetchtxt):
                raise ProfileValidationError("Fetch.txt is present but is not allowed.")
                logging.error(bag + "Fetch.txt is present but is not allowed." + '\n')

    # Check the Bag's version, and if it's not in the list of allowed versions,
    # throw an exception.
    def validate_accept_bagit_version(self, bag):
        if bag.version not in self.profile['Accept-Bagit-Version']:
            raise ProfileValidationError("Bag version does is not in list of allowed values.")
            logging.error(bag + "Bag version does is not in list of allowed values." + '\n')

    # Perform tests on 'Serialization' and 'Accept-Serialization', in one function.
    # Since the https://github.com/edsu/bagit only operates on unserialized Bags,
    # 1) we can't pass this function or the next the bag object (since it is always 
    # unserialized). Instead, pass them the path to the Bag, and 2) this method need
    # to be called before validate().
    def validate_serialization(self, path_to_bag):
        # First, perform the two negative tests.
        if self.profile['Serialization'] == 'required' and os.path.isdir(path_to_bag):
            raise ProfileValidationError("Bag serialization is required but Bag is a directory.")
            logging.error(path_to_bag + "Bag serialization is required but Bag is a directory." + '\n')
            return False
        if self.profile['Serialization'] == 'forbidden' and os.path.isfile(path_to_bag):
            raise ProfileValidationError("Bag serialization is forbidden but Bag appears is a file.")
            logging.error(path_to_bag + "Bag serialization is forbidden but Bag appears is a file." + '\n')
            return False

        # Then test to see whether the Bag is serialized (is a file) and whether the mimetype is one
        # of the allowed types.
        if self.profile['Serialization'] == 'required' or self.profile['Serialization'] == 'optional' and os.path.isfile(path_to_bag):
            bag_path, bag_file = os.path.split(path_to_bag)
            mtype = mimetypes.guess_type(bag_file)
            if mtype not in self.profile['Accept-Serialization']:
                raise ProfileValidationError("Bag serialization type is not in the list of allowed values.")
                logging.error(path_to_bag + "Bag serialization is forbidden but Bag appears is a file." + '\n')
      
        # If we have passed the serialization tests, return True.
        return True

# command line program

class BagitProfileOptionParser(optparse.OptionParser):
  def __init__(self, *args, **opts):
    optparse.OptionParser.__init__(self, *args, **opts)

def _make_opt_parser():
  parser = BagitProfileOptionParser(usage='usage: %prog [options] BagitProfile bagDir1 bagDir2 ...')
  parser.add_option('--quiet', action='store_true', dest='quiet')
  parser.add_option('--log', action='store', dest='log')

  return parser

def _configure_logging(opts):
  log_format="%(asctime)s - %(levelname)s - %(message)s"
  if opts.quiet:
    level = logging.ERROR
  else:
    level = logging.INFO
  if opts.log:
    logFile = os.path.join(opts.log + '/logs', 'BagitProfile' + time.strfime('%y_%m_%d') + '.log')
    logging.basicConfig(filename=logFile, level=level, format=log_format)
  if not opts.log:
    logging.basicConfig(filename='BagitProfile' + time.strfime('%y_%m_%d') + '.log', level=level, format=log_format)
  else:
    logging.basicConfig(level=level, format=log_format)

if __name__ == '__main__':
  opt_parser = _make_opt_parser()
  opts, args = opt_parser.parse_args()
  _configure_logging(opts)
  log = logging.getLogger()

  rc = 0
  
  validate()
  #sys.exit(rc)
