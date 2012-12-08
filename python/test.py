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

  def setUp(self):
      self.bag = bagit.Bag('test-bar')
      self.profile = bagit_profile.Profile('https://raw.github.com/ruebot/bagit-profiles/master/bagProfileBar.json')
      self.retrieved_profile = self.profile.get_profile()
  
  def test_validate_bagit_profile_info(self):
    self.assertTrue(self.profile.validate_bagit_profile_info(self.retrieved_profile))

  def test_validate(self):
    self.assertTrue(self.profile.validate(self.bag))

  def test_validate_bag_info(self):
    self.assertTrue(self.profile.validate_bag_info(self.bag))

  def test_validate_manifests_required(self):
    self.assertTrue(self.profile.validate_manifests_required(self.bag))

  def test_validate_allow_fetch(self):
    self.assertTrue(self.profile.validate_allow_fetch(self.bag))

  def test_validate_accept_bagit_version(self):
    self.assertTrue(self.profile.validate_accept_bagit_version(self.bag))
    
  def test_validate_serialization(self):
    self.assertTrue(self.profile.validate_serialization(os.path.abspath("test-bar")))

if __name__ == '__main__':
  unittest.main()
