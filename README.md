# Django Helpdesk

## Installation

~~~
> pipenv install https://github.com/genosltd/django-helpdesk
~~~

or with pip using python 3.7:

~~~
> pip install https://github.com/genosltd/django-hashtag
~~~

## Usage

Do not forget to list `django_helpdesk` in `settings.py`:

~~~python
# settings.py
INSTALLED_APPS = [
    'django_helpdesk',
]
~~~

### Models

### Admin

## Contributing

1. Document the problem you are contributing to by [creating a new issue][new-issue] if not documented already.
1. Fork the repo privately [here][fork]. See [Fork a repo][fork-a-repo] for help.
1. Clone you fork locally. See [Cloning a repository][clone-a-repo] for help.
1. Open your clone directory in `cmd`
1. Install `django-hashtag` with:

    ~~~
    > pipenv install --skip-lock -d
    ~~~

1. Optionally for faster dev cycle, install venv with python 3.7:

    ~~~
    > pipenv run python -m venv venv && venv\Scripts\activate.bat

    (venv)> python -m pip install -U pip  && pip install --no-deps -r requirements.txt && pip install -e .
    ~~~

1. Create a new branch
1. Make necessary changes to the code
1. Test your changes as described in [Testing](#testing)
1. Commit and push
1. Create pull request
1. Discuss and tweak your contribution
1. Celebrate


### Testing

For testing please use:

~~~
> pipenv run tests\runtests.py
~~~

or with venv:

~~~
> venv\Scripts\activate.bat && python runtests.py
~~~

For coverage use:

~~~
> pipenv run coverage run && pipenv run coverage html
~~~

or with venv:

~~~
> venv\Scripts\activate.bat && coverage run && coverage html
~~~

Open [`htmlcov/index.html`](.\htmlcov\index.html]) in your browser for the coverage report.

[new-issue]: https://github.com/genosltd/django-helpdesk/issues/new
[fork]: https://github.com/genosltd/django-helpdesk/fork
[fork-a-repo]: https://docs.github.com/en/get-started/quickstart/fork-a-repo
[clone-a-repo]: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
