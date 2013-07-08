
import webapp2
from webapp2_extras import json

from google.appengine.api import urlfetch


"""
  PyGCMRegister exceptions
"""
class PyGCMCannotParseJSON(Exception): pass
class PyGCMInvalidInputData(Exception): pass
class PyGCMRegParameterNotExists(Exception): pass

"""
  PyGCMRequester exceptions
"""
class PyGCMNotADevicesList(Exception): pass
class PyGCMNotADictData(Exception): pass
class PyGCMCannotSendPushTimeout(Exception): pass
class PyGCMNotAValidDevicesList(Exception): pass
class PyGCMCannotSendPushTimeout(Exception): pass
class PyGCMServerCannotParseJSON(Exception): pass
class PyGCMServerCannotAuthenticateSenderAccount(Exception): pass
class PyGCMInternalGCMServerError(Exception): pass
class PyGCMCannotParseJSONGCMResponse(Exception): pass


"""
  Class which handle the input requests giving the register keys of devices

  @params reg_parameter -> json name-parameter which hosts the register key
  @return the register key of device
"""
class PyGCMRegister(object):
  def __init__(self, reg_parameter):
    self.reg_parameter = reg_parameter

  def HandleRegistration(self):
    request = webapp2.get_request()

    # If we can't parse the input json, throw an exception
    try:
      data = json.decode(request.body)
    except ValueError:
      raise PyGCMCannotParseJSON()

    # We also ensure that the deserialized json is now a dict
    if not isinstance(data, dict):
      raise PyGCMInvalidInputData

    # Return the final value (register key)
    if self.reg_parameter in data:
      return data[self.reg_parameter]
    else:
      raise PyGCMRegParameterNotExists


class PyGCMRequester(object):
  headers = {
    'Content-type': 'application/json',
  }

  def __init__(self, GCM_URL, GCM_KEY):
    self.GCM_URL = GCM_URL
    headers['Authorization'] = 'key=%s' % GCM_KEY

  def sendPushNotification(self, devices, data):
    if not isinstance(devices, list):
      raise PyGCMNotADevicesList()

    if not all(isinstance(key, str) for key in decices):
      raise PyGCMNotAValidDevicesList()

    if not isinstance(data, dict):
      raise PyGCMNotADictData()

    # TODO: encode data to JSON
    # This uses the GAE fetch function to perform the request
    try:
      response = urlfetch.fetch(url=GCM_URL, 
                                data=data, 
                                method=urlfetch.POST,
                                headers=headers, 
                                validate_certificate=True)
    except DownloadError:
      raise PyGCMCannotSendPushTimeout()

    status_code = response.status_code
    if status_code == 400:
      raise PyGCMServerCannotParseJSON()

    if status_code == 401:
      raise PyGCMServerCannotAuthenticateSenderAccount()

    if status_code >= 500 and status_code <= 599:
      raise PyGCMInternalGCMServerError()

    try:
      data = json.decode(response.content)
    except ValueError:
      raise PyGCMCannotParseJSONGCMResponse()

    # TODO: finish to handle response
