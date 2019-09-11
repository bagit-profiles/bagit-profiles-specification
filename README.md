BagIt Profiles Specification
===

Status of this specification
---
Current version: 2.0 (2010-09-12). Maintained by Mark Jordan and Nick Ruest.

Original draft created by members of the Access 2012 Hackfest group: Meghan Currie, Krista Godfrey, Mark Jordan, Nick Ruest, William Wueppelmann, and Dan Chudnov.


Feedback / discussion
---

Please comment on this draft specification in the Digital Curation Google Group, https://groups.google.com/forum/?fromgroups#!forum/digital-curation .

Purpose and background
---

The purpose of the BagIt Profiles Specification is to allow creators and consumers of Bags to agree on optional components of the Bags they are exchanging. Details of the profile are instantiated in a JSON file that both the producing and consuming applications interpret using the conventions described below. The profile file sits at an HTTP URI (e.g., `http://example.com/bagitprofiles/profile-bar-v0.1.json`), and can therefore be read by any number of applications creating or consuming Bags:

	                        BagIt Profile JSON file
                                        /       \
                                       v         v
                        Bag creating app 1  -->  Bag consuming app
                        Bag creating app 2


This proposed Specification builds on the sample profile included in the Library of Congress Bagger tool. However, that profile was local to LC and not intended to be implemented widely. The proposed Specification is intended to be an optional extension to the cannonical BagIt spec, and in no way modifies that specification. Like the BagIt spec, this Profile spec is agnostic to the payload stored in a Bag's data directory.

Use cases for BagIt profiles include distributed mass production of Bags, repository or application-specific content ingestion via Bags (e.g. SWORD, Archivematica), and Preservation-as-a-Service.

Workflow
---

The intended workflow for using a BagIt profile is:

1. The creator of the Bags ensures that Bags it produces meet all of the constraints expressed in the agreed-upon and published BagIt profile file. The creator declares the `BagIt-Profile-Identifier` in the `bag-info.txt` file of the Bags.

2. The consumer of the Bags identifies the profile(s) from the `BagIt-Profile-Identifier` field in their `bag-info.txt`. The consumer then retrieves the profile file from its URI and validates incoming Bags against it; specifically, it must complete the Bag if `fetch.txt` is present, validate the complete Bag against the profile, and then validate the Bag against the cannonical BagIt spec.

Each of these steps may be performed by a separate tool or microservice; in fact, implementers may integrate validation functionality in tools that perform other Bag-processing functions. For example, the completion of a holey Bag might be performed by a more general Bag-processing tool and need not be delegated to a separate validation tool.

Some profile constraints are fatal: for example, failure to validate 'Accept-Serialization' or 'Accept-BagIt-Version' implies that the rest of the bag is unverifiable and processing should stop. Therefore, the task that checks these two constraints should be performed as early as possible in the workflow. Processing may continue after non-fatal errors in order to generate a comprehensive error report.

Implementation details
---

Bags complying to a BagIt profile MUST contain the tag `BagIt-Profile-Identifier`
in their `bag-info.txt`, which value is the URI of the JSON file containing the profile it
conform to.  This tag MAY be repeated if the bag conforms to multiple profiles.
The URI that identifies the profile SHOULD be versioned, e.g. `http://example.com/bagitprofiles/profile-bar-v0.1.json`.
Resolving the URI with `Accept: application/json` SHOULD provide a BagIt Profile as JSON according to this specification.

The following fields make up a BagIt profile. Each field is a top-level JSON key, as illustrated in the examples that follow. LIST in the field definitions indicates that the key can have one or more values, serialized as a JSON array. Itemized values separated by a | indicate allowed options for that field.

1. `BagIt-Profile-Info`:

A list of tags that describes the profile itself. The following tags are
required in this section: `Source-Organization`, `External-Description`,
`Version`, and `BagIt-Profile-Identifier`. Starting with version [`v1.2.0`],
`BagIt-Profile-Version` is also required.

