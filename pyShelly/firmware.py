import json
import urllib.request
import re

from .compat import s
from .utils import exception_log
from .const import (
    REGEX_VER
)

class firmware_manager():

    def __init__(self, parent):
        self.parent = parent
        self.list = self._http_get('https://repo.shelly.cloud/files/firmware')
        self.last_updated = None

    def _http_get(self, url):
        f = None
        try:
            f = urllib.request.urlopen(url)
            body = f.read()
            res = json.loads(s(body))
            return res['data']
        except Exception as ex:
            exception_log(ex, "Error http GET: http://{}", url)
        finally:
            if f:
                f.close()
        return {}

    def format(self, value):
        ver = re.search(REGEX_VER, value)
        if ver:
            return ver.group(2) + " (" + ver.group(1) + ")"
        return value

    def version(self, shelly_type, beta):
        if shelly_type in self.list:
            cfg = self.list[shelly_type]
            if beta and 'beta_ver' in cfg:
                return self.format(cfg['beta_ver'])
            else:
                return self.format(cfg['version'])

    def url(self, shelly_type, beta):
        if shelly_type in self.list:
            cfg = self.list[shelly_type]
            if beta and 'beta_ver' in cfg:
                return cfg['beta_url']
            else:
                return None
