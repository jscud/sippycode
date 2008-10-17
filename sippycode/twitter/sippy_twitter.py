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


import os.path
import getpass
from xml.etree import ElementTree
import sippycode.twitter.core as twitter
import sippycode.auth.core as auth


def main():
  command = ''
  current_page = 0
  print 'Welcome to the sippycode Twitter client.'
  client = get_credentialed_client()
  print_instructions()

  while not command.startswith('q'):
    command = raw_input(': ')
    if command.startswith('q'):
      break
    elif command.startswith('u'):
      message = raw_input('What are you doing?: ')
      while len(message) >= 140:
        print 'Too long!'
        message = raw_input('What are you doing?: ')
      if len(message) > 0:
        client.update(message)
    elif command.startswith('n'):
      if current_page > 0:
        current_page -= 1
      show_page(client, current_page)
    elif command.startswith('p'):
      current_page = int(raw_input('Start at page: '))
      show_page(client, current_page)
    else:
      current_page += 1
      show_page(client, current_page)

  
def print_instructions():
  print 'Commands:'
  print '  u: to post an update.'
  print '  nothing or o: to see older updates.'
  print '  n: to see newer updates.'
  print '  p: to see a specific page of updates.'
  #print '  r: to read updates from a particular user.'
  print '  q: to quit.'
  # TODO add f command to follow a user.


def get_credentialed_client():
  if os.path.exists('.twitter.creds'):
    choice = raw_input('Load credentials from file y/n (y): ')
    if not choice.startswith('n'):
      credential_file = open('.twitter.creds', 'r')
      client = twitter.TwitterClient('', '')
      credentials = auth.BasicAuth('', '')
      credentials.basic_cookie = credential_file.read()
      client._credentials = credentials
      credential_file.close()
      return client
  username = raw_input('Username: ')
  password = getpass.getpass()
  client = twitter.TwitterClient(username, password)
  choice = raw_input('Save credentials in .twitter.creds y/n (y): ')
  if not choice.startswith('n'):
    credential_file = open('.twitter.creds', 'w')
    credential_file.write(client._credentials.basic_cookie)
    credential_file.close()
  return client


def show_page(client, page_number):
  response = client.friends_timeline(page=page_number)
  if response.status == 200:
    render_statuses(response.read())
  else:
    print 'Sorry, we couldn\'t read the updates from your friends.'


def render_statuses(xml_string):
  tree = ElementTree.fromstring(xml_string)
  for status in tree.findall('status'):
    print '%s - %s - %s' % (
        status.findtext('user/screen_name'),
        status.findtext('user/name'),
        status.findtext('created_at'))
    print status.findtext('text')
    print ''
   

if __name__ == '__main__':
  main()
