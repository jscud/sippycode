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
import urlparse
import urllib


class HttpRequest(object):
  """Contains all of the parameters for an HTTP 1.1 request.
  
  The HTTP headers are represented by a dictionary, and it is the 
  responsibility of the user to ensure that duplicate field names are combined
  into one header value according to the rules in section 4.2 of RFC 2616.
  """
  scheme = None
  host = None
  port = None
  method = None
  uri = None
  body = None

  def __init__(self, scheme=None, host=None, port=None, method=None, uri=None, 
      headers=None, body=None):
    """
    Args:
      uri: str The relative path inclusing escaped query parameters.
    """
    self.headers = headers or {}
    if scheme is not None:
      self.scheme = scheme
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
      
      
class Uri(object):
  """A URI as used in HTTP 1.1"""
  scheme = None
  host = None
  port = None
  path = None
  
  def __init__(self, scheme=None, host=None, port=None, path=None, query=None):
    self.query = query or {}
    if scheme is not None:
      self.scheme = scheme
    if host is not None:
      self.host = host
    if port is not None:
      self.port = port
    if path:
      self.path = path
      
  def _get_query_string(self):
    param_pairs = []
    for key, value in self.query.iteritems():
      param_pairs.append('='.join((urllib.quote_plus(key), 
          urllib.quote_plus(str(value)))))
    return '&'.join(param_pairs)

  def get_full_path(self):
    """Returns the path with the query parameters escaped and appended."""
    param_string = self._get_query_string()
    if param_string:
      return '?'.join([self.path, param_string])
    else:
      return self.path
      
  def stamp(self, http_request=None):
    """Sets HTTP request components based on the URI."""
    if http_request is None:
      http_request = HttpRequest()
    # Determine the correct scheme.
    # The default scheme is 'http'.
    # TODO
    if self.scheme:
      http_request.scheme = self.scheme
    elif (self.scheme is None and http_request.scheme is None 
        and self.port != 443):
      http_request.scheme = 'http'
    elif (self.scheme is None and http_request.scheme is None 
        and self.port == 443):
      http_request.scheme = 'https'
    if self.port:
      http_request.port = self.port
    if not self.port and not http_request.port and (
        self.scheme == 'http' or self.scheme is None):
      http_request.port = 80
    elif not self.port and not http_request.port and self.scheme == 'https':
      http_request.port = 443
    if self.host:
      http_request.host = self.host
    # Set the relative uri path 
    if self.path:
      http_request.uri = self.get_full_path()
    elif not self.path and self.query:
      http_request.uri = '/%s' % self.get_full_path()
    elif not self.path and not self.query and not http_request.uri:
      http_request.uri = '/'
    return http_request

    
def parse_uri(uri_string):
  """Creates a Uri object which corresponds to the URI string.
  
  This method can accept partial URIs, but it will leave missing
  members of the Uri unset.
  """
  parts = urlparse.urlparse(uri_string)
  uri = Uri()
  if parts[0]:
    uri.scheme = parts[0]
  if parts[1]:
    host_parts = parts[1].split(':')
    if host_parts[0]:
      uri.host = host_parts[0]
    if len(host_parts) > 1:
      uri.port = int(host_parts[1])
  if parts[2]:
    uri.path = parts[2]
  if parts[4]:
    param_pairs = parts[4].split('&')
    for pair in param_pairs:
      pair_parts = pair.split('=')
      if len(pair_parts) > 1:
        uri.query[urllib.unquote_plus(pair_parts[0])] = (
            urllib.unquote_plus(pair_parts[1]))
      elif len(pair_parts) == 1:
        uri.query[urllib.unquote_plus(pair_parts[0])] = None
  return uri
      

