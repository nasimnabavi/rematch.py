from . import exceptions
from . import network

from . import config, logger


class User(dict):
  LOGGEDOUT_USER = {"is_authenticated": False, "is_superuser": False,
                    "is_staff": False, "is_active": False, "id": None}

  def __init__(self):
    super(User, self).__init__()

    try:
      if 'token' in config:
        self.refresh()

      # refresh was successful
      if self['is_authenticated']:
        return

      # only attempt user auto login if configured
      if not config['settings']['login']['autologin']:
        return

      if 'username' in config and 'password' in config and 'server' in config:
        self.login(config['username'], config['password'], config['server'])
    except exceptions.RematchException as ex:
      logger('user').debug(ex)
      self.update(self.LOGGEDOUT_USER)

  def login(self, username, password, server):
    # authenticate
    login_params = {'username': username, 'password': password}
    r = network.query("POST", "accounts/login/", params=login_params,
                      server=server, json=True)
    token = r['key']

    # receive new user account details
    r = network.query("GET", "accounts/profile/", server=server, token=token,
                      json=True)
    self.clear()
    self.update(r)

    # save functioning token
    if self['is_authenticated']:
      config['token'] = token
      config.save()

    return self['is_authenticated']

  def logout(self):
    try:
      self.update(network.query("POST", "accounts/logout/", json=True))
    except exceptions.AuthenticationException:
      pass
    del config['token']
    self.refresh()

  def refresh(self):
    self.clear()
    try:
      self.update(network.query("GET", "accounts/profile/", json=True))
    except exceptions.AuthenticationException:
      del config['token']
      self.update(network.query("GET", "accounts/profile/", json=True))

  def __setitem__(self, key, value):
    raise RuntimeError("User is a read only dict")

user = User()
