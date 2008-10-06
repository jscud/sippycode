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


import StringIO
from sippycode.http import core


class MockHttpClient(object):
  
  def _http_request(self):
    pass
    
class EchoHttpClient(object):
  
  def request(self, http_request):
    return self._http_request(http_request.host, http_request.method, 
        http_request.uri, http_request.scheme, http_request.port, 
        http_request.headers, http_request._body_parts)

  def _http_request(self, host, method, uri, scheme=None,  port=None, 
      headers=None, body_parts=None):
    body = StringIO.StringIO()
    response = core.HttpResponse(status=200, reason='OK', body=body)
    if headers is None:
      response._headers = {}
    else:
      response._headers = headers.copy()
    response._headers['Echo-Host'] = '%s:%s' % (host, str(port))
    response._headers['Echo-Uri'] = uri
    response._headers['Echo-Scheme'] = scheme
    response._headers['Echo-Method'] = method
    for part in body_parts:
      if isinstance(part, str):
        body.write(part)
      elif hasattr(part, 'read'):
        body.write(part.read())
    body.seek(0)
    return response
