# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 OpenStack, LLC
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from nose.plugins.attrib import attr

from tempest.common.utils.data_utils import arbitrary_string
from tempest.common.utils.data_utils import rand_name
from tempest import exceptions
from tempest.tests.object_storage import base


class ObjectTest(base.BaseObjectTest):

    @classmethod
    def setUpClass(cls):
        super(ObjectTest, cls).setUpClass()

        #Create a container
        cls.container_name = rand_name(name='TestContainer')
        cls.container_client.create_container(cls.container_name)

    @classmethod
    def tearDownClass(cls):
        #Get list of all object in the container
        objlist = \
            cls.container_client.list_all_container_objects(cls.container_name)

        #Attempt to delete every object in the container
        for obj in objlist:
            resp, _ = cls.object_client.delete_object(cls.container_name,
                                                      obj['name'])

        #Attempt to delete the container
        resp, _ = cls.container_client.delete_container(cls.container_name)

    @attr(type='smoke')
    def test_create_object(self):
        # Create storage object, test response

        #Create Object
        object_name = rand_name(name='TestObject')
        data = arbitrary_string()
        resp, _ = self.object_client.create_object(self.container_name,
                                                   object_name, data)

        #Create another Object
        object_name = rand_name(name='TestObject')
        data = arbitrary_string()
        resp, _ = self.object_client.create_object(self.container_name,
                                                   object_name, data)
        self.assertEqual(resp['status'], '201')

    @attr(type='smoke')
    def test_delete_object(self):
        # Create and delete a storage object, test responses

        #Create Object
        object_name = rand_name(name='TestObject')
        data = arbitrary_string()
        resp, _ = self.object_client.create_object(self.container_name,
                                                   object_name, data)

        resp, _ = self.object_client.delete_object(self.container_name,
                                                   object_name)
        self.assertEqual(resp['status'], '204')

    @attr(type='smoke')
    def test_object_metadata(self):
        # Add metadata to storage object, test if metadata is retrievable

        #Create Object
        object_name = rand_name(name='TestObject')
        data = arbitrary_string()
        resp, _ = self.object_client.create_object(self.container_name,
                                                   object_name, data)

        #Set Object Metadata
        meta_key = rand_name(name='test-')
        meta_value = rand_name(name='MetaValue-')
        orig_metadata = {meta_key: meta_value}

        resp, _ = \
            self.object_client.update_object_metadata(self.container_name,
                                                      object_name,
                                                      orig_metadata)
        self.assertEqual(resp['status'], '202')

        #Get Object Metadata
        resp, resp_metadata = \
            self.object_client.list_object_metadata(self.container_name,
                                                    object_name)
        self.assertEqual(resp['status'], '200')
        actual_meta_key = 'x-object-meta-' + meta_key
        self.assertTrue(actual_meta_key in resp)
        self.assertEqual(resp[actual_meta_key], meta_value)

    @attr(type='smoke')
    def test_get_object(self):
        # Retrieve object's data(in response body)

        #Create Object
        object_name = rand_name(name='TestObject')
        data = arbitrary_string()
        resp, _ = self.object_client.create_object(self.container_name,
                                                   object_name, data)

        resp, body = self.object_client.get_object(self.container_name,
                                                   object_name)
        self.assertEqual(resp['status'], '200')
        # Check data
        self.assertEqual(body, data)

    @attr(type='smoke')
    def test_copy_object_in_same_container(self):
        # Copy storage object

        # Create source Object
        src_object_name = rand_name(name='SrcObject')
        src_data = arbitrary_string(size=len(src_object_name) * 2,
                                    base_text=src_object_name)
        resp, _ = self.object_client.create_object(self.container_name,
                                                   src_object_name, src_data)

        # Create destination Object
        dst_object_name = rand_name(name='DstObject')
        dst_data = arbitrary_string(size=len(dst_object_name) * 3,
                                    base_text=dst_object_name)
        resp, _ = self.object_client.create_object(self.container_name,
                                                   dst_object_name, dst_data)

        # Copy source object to destination
        resp, _ = self.object_client.copy_object_in_same_container(
            self.container_name, src_object_name, dst_object_name)
        self.assertEqual(resp['status'], '201')

        # Check data
        resp, body = self.object_client.get_object(self.container_name,
                                                   dst_object_name)
        self.assertEqual(body, src_data)

    @attr(type='smoke')
    def test_copy_object_to_itself(self):
        # Change the content type of an existing object

        # Create Object
        object_name = rand_name(name='TestObject')
        data = arbitrary_string()
        resp, _ = self.object_client.create_object(self.container_name,
                                                   object_name, data)
        # Get the old content type
        resp_tmp, _ = self.object_client.list_object_metadata(
            self.container_name,
            object_name)
        # Change the content type of the object
        metadata = {'content-type': 'text/plain; charset=UTF-8'}
        self.assertNotEqual(resp_tmp['content-type'], metadata['content-type'])
        resp, _ = self.object_client.copy_object_in_same_container(
            self.container_name, object_name, object_name, metadata)
        self.assertEqual(resp['status'], '201')

        # Check the content type
        resp, _ = self.object_client.list_object_metadata(self.container_name,
                                                          object_name)
        self.assertEqual(resp['content-type'], metadata['content-type'])

    @attr(type='smoke')
    def test_copy_object_2d_way(self):
        # Copy storage object

        # Create source Object
        src_object_name = rand_name(name='SrcObject')
        src_data = arbitrary_string(size=len(src_object_name) * 2,
                                    base_text=src_object_name)
        resp, _ = self.object_client.create_object(self.container_name,
                                                   src_object_name, src_data)

        # Create destination Object
        dst_object_name = rand_name(name='DstObject')
        dst_data = arbitrary_string(size=len(dst_object_name) * 3,
                                    base_text=dst_object_name)
        resp, _ = self.object_client.create_object(self.container_name,
                                                   dst_object_name, dst_data)

        # Copy source object to destination
        resp, _ = self.object_client.copy_object_2d_way(self.container_name,
                                                        src_object_name,
                                                        dst_object_name)
        self.assertEqual(resp['status'], '201')

        # Check data
        resp, body = self.object_client.get_object(self.container_name,
                                                   dst_object_name)
        self.assertEqual(body, src_data)

    @attr(type='smoke')
    def test_copy_object_across_containers(self):
        # Copy storage object across containers

        #Create a container so as to use as source container
        src_container_name = rand_name(name='TestSourceContainer')
        self.container_client.create_container(src_container_name)

        #Create a container so as to use as destination container
        dst_container_name = rand_name(name='TestDestinationContainer')
        self.container_client.create_container(dst_container_name)

        # Create Object in source container
        object_name = rand_name(name='Object')
        data = arbitrary_string(size=len(object_name) * 2,
                                base_text=object_name)
        resp, _ = self.object_client.create_object(src_container_name,
                                                   object_name, data)
        #Set Object Metadata
        meta_key = rand_name(name='test-')
        meta_value = rand_name(name='MetaValue-')
        orig_metadata = {meta_key: meta_value}

        resp, _ = \
            self.object_client.update_object_metadata(src_container_name,
                                                      object_name,
                                                      orig_metadata)
        self.assertEqual(resp['status'], '202')

        try:
            # Copy object from source container to destination container
            resp, _ = self.object_client.copy_object_across_containers(
                src_container_name, object_name, dst_container_name,
                object_name)
            self.assertEqual(resp['status'], '201')

            # Check if object is present in destination container
            resp, body = self.object_client.get_object(dst_container_name,
                                                       object_name)
            self.assertEqual(body, data)
            actual_meta_key = 'x-object-meta-' + meta_key
            self.assertTrue(actual_meta_key in resp)
            self.assertEqual(resp[actual_meta_key], meta_value)

        except Exception as e:
            self.fail("Got exception :%s ; while copying"
                      " object across containers" % e)
        finally:
            #Delete objects from respective containers
            resp, _ = self.object_client.delete_object(dst_container_name,
                                                       object_name)
            resp, _ = self.object_client.delete_object(src_container_name,
                                                       object_name)
            #Delete containers created in this method
            resp, _ = self.container_client.delete_container(
                src_container_name)
            resp, _ = self.container_client.delete_container(
                dst_container_name)

    @attr(type='smoke')
    def test_access_public_container_object_without_using_creds(self):
        # Make container public-readable, and access the object
           # anonymously, e.g. without using credentials

        try:
            resp_meta = None
            # Update Container Metadata to make public readable
            cont_headers = {'X-Container-Read': '.r:*,.rlistings'}
            resp_meta, body = \
                self.container_client.update_container_metadata(
                    self.container_name, metadata=cont_headers,
                    metadata_prefix='')
            self.assertEqual(resp_meta['status'], '204')

            # Create Object
            object_name = rand_name(name='Object')
            data = arbitrary_string(size=len(object_name),
                                    base_text=object_name)
            resp, _ = self.object_client.create_object(self.container_name,
                                                       object_name, data)
            self.assertEqual(resp['status'], '201')

            # List container metadata
            resp_meta, _ = \
                self.container_client.list_container_metadata(
                    self.container_name)
            self.assertEqual(resp_meta['status'], '204')
            self.assertIn('x-container-read', resp_meta)
            self.assertEqual(resp_meta['x-container-read'], '.r:*,.rlistings')

            # Trying to Get Object with empty Headers as it is public readable
            resp, body = \
                self.custom_object_client.get_object(self.container_name,
                                                     object_name, metadata={})
            self.assertEqual(body, data)
        finally:
            if resp_meta['status'] == '204':
                # Delete updated container metadata, to revert back.
                resp, body = \
                    self.container_client.delete_container_metadata(
                        self.container_name, metadata=cont_headers,
                        metadata_prefix='')

                resp, _ = \
                    self.container_client.list_container_metadata(
                        self.container_name)
                self.assertEqual(resp['status'], '204')
                self.assertIn('x-container-read', resp)
                self.assertEqual(resp['x-container-read'], 'x')

    @attr(type='negative')
    def test_access_object_without_using_creds(self):
        # Attempt to access the object anonymously, e.g.
        # not using any credentials

        # Create Object
        object_name = rand_name(name='Object')
        data = arbitrary_string(size=len(object_name),
                                base_text=object_name)
        resp, _ = self.object_client.create_object(self.container_name,
                                                   object_name, data)
        self.assertEqual(resp['status'], '201')

        # Trying to Get Object with empty Headers
        self.assertRaises(exceptions.Unauthorized,
                          self.custom_object_client.get_object,
                          self.container_name, object_name, metadata={})

    @attr(type='negative')
    def test_write_object_without_using_creds(self):
        # Attempt to write to the object anonymously, e.g.
        # not using any credentials

        # Trying to Create Object with empty Headers
        object_name = rand_name(name='Object')
        data = arbitrary_string(size=len(object_name),
                                base_text=object_name)
        obj_headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json'}

        self.assertRaises(exceptions.Unauthorized,
                          self.custom_object_client.create_object,
                          self.container_name, object_name, data,
                          metadata=obj_headers)

    @attr(type='negative')
    def test_delete_object_without_using_creds(self):
        # Attempt to delete the object anonymously,
        # e.g. not using any credentials

        # Create Object
        object_name = rand_name(name='Object')
        data = arbitrary_string(size=len(object_name),
                                base_text=object_name)
        resp, _ = self.object_client.create_object(self.container_name,
                                                   object_name, data)

        # Trying to Delete Object with empty Headers
        self.assertRaises(exceptions.Unauthorized,
                          self.custom_object_client.delete_object,
                          self.container_name, object_name)
