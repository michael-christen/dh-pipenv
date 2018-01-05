# dh-pipenv

This is a very small shim for
[`dh-virtualenv`](https://github.com/spotify/dh-virtualenv) to allow it to use
[`pipenv`](https://github.com/pypa/pipenv) when installing
dependencies.

We know when `dh-virtualenv` is trying to installing dependencies because
they'll call the `pip-tool` with `-r <requirements_file>`. When we see that
pattern, we remove `-r <requirements_file>` from the cmd args as well as other
parameters that are incompatible with `pipenv`.

Parameters we are currently filtering out include
* `--log` - passed by default from `dh-virtualenv`
* `--extra-index-url` (required for installing `dh-pipenv` when running
  locally)

## Getting Started

To get it to work on a package that uses `dh-virtualenv` add these lines to
your `debian/rules` file.

```
override_dh_virtualenv:
    dh_virtualenv \
        --preinstall pipenv==9.0.1 \
        --preinstall dh-pipenv==0.1.0 \
        --pip-tool dh-pipenv
```

It simply ensures that `dh-pipenv` and `pipenv` are installed, and then asks
`dh-virtualenv` to install with `dh-pipenv` instead of default `pip`.

## Testing:

dh-pipenv needs to be accessible via `pypi`, to avoid spamming pypi with broken
builds I used [`pypi-server`](https://pypi.python.org/pypi/pypiserver) to run a
local pypi server. Then my development workflow looked like this

1. Edit `dh-pipenv`
2. Run `python setup.py sdist upload -r localpypi`
3. Attempt to run `dh-virtualenv` in a repo that had it enabled

Setup of pypi server was done by following the
[docs here](https://pypi.python.org/pypi/pypiserver). Then I ran it with:

```
pypi-server -p 8080 --overwrite -P .htpasswd packages
```

* `-p 8080` specifies the port
* `--overwrite` allows packages of the same version to overwrite themselves
  (very handy for development)
* `-P .htpasswd` referenced a password file that was generated for this pypi so
  that I could upload packages to it
