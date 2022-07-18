from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
import argparse
import re


# SOURCE: https://gist.github.com/asfaltboy/79a02a2b9871501af5f00c95daaeb6e7
class EmailType:
    """
    Supports checking email agains different patterns. The current available patterns is:
    RFC5322 (http://www.ietf.org/rfc/rfc5322.txt)
    """

    patterns = {
        'RFC5322': re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
    }

    def __init__(self, pattern):
        if pattern not in self.patterns:
            raise KeyError('{} is not a supported email pattern, choose from:'
                           ' {}'.format(pattern, ','.join(self.patterns)))
        self._rules = pattern
        self._pattern = self.patterns[pattern]

    def __call__(self, value):
        if not self._pattern.match(value):
            raise argparse.ArgumentTypeError(
                "'{}' is not a valid email - does not match {} rules".format(value, self._rules))
        return value


class Command(BaseCommand):
    help = 'builtin createsuperuser command but accepts all input (including password) through arguments'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs=1)
        parser.add_argument('email', type=EmailType('RFC5322'), nargs=1)
        parser.add_argument('password', nargs=1)

    def handle(self, *args, **options):
        username = options['username'][0]
        email = options['email'][0]
        password = options['password'][0]

        if User.objects.filter(username=username).exists():
            raise CommandError(f'User {username} already exists!')

        user = User.objects.create_superuser(username, email, password)
        user.save()

        self.stdout.write(f'List of superusers is now: '
                          f'{", ".join(map(lambda u: u.username, User.objects.filter(is_superuser=True).all()))}\n')
