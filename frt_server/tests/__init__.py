import os
import unittest
import tempfile
import eve.tests
import json
import shutil
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL

os.environ['FRT_TESTING'] = '1'

import frt_server.config
from frt_server.run import create_app, setup_database
from frt_server.tables import User, Family

class TestMinimal(eve.tests.TestMinimal):
    def setUp(self):
        self.clean_upload_folder()
        self.addCleanup(self.clean_upload_folder)
        self.addCleanup(self.drop_database)

        self.this_directory = os.path.dirname(os.path.realpath(__file__))

        self.app = create_app()
        self.setup_database()
        self.app.app_context().push()
        self.test_client = self.app.test_client()
        self.cachedApiToken = None

        self.domain = self.app.config['DOMAIN']

    def tearDown(self):
        self.drop_database()
        del self.app

    def clean_upload_folder(self):
        if os.path.exists(frt_server.config.UPLOAD_FOLDER):
            shutil.rmtree(frt_server.config.UPLOAD_FOLDER)

    def setup_database(self):
        self.connection = self.app.data.driver
        # we get our own minimal subset of sample data for speed
        setup_database(self.app, populate_sample_data=False)

        eva = User(username='Eva', email='eve@evil.com', password='eveisevil')
        self.connection.session.add(eva)
        self.connection.session.commit()

    def drop_database(self):
        self.connection.session.remove()
        self.connection.drop_all()

    def get(self, url):
        headers = [
            ('Content-Type', 'application/json'),
            ('Authorization', self.cachedApiToken)
        ]
        response = self.test_client.get(url, headers=headers)
        return self.parse_response(response)

    def download(self, url):
        headers = [
            ('Authorization', self.cachedApiToken)
        ]
        response = self.test_client.get(url, headers=headers)
        return response

    def post(self, url, data):
        """post data as a json object to url"""
        headers = [
            ('Content-Type', 'application/json'),
            ('Authorization', self.cachedApiToken)
        ]
        response = self.test_client.post(url, data=json.dumps(data), headers=headers)
        return self.parse_response(response)

    def upload_file(self, url, field_name, path, fields={}):
        """upload file in a multipart/form-data request with field_name. path is relative
        to project root"""
        with open(os.path.join(self.this_directory, '..', '..', path), 'rb') as f:
            fields.update({field_name: f})
            response = self.test_client.post(url,
                    headers=[
                        ('Content-Type', 'multipart/form-data'),
                        ('Authorization', self.cachedApiToken)
                    ],
                    data=fields)
            return self.parse_response(response)

    def upload_font_file(self, family_id, file_path, message=None):
        family = self.connection.session.query(Family).get(family_id)
        user = self.connection.session.query(User).get(self.user_id)
        family.process_filename(os.path.join(self.this_directory, '..', '..', file_path), user, message or 'commit message here')

    def login_as(self, email, password):
        """save the auth token from the given user for all future requests"""
        data, status = self.login(email, password)
        assert status == 200
        self.cachedApiToken = data['token']
        self.user_id = data['user_id']
        return data, status

    def logout(self):
        """not an actual request, just resets the cached token"""
        self.cachedApiToken = None

    def login(self, email, password):
        return self.post('/login', dict(email=email, password=password))

