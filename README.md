# Website

This part of the website now only contains the DMOJ-solutions portion of the site.  To check out the branch still being maintained, click [here](https://github.com/plasmatic1/website-OLD/tree/reduced-to-dmojsols).

# Old Readme

My personal website!

You can access it [here](http://mosesxu.ca)!

## Installation

- Clone the repo
- Create a `config.py` file with the required config keys:
    - `SECRET_KEY`: Secret option from Django `settings.py`
    - `GITHUB_AUTH_KEY`: A GitHub API key used in `todolist` for accessing the GitHub API
    - `STATIC_ROOT`: Static root option from Django `settings.py`
    - `DEBUG`: Debug option from Django `settings.py`
    - *Note that `settings.py` may also need to be modified to change the allowed hosts, port, etc.*

## Notes

- Tested on: `Python 3.7.3`.  Likely compatible with: `Python 3.6`, `Python 3.7`, `Python 3.8`
- `todolist` uses the `Problem` model from `dmojsolutions` to resolve the names of DM::OJ problems from their links
