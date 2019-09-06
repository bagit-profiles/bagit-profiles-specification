# APTrust Proposed BagIt Profile Changes

APTrust has been using a modified version of BagIt profiles as part of its open source [DART](https://github.com/APTrust/dart) software. Among other things, DART can both build and validate bags according to a BagIt profile.

As part of its test suite, DART includes profiles from APTrust and the now defunct DPN. Each of these profiles includes a custom tag file with a number of required tags.

The existing BagIt profiles in this repository cannot describe valid APTrust and DPN bags because APTrust requires a tag file called aptrust-info.txt, which must contain a specific set of tags, and DPN required a file called dpn-tags/dpn-info.txt whose tags also had to comply with a defined set of requirements.

## Limitations of Tag Definitions in BagIt-Profiles v1.2.0

BagIt-Profiles v1.2.0 allows users to specify which tags should be present in the bag-info.txt file, whether they're required, and which values are allowed. For example:

```json
   "Bag-Info":{
      "Source-Organization":{
         "required":true,
         "values":[
            "Simon Fraser University",
            "York University"
         ]
      },
      "Contact-Name":{
         "required":true,
         "values":[
            "Mark Jordan",
            "Nick Ruest"
         ]
      },
      "Contact-Phone":{
         "required":false
      }
```

v1.2.0 also allows users to specify which tag files are required, like so:

```json
   "Tag-Files-Required":[
     "DPN/dpnFirstNode.txt",
     "DPN/dpnRegistry"
   ]
```

The spec does not allow users to specify which specific tags are required in additional files like `aptrust-info.txt` and `dpn/dpn-tags.txt`.

It may be possible to define additional fields in the profile like so to add these definitions:

```json
   "APTrust-Info":{
      "Access":{
         "required":true,
         "values":[
            "Institution",
            "Consortia",
            "Restricted"
         ]
      },
      "Title":{
         "required":true
      },
```

This approach presents two problems.

1. First, in order to collect a list of all tag definitions, the software that creates or validates the bag must scan through all the keys of BagIt profile JSON structure and look for keys that don't match known names like `Manifests-Required`, `Allow-Fetch.txt`, etc. Then it must assume these keys describe tag files, and the values describe tags expected to be in those files.

2. Second, the key names in the JSON structure don't necessarily match the tag file names. Bag-Info.txt and bag-info.txt are not the same thing on case-sensitive file systems.

## Proposed Fix for Tag Definitions

A single key in a BagIt profile called Tags can contain a list of all required tag files as well as definitions of the tags expected to be in them. For example:

```json
    "Tags":[
        {
            "tagFile": "bag-info.txt",
            "tagName": "Source-Organization",
            "required": true,
            "help": "The name of the organization that produced this bag, or is responsible for its contents."
        },
        {
            "tagFile": "aptrust-info.txt",
            "tagName": "Title",
            "required": true,
            "help": "The title or name of that describes this bag's contents."
        },
        {
            "tagFile": "aptrust-info.txt",
            "tagName": "Access",
            "required": true,
            "values": [
                "Consortia",
                "Institution",
                "Restricted"
            ],
            "help": "Access rights for this bag describe who can see that it exists in the repository."
        }
    ]
```

Bagging software and bag validators can scan a single list in the profile definition to get a list of all required tags in all required tag files. If a tag file contains a single required tag, the bagger/validator can assume the containing tag file is also required. `Tag-Files-Required` may then no longer require a separate definition.

### A Note on the Help Attribute

APTrust uses the help attribute of each tag definition to provide tooltips in its graphical bagging library. These tips help users understand what information is expected in a tag field.

Members of the [Beyond the Repository](https://northwestern.app.box.com/s/3qu2qbkdx3aod6wj9jt6977p4byhpj3y) (BTR) project will soon be publishing a BagIt profile intended to be supported by all distributed digital preservation repositories (DDPs) in the US. They also want a new attribute similar to `help` in the tag defintions, though they are calling it `definition`. The name isn't as important as the presence of some inline documentation to help bag creators supply meaningful tag values.

## Manifests-Allowed and Tag-Manifests-Allowed

BagIt profiles v1.2.0 defines `Manifests-Required` and `Tag-Manifests-Required`.

```json
   "Manifests-Required":[
      "md5"
   ],
   "Tag-Manifests-Required": [
      "md5"
   ]
```

However, APTrust currently supports, and BTR plans to support, `Manifests-Allowed` and `Tag-Manifests-Allowed`. In both cases, this is for the practical purpose of making it as easy as possible for depositors to push content to DDPs.

APTrust found that some of its depositors' internal workflows already produced bags with md5 manifests, while others produced bags with sha256 manifests. To avoid making depositors redefine their internal workflows, APTrust started accepting bags with either md5 or sha256 manifests.

Our profile definition looked like this:

```json
   "Manifests-Required":[],
   "Tag-Manifests-Required": [],
   "Manifests-Allowed":[
      "md5",
      "sha256"
   ],
   "Tag-Manifests-Allowed": [
      "md5",
      "sha256"
   ]
```

Since the [BagIt specification](https://tools.ietf.org/html/rfc8493) says a bag must have a payload manifest, APTrust's validator does require a manifest, and will accept any one from the list.

BTR plans a similar definition, in order to make the process of moving data from local repos into DDPs as simple as possible. Their definition will likely support all commonly-implemented digest algorithms, like this:

```json
   "Manifests-Allowed":[
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
   ]
```

## Deserialization-Match-Required

Finally, APTrust has one request related to validating serialized bags. We currently enforce a recommendation that was part of version 14 of the BagIt spec but was later dropped. [Section 4.2](https://tools.ietf.org/html/draft-kunze-bagit-14#page-11) of the old spec said:

```
The serialization SHOULD have the same name as the bag's base directory...
```

APTrust has always enforced a rule that these names MUST match. That is, if a tarred bag file is called `photos.tar`, it must untar to a single directory called `photos`.

APTrust and other DDPs typically untar bags in a staging area during the ingest process. When the bag `photos.tar` bag untars to a directory called `photos`, we can be sure its contents will not overwrite or commingle with the contents of another bags being processed at the same time.

When bags `photos.tar`, `audio.tar`, and `video.tar` all expand to directory called `bag_contents` and are all being ingested at the same time, we wind up with a mess.

To prevent this, APTrust looks into serialized bags BEFORE deserializing them to ensure that the will expand into a directory with the same name. We reject bags that don't meet this rule.

Although the recommendation in Section 4.2 was dropped from the official BagIt spec, we would like BagIt profiles to provide a way to specify whether a valid bag must deserialize to an expected directory. This rule would only apply to serialized bags, and can default to false.

It has practical applications for DDPs and can vastly simplify the ingest process and the maintenance of the DDPs staging area. APTrust is not the only DDP to use a staging area for bag validation. Chronopolis, Texas Digital Library, and Hathi Trust also used staging areas when they acted as DPN nodes, and DDPs will likely continue to use them in the future.

## BTR and APTrust Change Requests

The BTR team will be submitting its comments and change requests separately in the coming weeks. Nothing in the BTR requests contradicts anything in the APTrust requests. The only difference so far is the name of the `help/description` attribute, and APTrust is flexible on that.

## Included Sample Profiles

The JSON files in this directory show sample BagIt profiles for APTrust and DPN that conform to the changes proposed above.

Note that, for the time being, these samples go against the BagIt profile rule of not defining what's expected in the bagit.txt file. These profiles include ALL tags expected to be found in the bag.

Including bagit.txt in the `Tags` list simplifies the work of the bagger and the validator by including all requirements in a single place.

The examples also include a `Default-Value` attribute in tag definitions. DART uses this internally when creating bags. APTrust is not asking for this to be part of a future BagIt profile spec.
