# Bagit Profile

[![Build Status](https://secure.travis-ci.org/ruebot/bagit-profiles.png)](http://travis-ci.org/ruebot/bagit-profiles)

### Description

A simple Python module for validating BagIt profiles. See the [BagIt Profiles Specification (draft)](https://github.com/ruebot/bagit-profiles/blob/master/README.md) for more information.

This module is intended for use with [bagit](https://github.com/edsu/bagit) but does not extend it.

### Installation

bagit_profile.py is a single-file python module that you can drop into your project as needed or you can install globally with:

`git clone https://github.com/ruebot/bagit-profiles.git`
`cd bagit-profiles/python`
`sudo python setup.py install`

### Usage

```python
import bagit
import bagit_profile
```

Instantiate an existing Bag using [bagit](https://github.com/edsu/bagit).
`bag = bagit.Bag('mydir')`

Instantiate a profile, supplying its URI.
`my_profile = bagit_profile.Profile('http://example.com/bagitprofile.json')`

Validate 'Serialization' and 'Accept-Serialization'. This must be done before .validate(bag) is called. 'mydir' is the path to the Bag.

```python
if my_profile.validate_serialization('mydir'):
      print "Serialization validates"
      else:
            print "Serialization does not validate"
```

Validate the rest of the profile.

```python
if my_profile.validate(bag):
      print "Validates"
      else:
            print "Does not validate"
```

Or from the commandline:

`bagit.py 'http://uri.for.profile/profile.json' path/to/bag`

### Test suite

`python test.py`

### Development

1. [Fork the repository](https://help.github.com/articles/fork-a-repo)
2. Do something awesome!
3. [Submit a pull request](https://help.github.com/articles/creating-a-pull-request) explianing what your plugin does

### License

![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")
