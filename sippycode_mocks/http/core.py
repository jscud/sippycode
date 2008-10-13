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
import pickle
import os.path
from sippycode.http import core
from sippycode_tests import config


class MockHttpClient(object):

  real_client = None

  def __init__(self, recordings=None, real_client=None):
    self._recordings = recordings or []
    if real_client is not None:
      self.real_client = real_client

  def add_response(self, http_request, status, reason, headers=None, 
      body=None):
    if body is not None:
      if hasattr(body, 'read'):
        copied_body = body.read()
      else:
        copied_body = body
    response = core.HttpResponse(status, reason, headers, copied_body)
    # TODO Screub the request and the response.
    self._recordings.append((http_request._copy(), response))
  
  def request(self, http_request):
    """Provide a recorded response, or record a response for replay.

    If the real_client is set, the request will be made using the
    real_client, and the response from the server will be recorded.
    If the real_client is None (the default), this method will examine
    the recordings and find the first which matches. 
    """
    request = http_request._copy()
    _scrub_request(request)
    if self.real_client is None:
      for recording in self._recordings:
        if _match_request(recording[0], request):
          return recording[1]
    else:
      response = self.real_client.request(http_request)
      _scrub_response(response)
      self.add_response(request, response.status, response.reason, 
          dict(response.getheaders()), response.read())
      # Return the recording which we just added.
      return self._recordings[-1][1]
    return None
    
  def _save_recordings(self, filename):
    recording_file = open(os.path.join(config.http_recordings_directory, 
        filename), 'wb')
    pickle.dump(self._recordings, recording_file)
    pass

  def _load_recordings(self, filename):
    recording_file = open(os.path.join(config.http_recordings_directory, 
        filename), 'rb')
    self._recordings = pickle.load(recording_file)

  def _load_or_use_client(self, filename, http_client):
    if os.path.exists(os.path.join(config.http_recordings_directory, filename)):
      self._load_recordings(filename)
    else:
      self.real_client = http_client

def _match_request(http_request, stored_request):
  """Determines whether a request is similar enough to a stored request 
     to cause the stored response to be returned."""
  return True

def _scrub_request(http_request):
  pass

def _scrub_response(http_response):
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
