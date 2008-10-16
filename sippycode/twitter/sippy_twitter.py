#    Copyright 2008 Jeffrey William Scudder
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

import sippycode.http.core as http_core
import sippycode.auth.core as auth_core

class TwitterClient(object):

  def __init__(self, username, password):
    self._credentials = auth_core.BasicAuth(username, password)

  def update(self, message):
    request = http_core.HttpRequest(method='POST')
    http_core.parse_uri(
        'http://twitter.com/statuses/update.xml').modify_request(request)
    request.add_form_inputs({'status': message})
    self._credentials.modify_request(request)
    client = http_core.HttpClient()
    response = client.request(request)
    return response
