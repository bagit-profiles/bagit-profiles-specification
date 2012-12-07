import os
import shutil
import logging
import datetime
import tempfile
import unittest

from os.path import join as j

import bagit_profile

class Test_bag_profile(unittest.TestCase):

  # Instantiate an existing Bag using https://github.com/edsu/bagit.
  bag = bagit.Bag('test-bar')

  # Instantiate a profile, supplying its URI.
  my_profile = bagit_profile.Profile('https://raw.github.com/ruebot/bagit-profiles/refactor/cli-and-module/bagProfileBar.json')

  # Validate 'Serialization' and 'Accept-Serialization'. This must be done 
  # before .validate(bag) is called. 'mydir' is the path to the Bag.
  
  def test_serialization():
    assertTrue(my_profile.validate_serialization('test-bar'))

  #validate the rest of the profile/
  def test_bag_validation():
    assertTrue(my_profile.validate(bag))
