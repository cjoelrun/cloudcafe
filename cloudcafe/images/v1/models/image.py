"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from copy import deepcopy

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.compute.common.equality_tools import EqualityTools
from datetime import datetime
import json


class Image(AutoMarshallingModel):
    """@Summary Complete model of an image"""

    def __init__(self, id_=None, status=None, name=None, container_format=None,
                 disk_format=None, owner=None, checksum=None, min_ram=None,
                 min_disk=None, size=None, deleted=None, protected=None,
                 is_public=None, properties=None, created_at=None,
                 updated_at=None, deleted_at=None, members_list=None):
        super(Image, self).__init__()

        self.id_ = id_
        self.status = status
        self.name = name
        self.deleted = deleted
        self.container_format = container_format
        self.created_at = created_at
        self.disk_format = disk_format
        self.updated_at = updated_at
        self.owner = owner
        self.protected = protected
        self.min_ram = min_ram
        self.checksum = checksum
        self.min_disk = min_disk
        self.is_public = is_public
        self.deleted_at = deleted_at
        self.properties = properties
        self.size = size
        self.members_list = members_list

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Image object to compare with
        @type other: Image
        @return: True if Image objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other, '_log')

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Image object to compare with
        @type other: Image
        @return: True if Image objects are not equal, False otherwise
        @rtype: bool
        """
        return not self.__eq__(other)

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            if prop in ['created_at', 'updated_at', 'deleted_at']:
                date_property = self.__dict__[prop]
                date_string = 'None' or \
                              date_property.strftime('%Y-%m-%dT%H:%M:%S')
                values.append("{0}: {1}".format(prop, date_string))
            else:
                values.append("{0}: {1}".format(prop, self.__dict__[prop]))
        return '[ {0} ]'.format(', '.join(values))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        serialized_str.replace('false', 'False')
        serialized_str.replace('true', 'True')
        json_dict = json.loads(serialized_str)

        if 'images' in json_dict.keys():
            images = []
            for image in json_dict['images']:
                images.append(cls._dict_to_obj(image))
            return images
        else:
            image_str = json_dict['image']
            return cls._dict_to_obj(image_str)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        """@summary: Processing dates in converting string to date objects"""
        json_dict = deepcopy(json_dict)
        json_dict['id_'] = json_dict.pop('id')

        for date_key in ['created_at', 'updated_at', 'deleted_at']:
            if json_dict.get(date_key):
                json_dict[date_key] = None or datetime.strptime(
                    json_dict[date_key],
                    '%Y-%m-%dT%H:%M:%S')
        return Image(**json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """Returns an instance of a Image based on the xml serialized_str
        passed in.
        """
        raise NotImplementedError("Glance does not serve XML-formatted \
                                  resources.")

    @classmethod
    def _xml_ele_to_obj(cls, element):
        raise NotImplementedError("Glance does not serve XML-formatted \
                                  resources.")

    def add_member(self, member):
        members_list = self.members_list if self.members_list else []
        members_list.append(member)
        self.members_list = members_list

    def delete_member(self, member_to_delete):
        members_list = self.members_list if self.members_list else []
        for member in self.members_list:
            if member.member_id == member_to_delete.member_id:
                members_list.remove(member_to_delete)

        self.members_list = members_list

    def replace_members_list(self, members_list):
        self.members_list = members_list


class ImageMin(AutoMarshallingModel):
    """A mini Image model returned on certain calls to Images API """

    def __init__(self, id_=None, can_share=None):
        super(ImageMin, self).__init__()

        self.id_ = id_
        self.can_share = can_share

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return ImageMin(
            id_=json_dict['image_id'],
            can_share=json_dict['can_share'])


class ImageMinList(AutoMarshallingModel):
    """Model class that allows automarshalling of list of MinImage."""

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_list = json.loads(serialized_str)

        return [ImageMin._dict_to_obj(image_json) for image_json in
                json_list['shared_images']]
