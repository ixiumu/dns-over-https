# DNS over HTTPS Proxy
# xiumu <xiumu at mail dot com>

from google.appengine.api import urlfetch
import logging
import webapp2

class DoH(webapp2.RequestHandler):
    def get(self):
        # self.response.headers['Content-Type'] = 'application/dns-message'
        self.response.write('coming soon!')

class Resolve(webapp2.RequestHandler):
    def get(self):

        if self.request.get('name'):
            # real client ip
            client_ip = self.request.environ.get('CF_CONNECTING_IP') or self.request.environ.get('HTTP_X_APPENGINE_USER_IP') or self.request.environ.get('HTTP_X_FORWARDED_FOR') or self.request.environ.get('REMOTE_ADDR')
            target_url = 'https://dns.google' + self.request.path_qs + '&edns_client_subnet=' + client_ip
            target_headers = self.request.headers
            # print(target_headers)
            # self.response.write(target_url)

            try:
                result = urlfetch.fetch(
                    url = target_url,
                    headers = target_headers,
                    deadline = 5,
                    validate_certificate = None
                    )
                if result.status_code == 200:
                    # self.response.headers['Content-Type'] = 'application/x-javascript'
                    self.response.headers['Content-Type'] = result.headers['Content-Type']
                    self.response.write(result.content)
                else:
                    self.response.status_int = result.status_code
            except urlfetch.Error:
                logging.exception('ERROR: Caught exception fetching url')
        else:
            self.response.write('ERROR: name cannot be empty!')

class Home(webapp2.RequestHandler):
    def get(self):
        self.response.write('GET: /resolve?name=<example.com>')

app = webapp2.WSGIApplication([
    ('/', Home),
    ('/dns-query', DoH),
    ('/resolve', Resolve)
])