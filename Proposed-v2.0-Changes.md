# Proposed BagIt Profile Changes for v2.0

This document proposes some breaking changes to the BagIt Profiles specification.

The current BagIt Profiles spec only defines tags within the bag-info.txt file. It cannot describe valid APTrust bags because APTrust requires a tag file called aptrust-info.txt, which must contain a specific set of tags, each of which has defined constraints. Other organizations in the past, such as DPN, also required a defined set of tags outside of bag-info.txt, and future organizations will likely do the same.

APTrust proposes changes to BagIt Profiles to achieve the following goals:

1. Allow profiles to descibe tags outside the bag-info.txt file.

2. Simplify the work of software that creates and validates bags by collecting all tag requirements in a single list within the profile.

3. Allow profiles to tell users (optionally through bagging software user GUIs) what information is expected in tag values.

4. Allow profiles to specify a set of valid manifests and tag manifests without prescribing which manifest algorithms must be used.

5. Allow profiles to specify whether serialized bags must expand into a directory that matches the name of the serialized bag.

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

2. Second, the key names in the JSON structure don't necessarily match the tag file names. Bag-Info.txt and bag-info.txt are not the same thing on case-sensitive file systems. Asking the bagging/validation software to infer file names based on loosely matching key names invites trouble.

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

Bagging software and bag validators can scan a single list in the profile definition to find all required tags in all required tag files. If a tag file contains a single required tag, the bagger/validator can assume the containing tag file is also required. If this is the case, `Tag-Files-Required` would no longer be required.

### A Note on the Help Attribute

APTrust uses the help attribute of each tag definition to provide tooltips in its graphical bagging library. These tips help users understand what information is expected in a tag field. For example, see the tooltip for the Bag-Group-Identifier tag in the screenshot below.

![DART bagging tool showing a tooltip for the Bag-Group-Identifier tag](./img/HelpAsTooltip.png)

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

Because APTrust, Chronopolis, DuraCloud, LOCKSS, and MetaArchive are all participating in the BTR grant, all may at some point be supporting the BTR profile idea of specifying allowed manifest algorithms without prescribing which specific one should be used.

## Deserialization-Match-Required

Finally, APTrust has one request related to validating serialized bags. We currently enforce a recommendation that was part of version 14 of the BagIt spec but was later dropped. [Section 4.2](https://tools.ietf.org/html/draft-kunze-bagit-14#page-11) of the old spec said:

```
The serialization SHOULD have the same name as the bag's base directory...
```

APTrust has always enforced a rule that these names MUST match. That is, if a tarred bag file is called `photos.tar`, it must untar to a single directory called `photos`.

APTrust and other DDPs typically untar bags in a staging area during the ingest process. When the bag `photos.tar` bag untars to a directory called `photos`, we can be sure its contents will not overwrite or commingle with the contents of another bags being processed at the same time.

Allowing bags to deserialize to arbitrary locations can cause problems. For example, if `photos.tar`, `audio.tar`, and `video.tar` all expand to directory called `bag_contents` and are all being ingested at the same time, contents of one bag can be mistaken for contents of another bag, and we wind up with a mess.

To prevent this, APTrust looks into serialized bags BEFORE deserializing them to ensure that the will expand into a directory with the same name. We reject bags that don't meet this rule.

Although the recommendation in Section 4.2 was dropped from the official BagIt spec, we would like BagIt profiles to provide a way to specify whether a valid bag must deserialize to an expected directory. This rule would only apply to serialized bags, and can default to false.

It has practical applications for DDPs and can vastly simplify the ingest process and the maintenance of the DDPs' staging area. APTrust is not the only DDP to use a staging area for bag validation. Chronopolis, Texas Digital Library, and Hathi Trust also used staging areas when they acted as DPN nodes, and DDPs will likely continue to use them in the future.

## BTR and APTrust Change Requests

The BTR team will be submitting its comments and change requests separately in the coming weeks. Nothing in the BTR requests contradicts anything in the APTrust requests. The only difference so far is the name of the `help/description` attribute, and APTrust is flexible on that.

## Included Sample Profiles

The sample profiles [bagProfileBar.json](bagProfileBar.json) and [bagProfileFoo.json](bagProfileFoo.json) have been revised from the 1.2.0 spec to use the format of the proposed 2.0 spec.