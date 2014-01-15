# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import testtools
import json
from tempest.test import attr
from tempest.api.murano import base
from tempest import exceptions

class SanityMuranoTest(base.MuranoMeta):

    @attr(type='smoke')
    def test_get_list_metadata_objects_ui(self):
        resp, body = self.get_list_metadata_objects("ui")
        assert body is not None
        assert resp['status'] == '200'

    @attr(type='smoke')
    def test_get_list_metadata_objects_workflows(self):
        resp, body = self.get_list_metadata_objects("workflows")
        assert body is not None
        assert resp['status'] == '200'

    @attr(type='smoke')
    def test_get_list_metadata_objects_heat(self):
        resp, body = self.get_list_metadata_objects("heat")
        assert body is not None
        assert resp['status'] == '200'

    @attr(type='smoke')
    def test_get_list_metadata_objects_agent(self):
        resp, body = self.get_list_metadata_objects("agent")
        assert body is not None
        assert resp['status'] == '200'

    @attr(type='smoke')
    def test_get_list_metadata_objects_scripts(self):
        resp, body = self.get_list_metadata_objects("scripts")
        assert body is not None
        assert resp['status'] == '200'

    @attr(type='smoke')
    def test_get_list_metadata_objects_manifests(self):
        resp, body = self.get_list_metadata_objects("manifests")
        assert body is not None
        assert resp['status'] == '200'

    @attr(type='negative')
    def test_get_list_metadata_objects_incorrect_type(self):
        self.assertRaises(exceptions.NotFound, self.get_list_metadata_objects,
                          'someth')

    @attr(type='smoke')
    def test_get_ui_definitions(self):
        resp, body = self.get_ui_definitions()
        assert body is not None
        assert resp['status'] == '200'

    @attr(type='smoke')
    def test_get_conductor_metadata(self):
        resp, body = self.get_conductor_metadata()
        assert body is not None
        assert resp['status'] == '200'

    @attr(type='smoke')
    def test_create_directory_and_delete_workflows(self):
        resp, body = self.create_directory("workflows/", "testdir")
        resp1, body1 = self.delete_metadata_obj_or_folder("workflows/testdir")
        assert resp['status'] == '200'
        assert resp1['status'] == '200'
        assert body['result'] == 'success'
        assert body1['result'] == 'success'

    @attr(type='smoke')
    def test_create_directory_and_delete_ui(self):
        resp, body = self.create_directory("ui/", "testdir")
        resp1, body1 = self.delete_metadata_obj_or_folder("ui/testdir")
        assert resp['status'] == '200'
        assert resp1['status'] == '200'
        assert body['result'] == 'success'
        assert body1['result'] == 'success'

    @attr(type='smoke')
    def test_create_directory_and_delete_heat(self):
        resp, body = self.create_directory("heat/", "testdir")
        resp1, body1 = self.delete_metadata_obj_or_folder("heat/testdir")
        assert resp['status'] == '200'
        assert resp1['status'] == '200'
        assert body['result'] == 'success'
        assert body1['result'] == 'success'

    @attr(type='smoke')
    def test_create_directory_and_delete_agent(self):
        resp, body = self.create_directory("agent/", "testdir")
        resp1, body1 = self.delete_metadata_obj_or_folder("agent/testdir")
        assert resp['status'] == '200'
        assert resp1['status'] == '200'
        assert body['result'] == 'success'
        assert body1['result'] == 'success'

    @attr(type='smoke')
    def test_create_directory_and_delete_scripts(self):
        resp, body = self.create_directory("scripts/", "testdir")
        resp1, body1 = self.delete_metadata_obj_or_folder("scripts/testdir")
        assert resp['status'] == '200'
        assert resp1['status'] == '200'
        assert body['result'] == 'success'
        assert body1['result'] == 'success'

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1268934')
    @attr(type='negative')
    def test_create_directory_manifests(self):
        self.assertRaises(exceptions.Forbidden, self.create_directory,
                          "manifests/", "testdir")

    @attr(type='negative')
    def test_create_directory_incorrect_type(self):
        self.assertRaises(exceptions.NotFound, self.create_directory,
                          "someth/", "testdir")

    @attr(type='smoke')
    def test_double_create_directory(self):
        self.create_directory("workflows/", "testdir")
        resp, body = self.create_directory("workflows/", "testdir")
        assert resp['status'] == '200'
        assert body['result'] == 'success'
        self.delete_metadata_obj_or_folder("workflows/testdir")

    @attr(type='negative')
    def test_delete_nonexistent_object(self):
        self.assertRaises(exceptions.NotFound,
                          self.delete_metadata_obj_or_folder,
                          "somth/blabla")

    @attr(type='negative')
    def test_delete_basic_folder(self):
        self.assertRaises(exceptions.MethodNotAllowed,
                          self.delete_metadata_obj_or_folder,
                          "workflows")

    @attr(type='negative')
    def test_create_basic_folder(self):
        self.assertRaises(exceptions.MethodNotAllowed, self.create_directory,
                          "", "somth")

    @attr(type='negative')
    def test_double_upload_file(self):
        self.upload_metadata_object(path="workflows")
        resp = self.upload_metadata_object(path="workflows")
        assert resp.status_code == 403
        self.delete_metadata_obj_or_folder("workflows/testfile.txt")

    @attr(type='negative')
    def test_upload_file_incorrect(self):
        resp = self.upload_metadata_object(path="workflows/testfil")
        assert resp.status_code == 404

    @attr(type='smoke')
    def test_upload_file_and_delete_workflows(self):
        resp = self.upload_metadata_object(path="workflows")
        resp1, body1 = self.get_list_metadata_objects("workflows")
        self.delete_metadata_obj_or_folder("workflows/testfile.txt")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)

    @attr(type='smoke')
    def test_upload_file_and_delete_ui(self):
        resp = self.upload_metadata_object(path="ui")
        resp1, body1 = self.get_list_metadata_objects("ui")
        self.delete_metadata_obj_or_folder("ui/testfile.txt")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)

    @attr(type='smoke')
    def test_upload_file_and_delete_heat(self):
        resp = self.upload_metadata_object(path="heat")
        resp1, body1 = self.get_list_metadata_objects("heat")
        self.delete_metadata_obj_or_folder("heat/testfile.txt")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)

    @attr(type='smoke')
    def test_upload_file_and_delete_agent(self):
        resp = self.upload_metadata_object(path="agent")
        resp1, body1 = self.get_list_metadata_objects("agent")
        self.delete_metadata_obj_or_folder("agent/testfile.txt")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)

    @attr(type='smoke')
    def test_upload_file_and_delete_scripts(self):
        resp = self.upload_metadata_object(path="scripts")
        resp1, body1 = self.get_list_metadata_objects("scripts")
        self.delete_metadata_obj_or_folder("scripts/testfile.txt")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)

    @attr(type='smoke')
    def test_upload_file_and_delete_manifests(self):
        resp = self.upload_metadata_object(path="manifests",
                                           filename='testfile-manifest.yaml')
        resp1, body1 = self.get_list_metadata_objects("manifests")
        self.delete_metadata_obj_or_folder("manifests/testfile-manifest.yaml")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile-manifest.yaml' in body1)

    @attr(type='smoke')
    def test_get_metadata_object(self):
        self.upload_metadata_object(path="workflows")
        resp1, body1 = self.get_metadata_object("workflows/testfile.txt")
        self.delete_metadata_obj_or_folder("workflows/testfile.txt")
        assert resp1['status'] == '200'
        assert body1 is not None

    @attr(type='negative')
    def test_get_nonexistent_metadata_object(self):
        self.assertRaises(exceptions.NotFound, self.get_metadata_object,
                          "somth/blabla")

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1249303')
    @attr(type='negative')
    def test_delete_nonempty_folder_in_workflows(self):
        self.create_directory("workflows/", "testdir")
        self.upload_metadata_object(path="workflows/testdir")
        self.assertRaises(Exception, self.delete_metadata_obj_or_folder,
                          "workflows/testdir")
        self.delete_metadata_obj_or_folder("workflows/testdir/testfile.txt")
        self.delete_metadata_obj_or_folder("workflows/testdir")

    @attr(type='positive')
    def test_create_folder_and_upload_file_workflows(self):
        self.create_directory("workflows/", "testdir")
        resp = self.upload_metadata_object(path="workflows/testdir")
        resp1, body1 = self.get_list_metadata_objects("workflows/testdir")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)
        resp, _ =\
            self.delete_metadata_obj_or_folder("workflows/testdir/testfile.txt")
        assert resp['status'] == '200'
        resp, _ = self.delete_metadata_obj_or_folder("workflows/testdir")
        assert resp['status'] == '200'
        resp, body = self.get_list_metadata_objects("workflows")
        assert resp['status'] == '200'
        assert ('testfile.txt' not in body)

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1249303')
    @attr(type='negative')
    def test_delete_nonempty_folder_in_ui(self):
        self.create_directory("ui/", "testdir")
        self.upload_metadata_object(path="ui/testdir")
        self.assertRaises(Exception, self.delete_metadata_obj_or_folder,
                          "ui/testdir")
        self.delete_metadata_obj_or_folder("ui/testdir/testfile.txt")
        self.delete_metadata_obj_or_folder("ui/testdir")

    @attr(type='positive')
    def test_create_folder_and_upload_file_ui(self):
        self.create_directory("ui/", "testdir")
        resp = self.upload_metadata_object(path="ui/testdir")
        resp1, body1 = self.get_list_metadata_objects("ui/testdir")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)
        resp, _ =\
            self.delete_metadata_obj_or_folder("ui/testdir/testfile.txt")
        assert resp['status'] == '200'
        resp, _ = self.delete_metadata_obj_or_folder("ui/testdir")
        assert resp['status'] == '200'
        resp, body = self.get_list_metadata_objects("ui")
        assert resp['status'] == '200'
        assert ('testfile.txt' not in body)

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1249303')
    @attr(type='negative')
    def test_delete_nonempty_folder_in_heat(self):
        self.create_directory("heat/", "testdir")
        self.upload_metadata_object(path="heat/testdir")
        self.assertRaises(Exception, self.delete_metadata_obj_or_folder,
                          "heat/testdir")
        self.delete_metadata_obj_or_folder("heat/testdir/testfile.txt")
        self.delete_metadata_obj_or_folder("heat/testdir")

    @attr(type='positive')
    def test_create_folder_and_upload_file_heat(self):
        self.create_directory("heat/", "testdir")
        resp = self.upload_metadata_object(path="heat/testdir")
        resp1, body1 = self.get_list_metadata_objects("heat/testdir")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)
        resp, _ =\
            self.delete_metadata_obj_or_folder("heat/testdir/testfile.txt")
        assert resp['status'] == '200'
        resp, _ = self.delete_metadata_obj_or_folder("heat/testdir")
        assert resp['status'] == '200'
        resp, body = self.get_list_metadata_objects("heat")
        assert resp['status'] == '200'
        assert ('testfile.txt' not in body)

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1249303')
    @attr(type='negative')
    def test_delete_nonempty_folder_in_agent(self):
        self.create_directory("agent/", "testdir")
        self.upload_metadata_object(path="agent/testdir")
        self.assertRaises(Exception, self.delete_metadata_obj_or_folder,
                          "agent/testdir")
        self.delete_metadata_obj_or_folder("agent/testdir/testfile.txt")
        self.delete_metadata_obj_or_folder("agent/testdir")

    @attr(type='positive')
    def test_create_folder_and_upload_file_agent(self):
        self.create_directory("agent/", "testdir")
        resp = self.upload_metadata_object(path="agent/testdir")
        resp1, body1 = self.get_list_metadata_objects("agent/testdir")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)
        resp, _ =\
            self.delete_metadata_obj_or_folder("agent/testdir/testfile.txt")
        assert resp['status'] == '200'
        resp, _ = self.delete_metadata_obj_or_folder("agent/testdir")
        assert resp['status'] == '200'
        resp, body = self.get_list_metadata_objects("agent")
        assert resp['status'] == '200'
        assert ('testfile.txt' not in body)

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1249303')
    @attr(type='negative')
    def test_delete_nonempty_folder_in_scripts(self):
        self.create_directory("scripts/", "testdir")
        self.upload_metadata_object(path="scripts/testdir")
        self.assertRaises(Exception, self.delete_metadata_obj_or_folder,
                          "scripts/testdir")
        self.delete_metadata_obj_or_folder("scripts/testdir/testfile.txt")
        self.delete_metadata_obj_or_folder("scripts/testdir")

    @attr(type='positive')
    def test_create_folder_and_upload_file_scripts(self):
        self.create_directory("scripts/", "testdir")
        resp = self.upload_metadata_object(path="scripts/testdir")
        resp1, body1 = self.get_list_metadata_objects("scripts/testdir")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)
        resp, _ =\
            self.delete_metadata_obj_or_folder("scripts/testdir/testfile.txt")
        assert resp['status'] == '200'
        resp, _ = self.delete_metadata_obj_or_folder("scripts/testdir")
        assert resp['status'] == '200'
        resp, body = self.get_list_metadata_objects("scripts")
        assert resp['status'] == '200'
        assert ('testfile.txt' not in body)

    @attr(type='smoke')
    def test_create_and_delete_new_service(self):
        resp, body = self.create_new_service('test')
        assert resp['status'] == '200'
        assert 'success' in body
        resp, body = self.delete_service('test')
        assert resp['status'] == '200'
        assert 'success' in body

    @attr(type='smoke')
    def test_update_created_service(self):
        self.create_new_service('test')
        resp, body = self.update_new_service('test')
        assert resp['status'] == '200'
        assert 'success' in body
        self.delete_service('test')

    @attr(type='positive')
    def test_create_complex_service(self):
        resp, body, post_body = self.create_complex_service('test')
        assert resp['status'] == '200'
        assert 'success' in body
        resp, body = self.get_metadata_object('services/test')
        self.delete_service('test')
        assert resp['status'] == '200'
        for k in post_body.values():
            if isinstance(k, list):
                for j in k:
                    assert j in body

    @attr(type='smoke')
    def test_get_list_all_services(self):
        resp, body = self.get_list_metadata_objects('services')
        assert resp['status'] == '200'
        assert body is not None

    @attr(type='smoke')
    def test_switch_service_parameter(self):
        self.create_complex_service('test')
        resp, body = self.switch_service_parameter('test')
        assert resp['status'] == '200'
        assert body['result'] == 'success'
        self.delete_service('test')

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1268976')
    @attr(type='negative')
    def test_switch_parameter_none_existing_service(self):
        self.assertRaises(exceptions.NotFound, self.switch_service_parameter,
                          'hupj')

    @attr(type='positive')
    def test_reset_cache(self):
        resp, body = self.reset_cache()
        assert resp['status'] == '200'
        assert body['result'] == 'success'

    @attr(type='smoke')
    def test_get_meta_info_about_service(self):
        self.create_new_service('test')
        resp, body = self.get_list_of_meta_information_about_service('test')
        self.delete_service('test')
        assert resp['status'] == '200'
        assert body['name'] == 'test'
        assert body['version'] == '0.1'

    @attr(type='negative')
    def test_get_meta_info_about_nonexistent_service(self):
        self.assertRaises(exceptions.NotFound,
                          self.get_list_of_meta_information_about_service,
                          "hupj")
