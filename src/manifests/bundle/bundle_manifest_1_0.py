# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from manifests.manifest import Manifest


class BundleManifest_1_0(Manifest):
    """
    A BundleManifest is an immutable view of the outputs from a assemble step
    The manifest contains information about the bundle that was built (in the `assemble` section),
    and the components that made up the bundle in the `components` section.

    The format for schema version 1.0 is:
        schema-version: "1.0"
        build:
          name: string
          version: string
          architecture: x64 or arm64
          location: /relative/path/to/tarball
        components:
          - name: string
            repository: URL of git repository
            ref: git ref that was built (sha, branch, or tag)
            commit_id: The actual git commit ID that was built (i.e. the resolved "ref")
            location: /relative/path/to/artifact
    """

    SCHEMA = {
        "build": {
            "required": True,
            "type": "dict",
            "schema": {
                "architecture": {"required": True, "type": "string"},
                "id": {"required": True, "type": "string"},
                "location": {"required": True, "type": "string"},
                "name": {"required": True, "type": "string"},
                "version": {"required": True, "type": "string"},
            },
        },
        "schema-version": {"required": True, "type": "string", "allowed": ["1.0"]},
        "components": {
            "required": True,
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "commit_id": {"required": True, "type": "string"},
                    "location": {"required": True, "type": "string"},
                    "name": {"required": True, "type": "string"},
                    "ref": {"required": True, "type": "string"},
                    "repository": {"required": True, "type": "string"},
                },
            },
        },
    }

    def __init__(self, data):
        super().__init__(data)
        self.build = self.Build(data["build"])
        self.components = list(map(lambda entry: self.Component(entry), data["components"]))

    def __to_dict__(self):
        return {
            "schema-version": "1.0",
            "build": self.build.__to_dict__(),
            "components": list(map(lambda component: component.__to_dict__(), self.components)),
        }

    class Build:
        def __init__(self, data):
            self.name = data["name"]
            self.version = data["version"]
            self.architecture = data["architecture"]
            self.location = data["location"]
            self.id = data["id"]

        def __to_dict__(self):
            return {
                "name": self.name,
                "version": self.version,
                "architecture": self.architecture,
                "location": self.location,
                "id": self.id,
            }

    class Component:
        def __init__(self, data):
            self.name = data["name"]
            self.repository = data["repository"]
            self.ref = data["ref"]
            self.commit_id = data["commit_id"]
            self.location = data["location"]

        def __to_dict__(self):
            return {
                "name": self.name,
                "repository": self.repository,
                "ref": self.ref,
                "commit_id": self.commit_id,
                "location": self.location,
            }
