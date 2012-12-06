import bagit
import bagit_profile

# Instantiate an existing Bag using https://github.com/edsu/bagit.
bag = bagit.Bag('test-bar')

# Instantiate a profile, supplying its URI.
my_profile = bagit_profile.Profile('https://raw.github.com/ruebot/bagit-profiles/refactor/cli-and-module/bagProfileBar.json')

# Validate 'Serialization' and 'Accept-Serialization'. This must be done 
# before .validate(bag) is called. 'mydir' is the path to the Bag.
if my_profile.validate_serialization('test-bar'):
    print "Serialization validates"
else:
    print "Serialization does not validate"

# Validate the rest of the profile.
if my_profile.validate(bag):
    print "Validates"
else:
    print "Does not validate"

