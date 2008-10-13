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
import StringIO


class UriTest(unittest.TestCase):
  
  def test_parse_uri(self):
    uri = core.parse_uri('http://www.google.com/test?q=foo&z=bar')
    self.assert_(uri.scheme == 'http')
    self.assert_(uri.host == 'www.google.com')
    self.assert_(uri.port is None)
    self.assert_(uri.path == '/test')
    self.assert_(uri.query == {'z':'bar', 'q':'foo'})
    
  def test_modify_request_no_request(self):
    uri = core.parse_uri('http://www.google.com/test?q=foo&z=bar')
    request = uri.modify_request()
    self.assert_(request.scheme == 'http')
    self.assert_(request.host == 'www.google.com')
    # If no port was provided, the HttpClient is responsible for determining
    # the default.
    self.assert_(request.port is None)
    self.assert_(request.uri.startswith('/test?'))
    self.assert_(request.method is None)
    self.assert_(request.headers == {})
    self.assert_(request._body_parts == [])
    
  def test_modify_request_http_with_set_port(self):
    request = core.HttpRequest(port=8080, method='POST')
    request.add_body_part('hello', 'text/plain') 
    uri = core.parse_uri('//example.com/greet')
    self.assert_(uri.query == {})
    self.assert_(uri._get_relative_path() == '/greet')
    self.assert_(uri.host == 'example.com')
    self.assert_(uri.port is None)
    
    uri.modify_request(request)
    self.assert_(request.host == 'example.com')
    # If no scheme was provided, the URI will not add one, but the HttpClient
    # should assume the request is HTTP.
    self.assert_(request.scheme is None)
    self.assert_(request.port == 8080)
    self.assert_(request.uri == '/greet')
    self.assert_(request.method == 'POST')
    self.assert_(request.headers['Content-Type'] == 'text/plain')
    
  def test_modify_request_use_default_ssl_port(self):
    request = core.HttpRequest(scheme='https', method='PUT')
    request.add_body_part('hello', 'text/plain')
    uri = core.parse_uri('/greet')
    uri.modify_request(request)
    self.assert_(request.host is None)
    self.assert_(request.scheme == 'https')
    # If no port was provided, leave the port as None, it is up to the 
    # HttpClient to set the correct default port.
    self.assert_(request.port is None)
    self.assert_(request.uri == '/greet')
    self.assert_(request.method == 'PUT')
    self.assert_(request.headers['Content-Type'] == 'text/plain')
    self.assert_(len(request._body_parts) == 1)
    self.assert_(request._body_parts[0] == 'hello')

  def test_to_string(self):
    uri = core.Uri(host='www.google.com', query={'q':'sippycode'})
    uri_string = uri._to_string()
    self.assert_(uri_string == 'http://www.google.com/?q=sippycode')


class HttpRequestTest(unittest.TestCase):

  def test_request_with_one_body_part(self):
    request = core.HttpRequest()
    self.assert_(len(request._body_parts) == 0)
    self.assert_('Content-Length' not in request.headers)
    self.assert_(not 'Content-Type' in request.headers)
    self.assert_(not 'Content-Length' in request.headers)
    request.add_body_part('this is a test', 'text/plain')
    self.assert_(len(request._body_parts) == 1)
    self.assert_(request.headers['Content-Type'] == 'text/plain')
    self.assert_(request._body_parts[0] == 'this is a test')
    self.assert_(request.headers['Content-Length'] == str(len(
        'this is a test')))
    
  def test_add_file_without_size(self):
    virtual_file = StringIO.StringIO('this is a test')
    request = core.HttpRequest()
    try:
      request.add_body_part(virtual_file, 'text/plain')
      self.fail('We should have gotten an UnknownSize error.')
    except core.UnknownSize:
      pass
    request.add_body_part(virtual_file, 'text/plain', len('this is a test'))
    self.assert_(len(request._body_parts) == 1)
    self.assert_(request.headers['Content-Type'] == 'text/plain')
    self.assert_(request._body_parts[0].read() == 'this is a test')
    self.assert_(request.headers['Content-Length'] == str(len(
        'this is a test')))

  def test_copy(self):
    request = core.HttpRequest(scheme='https', host='www.google.com', 
        method='POST', headers={'test':'1', 'ok':'yes'})
    request.add_body_part('body1', 'text/plain')
    request.add_body_part('<html>body2</html>', 'text/html')
    copied = request._copy()
    self.assert_(request.scheme == copied.scheme)
    self.assert_(request.host == copied.host)
    self.assert_(request.method == copied.method)
    self.assert_(request.uri == copied.uri)
    self.assert_(request.headers == copied.headers)
    self.assert_(request._body_parts == copied._body_parts)
    copied.headers['test'] = '2'
    copied._body_parts[1] = '<html>body3</html>'
    self.assert_(request.headers != copied.headers)
    self.assert_(request._body_parts != copied._body_parts)


def suite():
  return unittest.TestSuite((unittest.makeSuite(UriTest,'test'),
                             unittest.makeSuite(HttpRequestTest,'test')))

 
if __name__ == '__main__':
  unittest.main()
