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

# Validate the profile.
my_profile.validate(bag)

"""
import sys
import json
import urllib

# For use during development.
import pprint
pp = pprint.PrettyPrinter(indent=4)

# Define an exceptin class for use within this module.
class ProfileValidationError(Exception):
  pass

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
  # which we've already called.
  def validate(self, bag):
    self.validate_bag_info(bag)
    self.validate_manifests_required(bag)
    self.validate_allow_fetch(bag)
    self.validate_serialization(bag)
    self.validate_accept_serialization(bag)
    self.validate_accept_bagit_version(bag)

  # @todo: Check self.profile['bag-profile-info'] to see if "Source-Organization", "External-Description", 
  # "Version" and "BagIt-Profile-Identifier" are defined. Errors here are fatal.
  def validate_bagit_profile_info(self, profile):
    # For debugging....
    pp.pprint(profile)

  # @todo: For each member of self.profile['bag_info'], if the member has a 'required' attribute, throw
  # an exception if the member is not present in the bag's bag-info.txt file. If the member
  # has a 'values' attribute, throw an exception if the member's value in bag-info.txt does
  # not have one of the listed values.
  def validate_bag_info(self, bag):
    pass

  # @todo: For each member of self.profile['manifests_required'], throw an exception if the manifest file
  # is not present.
  def validate_manifests_required(self, bag):
    pass

  # @todo: Check to see if this constraint is False, and if it is, then check to see
  # if the fetch.txt file exists. If it does, throw an exception.
  def validate_allow_fetch(self, bag):
    pass

  # @todo: Since the https://github.com/edsu/bagit only operates on unserialized Bags,
  # we can't use this and the next function with it. The script using our library needs
  # to check on its own.
  def validate_serialization(self, bag):
    pass

  def validate_accept_serialization(self, bag):
    pass

  # Check the Bag's version, and if it's not in the list of allowed versions,
  # throw an exception.
  def validate_accept_bagit_version(self, bag):
    if bag.version not in self.profile['Accept-Bagit-Version']:
      raise ProfileValidationError("Bag version does is not in list of allowed values.")
