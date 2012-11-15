BagIt Profiles Specification (DRAFT in progress)
===

Collaborators
---
This draft originally created by members of the Access 2012 Hackfest group: Meghan Currie, Krista Godfrey, Mark Jordan, Nick Ruest, William Wueppelmann, and Dan Chudnov.

Purpose and background
---

The purpose of the BagIt Profiles Specification is to allow creators and consumers of Bags to agree on which optional components of the bags they are exchanging. Details of the profile are instantiated in a JSON file that both the producing and consuming applications interpret using the conventions described below. The profile file sits at an HTTP URI (e.g., http://foo.example.com/bagitprofiles/profile-bar.json), and can therefore be read by any number of applications creating or consuming Bags:

                        BagIt Profile JSON file
                                        /       ^
                                       v         \
                        Bag creating app 1  -->  Bag consuming app
                        Bag creating app 2


				BagIt Profile JSON file
					/       ^
				       v         \		
			Bag creating app 1  -->  Bag consuming app
			Bag creating app 2


This proposed Specification builds on the sample profile included in the Library of Congress Bagger tool. However, that profile was local to LC and not intended to be implemented widely. The proposed Specification is intended to be an optional extension to the cannonical BagIt spec, and in no way modifies that specification.

Use cases for BagIt profiles include distributed mass production of Bags, repository or application-specific content ingestion via Bags (e.g. SWORD, Archivematica), and Preservation-as-a-Service.

The intended workflow for using a BagIt profile is: 

1. The application creating the Bags ensures that Bags it produces meet all of the constraints expressed in the agreed-upon profile file.

2. The application consuming these Bags retrieves the profile file from its URI and validates incoming Bags against it; specifically, it must complete the Bag if fetch.txt is present, validate the complete Bag against the profile, and then validate the Bag against the cannonical BagIt spec. 

Some profile attributes are fatal: failure to validate accept-serialization or accept-version implies that the rest of the bag is unverifiable and processing should stop. Processing may continue after other errors in order to generate a comprehensive error report.

Implementation details
---

The following fields make up a BagIt profile. Each field is a top-level JSON key, as illustrated in the examples that follow.

1. bag-info:
Specifies which tags are required, etc. Assumes presence of bag-info.txt. Each tag definition takes two optional parameters: required is true or false (default false) and indicates whether or not this tag is required. "values" is a list of acceptable values. If empty, any value is accepted.

bag-info.txt must contain the tag 'Bag-Profile', with a value of the URI of the JSON file containing the profile. LIST in the key definitions indicates that the key can have one or more values, serialized as a JSON array. Itemized values separated by a | indicate allowed options for that field.

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

    {
      "bag-info.txt": {
        "bagging-date": {
          "required": true
         },
        "source-organization" : {
          "required": true,
          "values": [ "Simon Fraser University", "York Univeristy" ]
         },
        "contact-phone": {
          "required": true
        },
      },
      "manifests-required" : [ "md5" ],
      "allow-fetch.txt" : false,
      "serialization" : "required",
      "accept-serialization" : [ "application/zip", "application/tar" ],
      "accept-version" : [ "0.96", "0.97" ],
    }


bagProfileBar.json

    {
      bag-info.txt: {
      "Source-Organization": {
        "required": true,
         "values": "Simon Fraser University", "York University"
      },
      "Organization-Address": {
        "required": true,
        "values": "8888 University Drive Burnaby, B.C. V5A 1S6 Canada", "4700 Keele Street Toronto, Ontario M3J 1P3 Canada"
      },
      "Contact-Name": {
        "required": true,
        "values": "Mark Jordan", "Nick Ruest"
      },
      "Contact-Phone": {
        "required": false
      },
      "Contact-Email": {
        "required": true
      },
      "External-Description": {
        "required": true
      },
      "External-Identifier": {
        "required": false
      },
      "Bag-Size": {
        "required": true
      },
          
      "Bag-Group-Identifier: {
        "required": false
      },
      "Bag-Count": {
        "required": true
      },
      "Internal-Sender-Identifier": {
        "required": false
      },
      "Internal-Sender-Description": {
        "required": false
      },
      "Bagging Date: {
        "required": true
        "yyyy-mm-dd"
      },
      "Payload-Oxum: {
        "required": true
      },
    },
    
    bagit.txt: {
      "required": true
    },

    "manifest-required":  [ "md5" ],
    "allow-fetch.txt" : false,
    "serialization" : "required",
    "accept-serialization" : [ "application/zip", "application/tar" ],
    "accept-version" : [ "0.96", "0.97" ],
  }

@todo
---

* Request feedback from BagIt implementer community, initially over the digital-curation@googlegroups.com discussion list.
* Write code to confirm proof-of-concept use cases.
* Formalize specification.
* Write standard libraries to assist in profile validation.
* Establish a public registry of BagIt profiles for common uses, such as ingestion of content into repository platforms.
