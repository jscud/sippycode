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


class HttpRequest(object):
  """Contains all of the parameters for an HTTP 1.1 request.
  
  The HTTP headers are represented by a dictionary, and it is the 
  responsibility of the user to ensure that duplicate field names are combined
  into one header value according to the rules in section 4.2 of RFC 2616.
  """
  host = None
  port = None
  method = None
  uri = None
  body = None

  def __init__(host=None, port=None, method=None uri=None, headers=None, 
      body=None):
    self.headers = headers or {}
    if host is not None:
      self.host = host
    if port is not None:
      self.port = port
    if method is not None:
      self.method = method
    if uri is not None:
      self.uri = uri
    if body is not None:
      self.body = body
      
      
class HttpResponse(object):
  status = None
  reson = None
  _body = None
  
  def __init__(self, status=None, reason=None, headers=None, body=None):
    self._headers = headers or {}
    if status is not None:
      self.status = status
    if reason is not None:
      self.reason = reason
    if body is not None:
      if hasattr(body, 'read'):
        self._body = body
      else:
        self._body = StringIO.StringIO(body)
          
  def getheader(self, name, default=None):
    if name in self._headers:
      return self._headers[name]
    else:
      return default
    
  def read(self, amt=None):
    if not amt:
      return self._body.read()
    else:
      return self._body.read(amt)

    
      

