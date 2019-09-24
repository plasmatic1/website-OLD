from base64 import b64decode
from urllib import request
from website import settings
from datetime import datetime
import re
import json


TAB_PATTERN = re.compile(r'\\t')
NEWLINE_PATTERN = re.compile(r'^\\n')

SRC_DIR_URL = 'https://api.github.com/repos/plasmatic1/dmoj-solutions/contents/%s'
SRC_FILE_URL = 'https://api.github.com/repos/plasmatic1/dmoj-solutions/contents/%s/%s'

BEGIN_TIME = datetime.fromtimestamp(0)


class RateLimitObj:
    def __init__(self):
        self.remaining = -1
        self.total = -1
        self.reset = BEGIN_TIME

    @property
    def initialized(self):
        return self.remaining != -1 and self.total != -1 and self.reset != BEGIN_TIME

    @property
    def until_reset(self):
        return self.reset - datetime.now()

    @property
    def until_reset_str(self):
        delta = self.until_reset.total_seconds()
        return '%d minute(s) %d second(s)' % (delta // 60, delta % 60)


rate_limit = RateLimitObj()


def get_raw(url):
    global rate_limit
    """
    Reads raw HTML from a URL
    :param url: the URL
    :return: the raw HTML
    """
    req = request.Request(url, headers={
        'Authorization': 'token %s' % settings.GITHUB_AUTH_KEY
    })

    with request.urlopen(req) as resp:
        rate_limit.remaining = resp.headers['X-RateLimit-Remaining']
        rate_limit.total = resp.headers['X-RateLimit-Limit']
        rate_limit.reset = datetime.fromtimestamp(int(resp.headers['X-RateLimit-Reset']))

        return str(resp.read(), 'ascii')


def codes_for_ext(ext):
    """
    Returns a list of file names to solutions in the specified extension
    :param ext: The extension to find solutions in
    :return: This list of solution file names
    """
    return [file['name'] for file in json.loads(get_raw(SRC_DIR_URL % ext))]


def src_for_code(ext, file_name):
    """
    Finds the source code to a specified solution
    :param ext: The extension to look under (for the solution file)
    :param file_name: The file name of the solution
    :return: The source code of the solution
    """
    return str(b64decode(json.loads(get_raw(SRC_FILE_URL % (ext, file_name)))['content']), 'ascii')