The `Source-Organization` and `External-Description` tags are taken from the
[reserved tags defined in the BagIt spec](https://tools.ietf.org/html/rfc8493#page-10).

The value of `Version` contains the version of the profile; the value of
`BagIt-Profile-Identifier` is the URI where the profile file is available, and
will have the same value as the `BagIt-Profile-Identifier` tag in bag-info.txt
(see below).

The value of `BagIt-Profile-Version` contains the version of this specification the
profile.conforms to. Since the tag was introduced after version [`v1.1.0`], any
profile not explicitly defining `BagIt-Profile-Version` should be treated as
conforming to version [`1.1.0`] of this specification.

Inclusion of `Contact-Name,` `Contact-Phone` and `Contact-Email,`
as [defined in the BagIt spec](https://tools.ietf.org/html/rfc8493#page-10), is not required but is encouraged.

2. `Tags`:

*(Added in [`v2.0`])*

A list of tag definitions, each of which describes requirements, constraints, and/or help text associated with a tag that may be present in the bag. Each tag definition may include the following parameters:

    * "tagName" [required] is the name of the tag. E.g. "Source-Organization"
    * "tagFile" [required] is the path of the file in which the tag appears. This path is relative to the root of the bag. For example, "bag-info.txt" or "custom-tags/custom.txt".
    * "required" is true or false (default false) and indicates whether or not this tag is required.
    * "values" is a list of acceptable values. If empty, any value is accepted.
    * "repeatable" is true or false (default true) and indicates whether or not this tag can be repeated in the file.
    * "help" is free-form text to assist bag creators in understanding what information is expected to be supplied as the tag's value.

	Implementers may define in the Tags section of their profile whatever tags their application requires, i.e., tags defined here are not limited to the 'reserved metadata element names' identified in the BagIt spec.

All required tags must be listed in the Tags list. If a tag in the list is required, the tag file containing that tag is also required to exist in a valid bag.

3. `Manifests-Required`: LIST

	Each manifest type in LIST is required. The list contains the type of manifest (not
	the complete filename), e.g. `["sha1", "md5"]`.

4. `Manifests-Allowed`: LIST

*(Added in [`v2.0`])*

   Each manifest type in the list may be present in the bag. If `Manifests-Required` is empty, a valid bag must include at least one payload manifest from the `Manifests-Allowed` list.

5. `Allow-Fetch.txt`: `true`|`false`

	A fetch.txt file is allowed within the bag. Default: `true`

6. `Serialization`: `forbidden`|`required`|`optional`

	Allow, forbid or require serialization of Bags. Default is `optional`.

7. `Accept-Serialization`: LIST

	A list of MIME types acceptable as serialized formats. E.g. "application/zip". If serialization has a value of required or optional, at least one value is needed. If serialization is forbidden, this has no meaning.

8. `Deserialization-Match-Required`: `true` | `false`

*(Added in [`v2.0`])*

   If this is true, a serialized bag must deserialize to a directory whose name matches the name of the serialized bag, minus the file extension. For example, `bagOfPhotos.tar` would have to deserialize to a single directory called `bagOfPhotos`. The default value for this option is `false`.

9. `Accept-BagIt-Version`: LIST

	A list of BagIt version numbers that will be accepted. At least one version number is required. All version numbers MUST be UTF-8 encoded strings.

8. `Tag-Manifests-Required`: LIST

  Each tag manifest type in LIST is required. The list contains the type of manifest (not
the complete filename), e.g. `["sha1", "md5"]`.

9. `Tag-Manifests-Allowed`: LIST

*(Added in [`v2.0`])*

   Each manifest type in the list may be present in the bag. If `Tag-Manifests-Required` is empty, a bag may include one or more tag manifest from the `Tag-Manifests-Allowed` list.

10. `Tag-Files-Allowed`: LIST

*(Added in [`v1.2.0`])*

  A list of tag files that may be included in a conformant Bag. Entries are either full path names relative to the bag base directory or path name patterns in which asterisks can represent zero or more characters (c.f. [glob(7)](http://man7.org/linux/man-pages/man7/glob.7.html)).

  If `Tag-Files-Allowed` is not provided, its value is assumed to be `['*']`, i.e. all tag files are allowed.

As per the [BagIt Spec](https://tools.ietf.org/html/rfc8493), these tag files need not be listed in tag manifest files.

  At least all the tag files listed in `Tags` must be in included in `Tag-Files-Allowed`.

Examples
---

[bagProfileFoo.json](https://raw.github.com/bagit-profiles/bagit-profiles/master/bagProfileFoo.json)

<!-- BEGIN-EVAL -w '```json' '```' -- cat ./bagProfileFoo.json -->
```json
{
   "BagIt-Profile-Info":{
      "BagIt-Profile-Identifier":"http://www.library.yale.edu/mssa/bagitprofiles/disk_images.json",
      "BagIt-Profile-Version": "2.0",
      "Source-Organization":"Yale University",
      "Contact-Name":"Mark Matienzo",
      "External-Description":"BagIt profile for packaging disk images",
      "Version":"0.3"
   },
    "Tags":[
        {
            "tagFile": "bagit.txt",
            "tagName": "BagIt-Version",
            "required": true,
            "values": [
                "0.96",
                "0.97"
            ],
            "defaultValue": "0.97",
            "help": "Which version of the BagIt specification describes this bag's format?"
        },
        {
            "tagFile": "bagit.txt",
            "tagName": "Tag-File-Character-Encoding",
            "required": true,
            "values": [
                "UTF-8"
            ],
            "defaultValue": "UTF-8",
            "help": "How are this bag's plain-text tag files encoded?"
        },
        {
            "tagFile": "bag-info.txt",
            "tagName": "Bagging-Date",
            "required": true,
            "help": "The date this bag was created."
        },
        {
            "tagName": "Source-Organization",
            "tagFile": "bag-info.txt",
            "required":true,
            "values":[
                "Simon Fraser University",
                "York University"
            ],
            "help": "The name of the organization transferring the content. This organization is assumed to be the custodian of the content."
        },
        {
            "tagFile": "bag-info.txt",
            "tagName": "Contact-Phone",
            "required": true,
            "values": [],
            "help": "The phone number of the bagging/archiving contact in the source organization."
        },
    ],
    "Manifests-Allowed": [
        "md5",
        "sha1",
		"sha224",
        "sha256",
        "sha384",
        "sha512"
    ],
    "Tag-Manifests-Allowed": [
        "md5",
        "sha1",
		"sha224",
        "sha256",
        "sha384",
        "sha512"
    ],
    "Allow-Fetch.txt":false,
    "Serialization":"required",
    "Deserialization-Match-Required": false,
    "Accept-Serialization":[
        "application/zip",
        "application/tar"
    ],
    "Accept-BagIt-Version":[
        "0.96",
        "0.97"
    ]
}
```

<!-- END-EVAL -->

[bagProfileBar.json](https://raw.github.com/bagit-profiles/bagit-profiles/master/bagProfileBar.json)

<!-- BEGIN-EVAL -w '```json' '```' -- cat ./bagProfileBar.json  -->
```json
{
    "BagIt-Profile-Info":{
        "BagIt-Profile-Identifier":"http://canadiana.org/standards/bagit/tdr_ingest.json",
        "BagIt-Profile-Version": "2.0",
        "Source-Organization":"Candiana.org",
        "Contact-Name":"William Wueppelmann",
        "Contact-Email":"tdr@canadiana.com",
        "External-Description":"BagIt profile for ingesting content into the C.O. TDR loading dock.",
        "Version":"1.3"
    },
    "Tags":[
        {
            "tagFile": "bagit.txt",
            "tagName": "BagIt-Version",
            "required": true,
            "values": [
                "0.96",
                "0.97",
                "1.0"
            ],
            "defaultValue": "0.97",
            "help": "Which version of the BagIt specification describes this bag's format?"
        },
        {
            "tagFile": "bagit.txt",
            "tagName": "Tag-File-Character-Encoding",
            "required": true,
            "values": [
                "UTF-8"
            ],
            "defaultValue": "UTF-8",
            "help": "How are this bag's plain-text tag files encoded?"
        },
        {
            "tagName": "Source-Organization",
            "tagFile": "bag-info.txt",
            "required":true,
            "values":[
                "Simon Fraser University",
                "York University"
            ],
            "help": "The name of the organization transferring the content. This organization is assumed to be the custodian of the content."
        },
        {
            "tagName": "Organization-Address",
            "tagFile": "bag-info.txt",
            "required":true,
            "values":[
                "8888 University Drive Burnaby, B.C. V5A 1S6 Canada",
                "4700 Keele Street Toronto, Ontario M3J 1P3 Canada"
            ],
            "help": "The street address of the source organization."
        },
        {
            "tagFile": "bag-info.txt",
            "tagName": "Contact-Name",
            "required":true,
            "values":[
                "Mark Jordan",
                "Nick Ruest"
            ],
            "help": "The street address of the source organization."
      },
        {
            "tagFile": "bag-info.txt",
            "tagName": "Contact-Phone",
            "required": false,
            "values": [],
            "help": "The phone number of the bagging/archiving contact in the source organization."
        },
        {
            "tagFile": "bag-info.txt",
            "tagName": "Contact-Email",
            "required": true,
            "help": "The email address of the bagging/archiving contact in the source organization."
        },
        {
            "tagFile": "bag-info.txt",
            "tagName": "External-Description",
            "required": true,
        },
        {
            "tagFile": "bag-info.txt",
            "tagName": "External-Identifier",
            "required": true,
        },
        {
            "tagFile": "bag-info.txt",
            "tagName": "Bag-Size",
            "required": true,
            "help": "The approximate size of the bag's payload, in human-readable format. E.g. 33MB or 268GB."
        },
        {
            "tagFile": "bag-info.txt",
            "tagName": "Bag-Group-Identifier",
            "required": false,
            "help": "An identifier that marks this bag as part of a single collection or a related group of items that has been packaged into several bags."
        },
        {
            "tagFile": "bag-info.txt",
            "tagName": "Bag-Count",
            "required": true,
            "help": "Two numbers separated by \"of\", in particular, \"N of T\", where T is the total number of bags in a group of bags and N is the ordinal number within the group; if T is not known, specify it as \"?\" (question mark).  Examples: 1 of 2, 4 of 4, 3 of ?, 89 of 145."
        },
        {
            "tagFile": "bag-info.txt",
            "tagName": "Internal-Sender-Identifier",
            "required": false,
            "help": "A unique identifier for this bag inside your organization."
        },
        {
            "tagFile": "bag-info.txt",
            "tagName": "Internal-Sender-Description",
            "required": false,
            "help": "A description of the bag's contents for the sender's internal use."
        },
        {
            "tagFile": "bag-info.txt",
            "tagName": "Bagging-Date",
            "required": true,
            "help": "The date this bag was created."
        },
        {
            "tagFile": "bag-info.txt",
            "tagName": "Payload-Oxum",
            "required": true,
            "help": "The number of files and bytes in this bag's payload. This should be calculated and set by the bagging software."
        },
        {
            "tagFile": "custom-tags/custom-info.txt",
            "tagName": "Custom-Tag-One",
            "required": true
        },
        {
            "tagFile": "custom-tags/custom-info.txt",
            "tagName": "Custom-Tag-Two",
            "required": false,
            "values": [
                "Linux",
                "Mac",
                "Windows"
            ]
        }
    ],
    "Manifests-Required":[
        "md5"
    ],
    "Manifests-Allowed": [
        "md5",
        "sha1",
		"sha224",
        "sha256",
        "sha384",
        "sha512"
    ],
    "Allow-Fetch.txt":false,
    "Serialization":"optional",
    "Deserialization-Match-Required": true,
    "Accept-Serialization":[
      "application/zip"
    ],
    "Tag-Manifests-Required":[
        "md5"
    ],
    "Tag-Manifests-Allowed": [
        "md5",
        "sha1",
		"sha224",
        "sha256",
        "sha384",
        "sha512"
    ],
    "Tag-Files-Allowed":[
        "DPN/*"
    ],
    "Accept-BagIt-Version":[
        "0.96"
    ]
}
```

<!-- END-EVAL -->

@todo
---

* ~~Add license (CC0/Public Domain?).~~
* ~~Request feedback from BagIt implementer community, initially in the Digital Curation Google Group.~~
* ~~Write code to confirm proof-of-concept use cases.~~
* ~~Formalize specification.~~ (Version 1.0 2013-05-19)
* Write standard libraries to assist in profile validation. ~~([Python](https://github.com/bagit-profiles/bagit-profiles-validator) done)~~
* Establish a public registry of BagIt profiles for common uses, such as ingestion of content into repository platforms.

### License

![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")

[`v1.1.0`]: https://github.com/bagit-profiles/bagit-profiles/tree/1.1.0
[`v1.2.0`]: https://github.com/bagit-profiles/bagit-profiles/tree/1.2.0
