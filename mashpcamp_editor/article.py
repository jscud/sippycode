from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
import urllib
from xml.etree import cElementTree as ElementTree
import logging


# Sign up for an Open Calais API key: http://www.opencalais.com/
open_calais_license_id = 'br86bgraa4hnn3ny47vu74ge'
# Get an App ID for your Yahoo Search BOSS app: 
# http://developer.yahoo.com/search/boss/
yahoo_search_app_id = '2vwjUpjIkY3KEN69IdN9pe_w0AQLVSq5FgM-'


class Preview(webapp.RequestHandler):
  def post(self):
    self.response.headers['Content-Type'] = 'text/plain'
    notes = self.request.body
    form_data = {'licenseID': open_calais_license_id, 'content':notes,
                 'paramsXML': '<c:params '
                     'xmlns:c="http://s.opencalais.com/1/pred/" '
                     'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
                   '<c:processingDirectives c:contentType="text/txt" '
                       'c:enableMetadataType="GenericRelations" '
                       'c:outputFormat="text/simple">'
                   '</c:processingDirectives>'
                   '<c:userDirectives c:allowDistribution="true" '
                       'c:allowSearch="true" c:externalID="17cabs901" '
                       'c:submitter="ABC">'
                   '</c:userDirectives>'
                   '<c:externalMetadata></c:externalMetadata>'
                 '</c:params>'}
    #logging.debug('request: ' + notes)
    calaise = urlfetch.fetch('https://api.opencalais.com/enlighten/rest/', 
                             urllib.urlencode(form_data), urlfetch.POST, 
                             headers={'Content-Type':
                                 'application/x-www-form-urlencoded'})
    #logging.debug('response: ' + calaise.content)
    if calaise.status_code == 200:
      calaise_xml = ElementTree.fromstring(calaise.content)
      for calaise_simple in calaise_xml.findall('CalaisSimpleOutputFormat'):
        for entity in calaise_simple:
          if entity.tag == 'Company':
            self.response.out.write('%s %s\n' % (entity.tag, 
                entity.attrib['normalized']))
          elif entity.tag == 'IndustryTerm':
            self.response.out.write('%s\n' % (entity.text))
          elif entity.tag == 'Topics':
            pass
          else:
            self.response.out.write('%s %s\n' % (entity.tag, entity.text))


class YSearch(webapp.RequestHandler):
  def get(self):
    query = self.request.get('q')
    yresults = urlfetch.fetch('http://boss.yahooapis.com/ysearch/web/v1/%s?'
        'appid=%s' % (urllib.quote(query), yahoo_search_app_id), 
        None, urlfetch.GET)
    self.response.out.write(yresults.content)


application = webapp.WSGIApplication(
                                     [('/article_preview', Preview),
                                      ('/article_ysearch', YSearch)],
                                     debug=True)


def main():
  run_wsgi_app(application)


if __name__ == "__main__":
  main()
