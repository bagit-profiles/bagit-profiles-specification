import os
import shutil
import logging
import datetime
import tempfile
import unittest
import bagit

from os.path import join as j

import bagit_profile

class Test_bag_profile(unittest.TestCase):
  
  def test_validate_bagit_profile_info(self):
    self.profile = bagit_profile.Profile('https://raw.github.com/ruebot/bagit-profiles/master/bagProfileBar.json')
    self.assertTrue(bagit_profile.Profile.validate_bagit_profile_info)  

  def test_validate(self):
    self.bag = bagit.Bag('test-bar')
    self.profile = bagit_profile.Profile('https://raw.github.com/ruebot/bagit-profiles/master/bagProfileBar.json')
    self.assertTrue(bagit_profile.Profile.validate)

  def test_validate_bag_info(self):
    self.bag = bagit.Bag('test-bar')
    self.profile = bagit_profile.Profile('https://raw.github.com/ruebot/bagit-profiles/master/bagProfileBar.json')
    self.assertTrue(bagit_profile.Profile.validate_bag_info)

  def test_validate_manifests_required(self):
    self.bag = bagit.Bag('test-bar')
    self.profile = bagit_profile.Profile('https://raw.github.com/ruebot/bagit-profiles/master/bagProfileBar.json')
    self.assertTrue(bagit_profile.Profile.validate_manifests_required)

  def test_validate_allow_fetch(self):
    bag = bagit.Bag('test-bar')
    profile = bagit_profile.Profile('https://raw.github.com/ruebot/bagit-profiles/master/bagProfileBar.json')
    self.assertTrue(bagit_profile.Profile.validate_allow_fetch)

  def test_validate_accept_bagit_version(self):
    bag = bagit.Bag('test-bar')
    profile = bagit_profile.Profile('https://raw.github.com/ruebot/bagit-profiles/master/bagProfileBar.json')
    self.assertTrue(bagit_profile.Profile.validate_accept_bagit_version)
    
  def test_validate_serialization(self):
    bag = bagit.Bag('test-bar')
    profile = bagit_profile.Profile('https://raw.github.com/ruebot/bagit-profiles/master/bagProfileBar.json')
    self.assertTrue(bagit_profile.Profile.validate_accept_bagit_version)

if __name__ == '__main__':
  unittest.main()
