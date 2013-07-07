
import webapp2
from webapp2_extras import json

from gaelib import handlers, tests

from pygcm import PyGCMRegister


class PyGCMRegisterTestHandler(handlers.Base):
  def post(self):
    r = PyGCMRegister('regkey')
    
    try:
      key = r.HandleRegistration()
    except (PyGCMCannotParseJSON, PyGCMInvalidInputData,
        PyGCMRegParameterNotExists) as e:
      webapp2.abort(403) # TODO: modify this, handle better
 
    self.json({'info': ('%s' % key)})


class PyGCMTest(tests.Base):
  app = webapp2.WSGIApplication([('/_/devices/register',
      PyGCMRegisterTestHandler)], debug=True)

  def testExpectedJSONResponse(self):
    jsondata = {
        'regkey' : 'Sfsfsffsdf-_-sddsdSA-D-s--__Apa-'
      }
    request = self.json_request('/_/devices/register', jsondata)
    response = request.get_response(self.app)
 
    self.assertEqual(response.body,
        ')]}\',\n{"info":"Sfsfsffsdf-_-sddsdSA-D-s--__Apa-"}')
    
