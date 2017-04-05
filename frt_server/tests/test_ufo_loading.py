from frt_server.tests import TestMinimal
from frt_server.tables import Family, Font

from sqlalchemy.orm import joinedload

import json
import os

class UfoLoadingTestCase(TestMinimal):
    def setUp(self):

        super().setUp()

        self.login_as('Eva', 'eveisevil')

        family = Family(family_name='Riblon')

        session = self.connection.session
        session.add(family)
        session.commit()
        session.refresh(family)

        self.family_id = family._id

        data, status = self.upload_file('/family/{}/upload'.format(self.family_id), 'file', 'testFiles/RiblonSans/RiblonSans.ufo.zip')
        self.assertEqual(status, 200)

        #session.refresh(family)
        family = session.query(Family).get(self.family_id)
        self.font_id = family.fonts[0]._id

    def test_load_contents_plist(self):
        query = json.dumps({"glyphs": None})
        data, status = self.get('/font/{}/ufo?query={}'.format(self.font_id, query))

        self.assertIsNotNone(data)
        glyphs = data['glyphs']
        self.assertIsNotNone(glyphs)

        self.assertEqual(glyphs, {"A": "A_.glif", "a": "a.glif", "s": "s.glif", "space": "space.glif"})
        # our plist SHOULD contain 4 different entries
        self.assertEqual(len(glyphs), 4)

    def test_get_fontinfo_plist(self):
        query = json.dumps({"fontinfo": None})
        data, status = self.get('/font/{}/ufo?query={}'.format(self.font_id, query))

        # random sample of data in the response
        self.assertIsNotNone(data)
        fontinfo = data['fontinfo']
        self.assertIsNotNone(fontinfo)
        self.assertTrue('ascender' in fontinfo)
        self.assertEqual(fontinfo["ascender"], 800)
        self.assertTrue('unitsPerEm' in fontinfo)
        self.assertEqual(fontinfo["unitsPerEm"], 1000)
        # our plist SHOULD contain 26 different entries
        self.assertEqual(len(fontinfo), 26)

    def test_get_ufo(self):
        data, status = self.get('font/{}/glyphs/')
