from setuptools import setup, Extension

frt_hb_convert = Extension('frt_hb_convert',
              define_macros = [('MAJOR_VERSION', '0'), ('MINOR_VERSION', '1')],
              include_dirs = ['/usr/include', '/usr/include/harfbuzz', '/usr/include/freetype2'],
              libraries = ['freetype', 'harfbuzz'],
              library_dirs = ['/usr/lib'],
              sources = ['frt_server/cmodules/frt_hb_convert.c'])

setup(name='frt_server',
              version='0.1',
              packages=['frt_server'],
              setup_requires=[
                     'pytest-runner'
              ],
              tests_require=[
                     'pytest'
              ],
              test_suite='frt_server.tests',
              ext_modules = [frt_hb_convert])

