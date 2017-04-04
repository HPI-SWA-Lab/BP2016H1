from sqlalchemy import Column, String, inspect
from sqlalchemy.orm import relationship

from frt_server.common import CommonColumns
from frt_server.font import Font
import frt_server.config

import os
import glob
import subprocess
import shutil
import zipfile

from werkzeug.utils import secure_filename

class Family(CommonColumns):
    __tablename__ = 'family'
    family_name = Column(String(300))
    fonts = relationship('Font', back_populates='family')

    def is_glyphs_file(self, filename):
        return filename.endswith('.glyphs')

    def is_ufo_file(self, filename):
        return filename.endswith('.ufo.zip')

    def source_folder_path(self):
        """Path to the folder containing all the family sources"""
        return os.path.join(frt_server.config.FAMILY_UPLOAD_FOLDER, str(self._id))

    def ensure_source_folder_exists(self):
        """Ensure that the folder at source_folder_path exists"""
        folder = self.source_folder_path()
        if not os.path.exists(folder):
            os.makedirs(folder)

    def clean_folders(self):
        """Delete all our associated folders"""
        if os.path.exists(self.source_folder_path()):
            shutil.rmtree(self.source_folder_path())

    def unzip_file(self, filename):
        with zipfile.ZipFile(os.path.join(self.source_folder_path(), filename), "r") as ufo_zip_file:
            ufo_zip_file.extractall(self.source_folder_path())

    def convert_font_after_upload(self, filename):
        """invoke fontmake in our source folder. no cleanup performed after"""
        type_parameter = None
        if self.is_glyphs_file(filename):
            type_parameter = "-g"
            temporary_filename = filename
        if self.is_ufo_file(filename):
            self.unzip_file(filename)
            temporary_filename = filename[:-4]
            type_parameter = "-u"

        subprocess.run(['fontmake', type_parameter, temporary_filename, '--no-production-names', '-o', 'otf', '--verbose', 'CRITICAL'],
                cwd=self.source_folder_path())

    def create_uploaded_font(self, font_name, ufo_filename, otf_filename, user):
        font = Font(font_name=font_name, author_id=user._id)
        self.fonts.append(font)
        session = inspect(self).session
        session.commit()
        session.refresh(font)

        font.clean_folders()
        font.ensure_folder_exists()
        return font

    def process_file(self, family_file, user):
        """convert a glyphs or ufo file to (ufo and) otf, create all associated Font entities, move files to the right folders
        we get:
        family/3/sourceFile.glyphs
        font/7/ufo/myFont.ufo
        font/7/otf/myFont.otf"""

        sanitized_filename = secure_filename(os.path.basename(family_file.filename))

        self.ensure_source_folder_exists()
        family_file.save(os.path.join(self.source_folder_path(), sanitized_filename))
        self.convert_font_after_upload(sanitized_filename)

        source_otf_path = os.path.join(self.source_folder_path(), 'master_otf')

        otf_filenames = [os.path.basename(filename) for filename in glob.glob(source_otf_path + '/*.otf')]
        if len(otf_filenames) < 1:
            raise FileNotFoundError('No otf files were generated')

        if self.is_ufo_file(sanitized_filename):
            return self.process_ufo_file(sanitized_filename[:-4], otf_filenames[0], user)
        else:
            return self.process_glyphs_file(sanitized_filename, otf_filenames, user)

    def process_glyphs_file(self, glyphs_filename, otf_filenames, user):
        source_otf_path = os.path.join(self.source_folder_path(), 'master_otf')
        source_ufo_path = os.path.join(self.source_folder_path(), 'master_ufo')

        for otf_filename in otf_filenames:
            font_name = otf_filename[:-4]
            ufo_filename = font_name + '.ufo'
            font = self.create_uploaded_font(font_name, ufo_filename, otf_filename, user)

            shutil.move(os.path.join(source_ufo_path, ufo_filename), os.path.join(font.ufo_folder_path(), ufo_filename))
            shutil.move(os.path.join(source_otf_path, otf_filename), font.otf_folder_path())

        shutil.rmtree(source_ufo_path)
        shutil.rmtree(source_otf_path)

    def process_ufo_file(self, ufo_filename, otf_filename, user):
        source_otf_path = os.path.join(self.source_folder_path(), 'master_otf')
        font_name = otf_filename[:-4]

        font = self.create_uploaded_font(font_name, ufo_filename, otf_filename, user)

        shutil.move(os.path.join(self.source_folder_path(), ufo_filename), os.path.join(font.ufo_folder_path(), ufo_filename))
        shutil.move(os.path.join(source_otf_path, otf_filename), os.path.join(font.otf_folder_path(), otf_filename))
        shutil.rmtree(source_otf_path)
