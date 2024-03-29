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
#   limitations under the License

import unittest
import StringIO
import os.path
from sippycode_mocks.http import core as mock_core
from sippycode.http import core
from sippycode_tests import config

class EchoClientTest(unittest.TestCase):
  
  def test_echo_response(self):
    client = mock_core.EchoHttpClient()
    # Send a bare-bones POST request.
    request = core.HttpRequest(host='www.jeffscudder.com', method='POST', 
        uri='/')
    request.add_body_part('hello world!', 'text/plain')
    response = client.request(request)
    self.assert_(response.getheader('Echo-Host') == 'www.jeffscudder.com:None')
    self.assert_(response.getheader('Echo-Uri') == '/')
    self.assert_(response.getheader('Echo-Scheme') is None)
    self.assert_(response.getheader('Echo-Method') == 'POST')
    self.assert_(response.getheader('Content-Length') == str(len(
        'hello world!')))
    self.assert_(response.getheader('Content-Type') == 'text/plain')
    self.assert_(response.read() == 'hello world!')
    
    # Send a multipart request.
    request = core.HttpRequest(scheme='https', host='www.jeffscudder.com', 
        port=8080, method='POST', uri='/multipart?test=true&happy=yes', 
        headers={'Authorization':'Test xyzzy', 'Testing':'True'})
    request.add_body_part('start', 'text/plain')
    request.add_body_part(StringIO.StringIO('<html><body>hi</body></html>'),
                          'text/html', len('<html><body>hi</body></html>'))
    request.add_body_part('alert("Greetings!")', 'text/javascript')
    response = client.request(request)
    self.assert_(response.getheader('Echo-Host') == 'www.jeffscudder.com:8080')
    self.assert_(
        response.getheader('Echo-Uri') == '/multipart?test=true&happy=yes')
    self.assert_(response.getheader('Echo-Scheme') == 'https')
    self.assert_(response.getheader('Echo-Method') == 'POST')
    self.assert_(response.getheader('Content-Type') == (
        'multipart/related; boundary="%s"' % (core.MIME_BOUNDARY,)))
    expected_body = ('Media multipart posting'
                     '\r\n--%s\r\n'
                     'Content-Type: text/plain\r\n\r\n'
                     'start'
                     '\r\n--%s\r\n'
                     'Content-Type: text/html\r\n\r\n'
                     '<html><body>hi</body></html>'
                     '\r\n--%s\r\n'
                     'Content-Type: text/javascript\r\n\r\n'
                     'alert("Greetings!")'
                     '\r\n--%s--') % (core.MIME_BOUNDARY, 
        core.MIME_BOUNDARY, core.MIME_BOUNDARY, core.MIME_BOUNDARY,)
    self.assert_(response.read() == expected_body)
    self.assert_(response.getheader('Content-Length') == str(
        len(expected_body)))

class MockHttpClientTest(unittest.TestCase):

  def setUp(self):
    self.client = mock_core.MockHttpClient()

  def test_respond_with_recording(self):
    request = core.HttpRequest(method='GET')
    core.parse_uri('http://www.google.com/').modify_request(request)
    self.client.add_response(request, 200, 'OK', body='Testing')
    response = self.client.request(request)
    self.assert_(response.status == 200)
    self.assert_(response.reason == 'OK')
    self.assert_(response.read() == 'Testing')

  def test_save_and_load_recordings(self):
    request = core.HttpRequest(method='GET')
    core.parse_uri('http://www.google.com/').modify_request(request)
    self.client.add_response(request, 200, 'OK', body='Testing')
    response = self.client.request(request)
    self.client._save_recordings('test_save_and_load_recordings')
    self.client._recordings = []
    response = self.client.request(request)
    self.assert_(response is None)
    self.client._load_recordings('test_save_and_load_recordings')
    response = self.client.request(request)
    self.assert_(response.status == 200)
    self.assert_(response.reason == 'OK')
    self.assert_(response.read() == 'Testing')

  def test_use_recordings(self):
    request = core.HttpRequest(method='GET')
    core.parse_uri('http://www.google.com/').modify_request(request)
    self.client._load_or_use_client('test_use_recordings', core.HttpClient())
    response = self.client.request(request)
    if self.client.real_client:
      self.client._save_recordings('test_use_recordings')
    self.assert_(response.status == 200)
    self.assert_(response.reason == 'OK')
    self.assert_(response.getheader('server') == 'gws')
    body = response.read()
    self.assert_(body.startswith('<html><head>'))

    
def suite():
  return unittest.TestSuite((unittest.makeSuite(EchoClientTest, 'test'),
                             unittest.makeSuite(MockHttpClientTest, 'test')))


if __name__ == '__main__':
  unittest.main()
