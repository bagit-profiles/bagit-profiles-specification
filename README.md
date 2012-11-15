Bagit Spec update - Profiles
===

Collaborators
---

Meghan Currie, Krista Godfrey, Mark Jordan, Nick Ruest, William Wueppelmann; special advisor Dan Chudnov.


bagitProfile
---

Allow creators and consumers of bags to agree on which optional and required components of the bags they are exchanging. The profile file (bagProfile.json), which is machine readable, sits at a valid url. The format of the file will be json.

This proposal builds on the sample profile in cluded in the Library of Congress Bagger tool. That profile was local to LC and not intended to be implemented widely. 

Intended workflow: Receive bag, complete bag if fetch.txt is present, validate the complete Bag against a profile, validate Bag according to Bag spec. 

Some profile attributes are 'fatal': failure to validate accept-serialization or accept-version implies that the rest of the bag is unverifiable and processing should stop. Processing may continue after other errors in order to generate a comprehensive error report.

Tests:

1. bag-info:
Specifies which tags are required, etc. Assumes presence of bag-info.txt. Each tag definition takes two optional parameters: required is true or false (default false) and indicates whether or not this tag is required. values is a list of acceptable values. If empty, any value is accepted.

bag-info.txt must contain the tag 'Bag-Profile', with a value of the URI of the JSON file containing the profile.

2. manifests-required: LIST
Each manifest file in LIST is required.

3. allow-fetch.txt: true|false
A fetch.txt file is allowed within the bag. Default: true

4. serialization: forbidden|required|optional
Allow, forbid or require serialization of bags. Default is optional.

5. accept-serialization: LIST
A list of MIME types acceptable as serialized formats. E.g. "application/zip". If serialization has a value of required or optional, at least one value is needed. If serialization is forbidden, this has no meaning.

6. accept-version: LIST
A list of Bagit version numbers that will be accepted. At least one version is required.


Examples
---

bagProfileFoo.json

    "bag-info.txt": {
    "bagging-date": {
      required: "true",
     },
    "source-organization" : {
      required: "true",
      values: [ "Simon Fraser University", "York Univeristy" ]
     },
    "contact-phone": {
      required: "true"
    },
    },
    "manifests-required" : [ "md5" ],
    "allow-fetch.txt" : "false",
    "serialization" : "required",
    "accept-serialization" : [ "application/zip", "application/tar" ],
    "accept-version" : [ "0.96", "0.97" ],


bagProfileBar.json

    bagProfile: {
      bag-info.txt: {
      "Source-Organization": {
        "required": "true"
         "values": "Simon Fraser University", "York University"
      },
      "Organization-Address": {
        "required": "true"
        "values": "8888 University Drive Burnaby, B.C. V5A 1S6 Canada", "4700 Keele Street Toronto, Ontario M3J 1P3 Canada"
      },
      "Contact-Name": {
        "required": "true"
        "values": "Mark Jordan", "Nick Ruest"
      },
      "Contact-Phone": {
        "required": "false"
      },
      "Contact-Email": {
        "required": "true"
      },
      "External-Description": {
        "required": "true"
      },
      "External-Identifier": {
        "required": "false"
      },
      "Bag-Size": {
        "required": "true"
      },
          
      "Bag-Group-Identifier: {
        "required": "false"
      },
      "Bag-Count": {
        "required": "true"
      },
      "Internal-Sender-Identifier": {
        "required": "false"
      },
      "Internal-Sender-Description": {
        "required": "false"
      },
      "Bagging Date: {
        "required": "true"
        "yyyy-mm-dd"
      },
      "Payload-Oxum: {
        "required": "true"
      },
    },
    
    bagit.txt: {
      "required": "true"
    },
    manifest-required”:  [ "md5" ], {
      "allow-fetch.txt" : "false",
      "serialization" : "required",
      "accept-serialization" : [ "application/zip", "application/tar" ],
      "accept-version" : [ "0.96", "0.97" ],
    },
  }
