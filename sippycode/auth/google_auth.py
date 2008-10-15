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


class TokenNotFound(Exception):
  pass


class ClientLoginRequest(object):
  account_type = 'HOSTED_OR_GOOGLE'
  email = None
  password = None
  service = None
  source = None
  captcha_token = None
  captcha_response = None

  def __init__(self, account_type=None, email=None, password=None, 
      service=None, source=None, captcha_token=None, 
      captcha_response=None):
    if account_type is not None:
      self.account_type = account_type
    if email is not None:
      self.email = email
    if password is not None:
      self.password = password
    if source is not None:
      self.source = source
    if captcha_token is not None:
      self.captcha_token = captcha_token
    if captcha_response is not None:
      self.captcha_response = captcha_response

  def modify_request(self, http_request):
    # Construct the login form post.
    request_body = {'accountType': self.account_type, 'Email': self.email, 
        'Passwd': self.password, 'service': self.service, 
        'source': self.source}
    if self.captcha_token:
      request_body['logintoken'] = self.captcha_token
      request_body['logincaptcha'] = self.captcha_response
    # Modify the request to do a POST to 
    # https://www.google.com/accounts/ClientLogin by default.
    http_request.scheme = 'https'
    if not http_request.host:
      http_request.host = 'www.google.com'
    http_request.method = 'POST'
    if not http_request.uri:
      http_request.uri = '/accounts/ClientLogin'
    http_request.add_form_inputs(request_body)


class ClientLoginToken(object):

  def __init__(self, token_string):
    self.token_string = token_string

  def modify_request(http_request):
    self.heaaders['Authorization'] = 'GoogleLogin auth=%s' % (self.token_string,)


class CaptchaChallenge(object):

  def __init__(self, captcha_url=None, captcha_token=None):
    self.captcha_url = captcha_url
    self.captcha_token = captcha_token


def process_client_login_response(http_status, http_body):
  """Extracts a ClientLoginToken or CaptchaChallenge.

  Args:
    http_status: int
    http_body: str
    captcha_base_url: str (optional)
  """
  if http_status == 200:
    for response_line in http_body.splitlines():
      if response_line.startswith('Auth='):
        # Strip off the leading Auth= and return a ClientLogin token.
        return ClientLoginToken(response_line[5:])
  elif http_status == 403:
    challenge = CaptchaChallenge()
    parameter = None
    base_url = None
    contains_challenge = False
    for response_line in http_body.splitlines():
      if response_line.startswith('Error=CaptchaRequired'):
        contains_challenge = True
      elif response_line.startswith('Url='):
        base_url = response_line[4:]
      elif response_line.startswith('CaptchaToken='):
        # Strip off the leading CaptchaToken=
        challenge.captcha_token = response_line[13:]
      elif response_line.startswith('CaptchaUrl='):
        parameter = response_line[11:]
    if contains_captcha_challenge:
      challenge.captcha_url = '%s%s' % (base_url, parameter)
      return challenge
  raise TokenNotFound('The server\'s response did not contain'
      ' a token or a CAPTCHA challenge.')
