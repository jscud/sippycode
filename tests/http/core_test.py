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
from sippycode.http import core


class UriTest(unittest.TestCase):
  
  def test_parse_uri(self):
    uri = core.parse_uri('http://www.google.com/test?q=foo&z=bar')
    self.assert_(uri.scheme == 'http')
    self.assert_(uri.host == 'www.google.com')
    self.assert_(uri.port is None)
    self.assert_(uri.path == '/test')
    self.assert_(uri.query == {'z':'bar', 'q':'foo'})
    
  def test_stamp_no_request(self):
    uri = core.parse_uri('http://www.google.com/test?q=foo&z=bar')
    request = uri.stamp()
    self.assert_(request.scheme == 'http')
    self.assert_(request.host == 'www.google.com')
    self.assert_(request.port == 80)
    self.assert_(request.uri.startswith('/test?'))
    self.assert_(request.method is None)
    self.assert_(request.headers == {})
    self.assert_(request.body is None)
    
  def test_stamp_http_with_set_port(self):
    request = core.HttpRequest(port=8080, method='POST', body='hello')
    uri = core.parse_uri('//example.com/greet')
    self.assert_(uri.query == {})
    self.assert_(uri.get_relative_path() == '/greet')
    self.assert_(uri.host == 'example.com')
    self.assert_(uri.port is None)
    
    uri.stamp(request)
    self.assert_(request.host == 'example.com')
    self.assert_(request.scheme == 'http')
    self.assert_(request.port == 8080)
    self.assert_(request.uri == '/greet')
    self.assert_(request.method == 'POST')
    
  def test_stamp_use_default_ssl_port(self):
    request = core.HttpRequest(scheme='https', method='PUT', body='hello')
    uri = core.parse_uri('/greet')
    uri.stamp(request)
    self.assert_(request.host is None)
    self.assert_(request.scheme == 'https')
    self.assert_(request.port == 443)
    self.assert_(request.uri == '/greet')
    self.assert_(request.method == 'PUT')
    

def get_suite():
  pass

  
if __name__ == '__main__':
  unittest.main()
