#!/usr/bin/env python
#
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
try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import sippycode.twitter.core as twitter
import sippycode.auth.core as auth


class StatusClient(object):
  _twitter_page = 0
  _local_page = 0
  
  def __init__(self):
    self._status_cache = []

  def print_current_page(self):
    print '------------------------------'
    start_index = self._local_page * 5
    for result in self._status_cache[start_index:start_index+5]:
      print result[0]
      print result[1]
      print ''

  def get_page(self, number, client):
    old_twitter_page = self._twitter_page
    if number > 0:
      self._twitter_page = (number / 4) + 1
      self._local_page = (number - 1) % 4
    else:
      self._twitter_page = 1
      self._local_page = 0
    if old_twitter_page != self._twitter_page:
      response = client.friends_timeline(page=self._twitter_page)
      if response.status == 200:
        self._status_cache = []
        tree = ElementTree.fromstring(response.read())
        for status in tree.findall('status'):
          self._status_cache.append(
              ('%s - %s - %s' % (
                  status.findtext('user/screen_name'), 
                  status.findtext('user/name'), 
                  status.findtext('created_at')), 
              status.findtext('text')))
      else: 
        print 'Sorry, we couldn\'t read the updates from your friends.'


def main():
  command = ''
  # The pages start at 1, so we begin at zero so that the first page will
  # be fetched.
  current_page = 0
  client = get_credentialed_client()
  status_viewer = StatusClient()
  print_instructions()

  while not command.startswith('q'):
    command = raw_input(': ')
    if command.startswith('q'):
      break
    elif command.startswith('n'):
      if current_page > 0:
        current_page -= 1
      status_viewer.get_page(current_page, client)
      status_viewer.print_current_page()
    elif command.startswith('p'):
      current_page = int(raw_input('Start at page: '))
      status_viewer.get_page(current_page, client)
      status_viewer.print_current_page()
    else:
      current_page += 1
      status_viewer.get_page(current_page, client)
      status_viewer.print_current_page()

  
def print_instructions():
  print 'Commands:'
  print '  nothing or o: to see older updates.'
  print '  n: to see newer updates.'
  print '  p: to see a specific page of updates.'
  #print '  r: to read updates from a particular user.'
  print '  q: to quit.'

def get_credentialed_client():
  if os.path.exists('.twitter.creds'):
    credential_file = open('.twitter.creds', 'r')
    client = twitter.TwitterClient('', '')
    credentials = auth.BasicAuth('', '')
    credentials.basic_cookie = credential_file.read()
    client._credentials = credentials
    credential_file.close()
    return client
  else:
    return None


if __name__ == '__main__':
  main()
