
import webapp2
from webapp2_extras import json


"""
  PyGCMRegister exceptions
"""
class PyGCMCannotParseJSON(Exception): pass
class PyGCMInvalidInputData(Exception): pass
class PyGCMRegParameterNotExists(Exception): pass


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

    # We also ensure that the deserialize json is now a dict
    if not isinstance(data, dict):
      raise PyGCMInvalidInputData

    # Return the final value (register key)
    if self.reg_parameter in data:
      return data[self.reg_parameter]
    else:
      raise PyGCMRegParameterNotExists

"""
class PyGCMRequester(object):
  headers = {
    'Content-type': 'application/json',
  }

  def __init__(self, GCM_URL, GCM_KEY):
    self.GCM_URL = GCM_URL
    headers['Authorization'] = 'key=%s' % GCM_KEY

  def makeRequest(self):
    """
