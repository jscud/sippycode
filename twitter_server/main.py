from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import urlfetch
import base64
import urllib


class UserPrefs(db.Model):
  creds = db.TextProperty()


def load_credentials():
  user = users.get_current_user()
  if user:
    user_id = user.user_id()
    credentials = UserPrefs.get_by_key_name('c%s' % user_id)
    if credentials:
      return credentials.creds
  return None


class SetCredentials(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(
        '<html>'
        '<body>'
          '<div style="float: right;">'
            '<a href="%s">Sign Out</a>'
          '</div>'
          '<form action="/set_credentials" method="post">'
            '<div><input type="text" name="uname"/></div>'
            '<div><input type="password" name="pword"/></div>'
            '<div><input type="submit" value="Set Credentials"></div>'
          '</form>'
        '</body>'
        '</html>' % users.create_logout_url('/'))

  def post(self):
    uname = self.request.get('uname')
    pword = self.request.get('pword')
    user = users.get_current_user()
    if user:
      user_id = user.user_id()
      credentials = UserPrefs.get_or_insert('c%s' % user_id)
      header = base64.encodestring('%s:%s' % (uname, pword)).strip()
      credentials.creds = header
      credentials.put()
    self.redirect('/')


class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    credentials = load_credentials()
    if credentials is None:
      self.redirect('/set_credentials')
    self.response.out.write(
       '<html>'
         '<head>'
           '<script src="/api.js"></script>'
           '<script src="http://www.json.org/json2.js"></script>'
         '</head>'
         '<body onload="start()"><div style="float: right;">'
           '<a href="%s">Sign Out</a></div><div id="container">:-)</div>'
           '<div id="debug"></div>'
         '</body>'
       '</html>' % (users.create_logout_url('/')))


class Api(webapp.RequestHandler):
  def post(self):
    self.response.headers['Content-Type'] = 'text/plain'    
    credentials = load_credentials()
    if credentials is None:
      self.response.set_status(403, 'No credentials')
      self.response.out.write('Error: No credentials.')
      return
    action = self.request.headers['action']
    if action == 'tweet': 
      message = self.request.body
      form_fields = {
          'status': message,
          'source': 'sippycode',
      }
      form_data = urllib.urlencode(form_fields)
      response = urlfetch.fetch(
          'http://twitter.com/statuses/update.json', form_data, urlfetch.POST,
          headers={'Authorization': 'Basic %s' % (credentials,)})
      self.response.out.write(response.content)
    elif action == 'read':
      if 'after' in self.request.headers:
        url = 'http://twitter.com/statuses/friends_timeline.json?since_id=%s' % self.request.headers['after']
      elif 'before' in self.request.headers:
        url = 'http://twitter.com/statuses/friends_timeline.json?max_id=%s' % self.request.headers['before']
      else:
        url = 'http://twitter.com/statuses/friends_timeline.json' 
      response = urlfetch.fetch(
          url, headers={'Authorization': 'Basic %s' % (credentials,)})
      self.response.out.write(response.content)
    else:
      self.response.set_status(404, 'Unknown Action')
      self.response.out.write('Error: unknown action: %s' % action)


application = webapp.WSGIApplication(
                                     [('/api', Api),
                                      ('/set_credentials', SetCredentials),
                                      ('/', MainPage)],
                                     debug=True)


def main():
  run_wsgi_app(application)


if __name__ == "__main__":
  main()
