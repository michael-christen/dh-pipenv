# dh-pipenv

This is a very small wrapper around `pipenv` to allow it to be used by
`dh-virtualenv`


To get it to work:

```
override_dh_virtualenv:
    dh_virtualenv \
        --preinstall dh-pipenv==0.1.0 \
        --preinstall pipenv==9.0.1 \
        --pip-tool dh-pipenv
```

# TODO:

- [ ] Setup on pypi
