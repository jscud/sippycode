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

class ClientLoginRequest(object):
  account_type = 'HOSTED_OR_GOOGLE'
  email = None
  password = None
  service = None
  source = None
  login_token = None
  login_captcha = None

  def __init__(self, account_type=None, email=None, password=None, 
      service=None, source=None, login_token=None, 
      login_captcha=None):
    if account_type is not None:
      self.account_type = account_type
    if email is not None:
      self.email = email
    if password is not None:
      self.password = password
    if source is not None:
      self.source = source
    if login_token is not None:
      self.login_token = login_token
    if login_captcha is not None:
      self.login_captcha = login_captcha

  def modify_request(http_request):
    pass


class ClientLooginToken(object):

  def __init__(self, token_string):
    pass
