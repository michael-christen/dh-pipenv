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

## TODO:

- [ ] Setup on pypi
