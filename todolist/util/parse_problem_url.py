"""
Sample URLS List:

dmoj: https://dmoj.ca/problem/valentines18s3
cf: https://codeforces.com/problemset/problem/1252/K
atcoder: https://atcoder.jp/contests/abc143/tasks/abc143_f
kattis: https://open.kattis.com/problems/quantumsuperposition

"""
from urllib.parse import urlparse

import requests


def get(url):
    """
    Sends a get request to the specified URL and does some basic utility processing
    :param url: The URL to get
    :return: The processed data
    """
    return requests.get(url=url)


def parse_dmoj(url):
    """
    Parses a DM::OJ URL for a problem name
    :param url: The URL
    :return: The name
    """
    pass


def parse_cf(url):
    """
    Parses a CodeForces URL for a problem name
    :param url: The URL
    :return: The name
    """
    pass


def parse_atcoder(url):
    """
    Parses an AtCoder URL for a problem name
    :param url: The URL
    :return: The name
    """
    pass


def parse_kattis(url):
    """
    Parses a Kattis URL for a problem name
    :param url: The URL
    :return: The name
    """
    pass


PARSE_FUNS = {
    'dmoj': parse_dmoj,
    'cf': parse_cf,
    'atcoder': parse_atcoder,
    'kattis': parse_kattis
}


class InvalidURLDomain(Exception):
    pass


def parse_problem_url(url):
    """
    Parses a URL for a problem type (judge) and name
    :param url: The URL
    :return: A tuple (type, name) representing the type (judge) of the problem and the name
    """
    url = urlparse(url)

    if url is 'dmoj':  # TODO: IS DMOJ
        return 'dmoj', parse_dmoj(url)
    elif url is 'cf':  # TODO: IS CF
        return 'cf', parse_cf(url)
    elif url is 'atcoder':  # TODO: IF ATCODER
        return 'atcoder', parse_atcoder(url)
    elif url is 'kattis':  # TODO: IF KATTIS
        return 'kattis', parse_kattis(url)
    else:
        raise InvalidURLDomain(f'Invalid domain <... TODO ...>')
