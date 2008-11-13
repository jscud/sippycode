#   Copyright 2008 Jeffrey William Scudder
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


from distutils.core import setup


setup(
    name='sippycode',
    version='0.1',
    description='Open source projects from the sippycode team',
    long_description = """\
The collection includes a library for making HTTP requests.
""",
    author='Jeffrey William Scudder',
    author_email='me@jeffscudder.com',
    license='Apache 2.0',
    url='http://code.google.com/p/sippycode',
    packages=['sippycode', 'sippycode.http', 'sippycode.auth',
              'sippycode.twitter', 'sippycode.xml',
              'sippycode_mocks', 'sippycode_mocks.http',
              'sippycode_tests', 'sippycode_tests.mocks',
              'sippycode_tests.http', 'sippycode_tests.auth',
              'sippycode_tests.xml_tests'],
    package_dir = {'sippycode':'sippycode', 
                   'sippycode_mocks':'sippycode_mocks',
                   'sippycode_tests':'sippycode_tests'}
)

