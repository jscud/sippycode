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


import unittest
from sippycode.auth import core as auth_core
from sippycode.http import core as http_core


class BasicAuthTest(unittest.TestCase):
  
  def test_modify_request(self):
    http_request = http_core.HttpRequest()
    credentials = auth_core.BasicAuth('Aladdin', 'open sesame')
    self.assert_(credentials.basic_cookie == 'QWxhZGRpbjpvcGVuIHNlc2FtZQ==')
    credentials.modify_request(http_request)
    self.assert_(http_request.headers[
        'Authorization'] == 'Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==')


def suite():
  return unittest.TestSuite((unittest.makeSuite(BasicAuthTest,'test'),))


if __name__ == '__main__':
  unittest.main()
