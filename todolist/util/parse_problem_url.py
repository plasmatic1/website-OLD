"""
Sample URLS List:

dmoj: https://dmoj.ca/problem/valentines18s3
cf: https://codeforces.com/problemset/problem/1252/K
atcoder: https://atcoder.jp/contests/abc143/tasks/abc143_f
kattis: https://open.kattis.com/problems/quantumsuperposition

"""
import re
from urllib.parse import urlparse

import requests

from dmojsolutions.models import Problem


def get(url):
    """
    Sends a get request to the specified URL and returns the content as a str object
    :param url: The URL to get
    :return: The content of the response, as a string object
    """
    return str(requests.get(url=url).content, 'utf8')


def parse_dmoj(url, parse_res):
    """
    Parses a DM::OJ URL for a problem name
    :param url: The URL
    :param parse_res: The result of `urllib.parse.urlparse(url)`
    :return: The problem name
    """

    problem_id = parse_res.path.split('/')[-1]
    return Problem.objects.get(code=problem_id).name  # MUST BE DMOJ SOLUTIONS Problem MODEL


def parse_cf(url, parse_res):
    """
    Parses a CodeForces URL for a problem name
    :param url: The URL
    :param parse_res: The result of `urllib.parse.urlparse(url)`
    :return: The problem name
    """

    path = parse_res.path.split('/')
    contest_id = path[-2]
    problem_id = path[-1]
    name = re.search(r'<div class=\"title\">[A-Z]\. ([\w \-\.]+?)</div>', get(url)).group(1)
    return f'{contest_id}{problem_id} - {name}'


def parse_atcoder(url, parse_res):
    """
    Parses an AtCoder URL for a problem name
    :param url: The URL
    :param parse_res: The result of `urllib.parse.urlparse(url)`
    :return: The problem name
    """

    contest = parse_res.path.split('/')[-1].split('_')[0]
    name = re.search(r'\<span class\=\"h2\"\>([\w\- ]+?)\<\/span\>', get(url)).group(1)
    return f'{contest.upper()} {name}'


def parse_kattis(url, parse_res):
    """
    Parses a Kattis URL for a problem name
    :param url: The URL
    :param parse_res: The result of `urllib.parse.urlparse(url)`
    :return: The problem name
    """

    return re.search(r'<h1>(.+?)</h1>', get(url)).group(1)


PARSE_FUNS = {
    'dmoj': parse_dmoj,
    'cf': parse_cf,
    'atcoder': parse_atcoder,
    'kattis': parse_kattis
}


class InvalidURLDomain(Exception):
    pass


class ProblemURLParseError(Exception):
    pass


def parse_problem_url(url):
    """
    Parses a URL for a problem type (judge) and name
    :param url: The URL
    :return: A tuple (type, name) representing the type (judge) of the problem and the name
    """
    parse_res = urlparse(url)
    netloc = parse_res.netloc

    try:
        if netloc == 'dmoj.ca':
            return 'dmoj', parse_dmoj(url, parse_res)
        elif netloc == 'codeforces.com':
            return 'cf', parse_cf(url, parse_res)
        elif netloc == 'atcoder.jp':
            return 'atcoder', parse_atcoder(url, parse_res)
        elif netloc == 'open.kattis.com':
            return 'kattis', parse_kattis(url, parse_res)
    except Exception as e:
        raise ProblemURLParseError(f'Exception: {str(e)}')

    raise InvalidURLDomain(f'Invalid domain "{netloc}"')
