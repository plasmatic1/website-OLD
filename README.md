# Website

My personal website!

You can access it [here](http://plasmatic1.me)!

## Installation

- Clone the repo
- Fill out the `/config.py` file (you will likely have to make one yourself) with the required config keys.  They are:
    - `SECRET_KEY`: Secret option from Django `settings.py`
    - `GITHUB_AUTH_KEY`: A GitHub API key used in `todolist` for accessing the GitHub API
    - `STATIC_ROOT`: Static root option from Django `settings.py`
    - `DEBUG`: Debug option from Django `settings.py`
    - *Note that `settings.py` does not need to be configured*
WIP

**temp**
- Set up a reverse proxy (i.e. `nginx`) and configure all of the static-files related issues
- Set up something to run the server with (i.e. `gunicorn`)
- :D

## Important Notes

- `todolist` uses the `Problem` model from `dmojsolutions` to resolve the names of DM::OJ problems from their links
