#!/usr/bin/env python

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
my_profile.validate_serialization('mydir')

# Validate the profile.
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

    # @todo: Check self.profile['bag-profile-info'] to see if "Source-Organization", 
    # "External-Description", "Version" and "BagIt-Profile-Identifier" are defined. 
    # Errors here are fatal.
    def validate_bagit_profile_info(self, profile):
        pass

    # @todo: For each member of self.profile['bag_info'], if the member has a 'required'
    #  attribute, throw an exception if the member is not present in the bag's bag-info.txt
    # file. If the member has a 'values' attribute, throw an exception if the member's value
    # in bag-info.txt does not have one of the listed values.
    def validate_bag_info(self, bag):
        pass

    # @todo: For each member of self.profile['manifests_required'], throw an exception if 
    # the manifest file is not present.
    def validate_manifests_required(self, bag):
        pass

    # @todo: Check to see if this constraint is False, and if it is, then check to see
    # if the fetch.txt file exists. If it does, throw an exception.
    def validate_allow_fetch(self, bag):
        pass

    # Check the Bag's version, and if it's not in the list of allowed versions,
    # throw an exception.
    def validate_accept_bagit_version(self, bag):
        if bag.version not in self.profile['Accept-Bagit-Version']:
            raise ProfileValidationError("Bag version does is not in list of allowed values.")

    # Perform tests on 'Serialization' and 'Accept-Serialization', in one function.
    # Since the https://github.com/edsu/bagit only operates on unserialized Bags,
    # 1) we can't pass this function or the next the bag object (since it is always 
    # unserialized). Instead, pass them the path to the Bag, and 2) this method need
    # to be called before validate().
    def validate_serialization(self, path_to_bag):
        # First, perform the two negative tests.
        if self.profile['Serialization'] == 'required' and os.path.isdir(path_to_bag):
            raise ProfileValidationError("Bag serialization is required but Bag is a directory.")
            return False
        if self.profile['Serialization'] == 'forbidden' and os.path.isfile(path_to_bag):
            raise ProfileValidationError("Bag serialization is forbidden but Bag appears is a file.")
            return False

        # Then test to see whether the Bag is serialized (is a file) and whether the mimetype is one
        # of the allowed types.
        if self.profile['Serialization'] == 'required' or self.profile['Serialization'] == 'optional' and os.path.isfile(path_to_bag):
            bag_path, bag_file = os.path.split(path_to_bag)
            mtype = mimetypes.guess_type(bag_file)
            if mtype not in self.profile['Accept-Serialization']:
                raise ProfileValidationError("Bag serialization type is not in the list of allowed values.")
      
        # If we have passed the tests, return True.
        return True

