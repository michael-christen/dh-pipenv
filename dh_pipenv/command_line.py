"""Shim between dh_virtualenv and pipenv
"""
import os
import subprocess
import sys


def remove_requirements(pip_args):
    # Check that -r requirements.txt is there
    # assert '-r' in pip_args, "-r not in args to pip-tool"
    # TODO: requirements.txt isn't always it, ie) ./requirements.txt
    # assert 'requirements.txt' in pip_args[r_index+1], "requirements.txt not after -r in args to pip-tool"
    # Remove -r requirements.txt
    try:
        r_index = pip_args.index('-r')
    except ValueError:
        return pip_args
    else:
        return pip_args[:r_index] + pip_args[r_index + 2:]


def remove_extra_index(pip_args):
    return [arg for arg in pip_args if '--extra-index-url=' not in arg]


def remove_log(pip_args):
    return [arg for arg in pip_args if '--log=' not in arg]


def convert_pip_args_to_pipenv_args(bin_dir, pip_args):
    # Fallback to pip if requirements.txt not specified
    if '-r' not in pip_args:
        return [os.path.join(bin_dir, 'pip')] + pip_args
    pipenv_args = [os.path.join(bin_dir, 'pipenv')]
    # Remove any problem args
    # Remove -r requirements.txt
    pip_args = remove_requirements(pip_args)
    # Remove --extra-index-url=...
    pip_args = remove_extra_index(pip_args)
    # Remove --log
    pip_args = remove_log(pip_args)
    # Add pip_args to pipenv_args
    pipenv_args += pip_args
    # TODO: Add additional args, ie) --system
    # Can't be specified by --extra-pip-arg in debian/rules because used by pip
    pipenv_args += ['--system', '--deploy']
    return pipenv_args


def main():
    print sys.argv
    dh_pipenv = sys.argv[0]
    # Get path of dh_pipenv pipenv
    assert os.path.isfile(dh_pipenv), "We should have a full path to dh_pipenv"
    bin_dir = os.path.dirname(dh_pipenv)
    pipenv_args = convert_pip_args_to_pipenv_args(bin_dir, sys.argv[1:])
    # Set VIRTUAL_ENV
    # TODO: Possibly only set for pipenv
    venv_dir = os.path.dirname(bin_dir)
    pipenv = os.path.join(os.path.dirname(dh_pipenv), 'pipenv')
    environment = os.environ.copy()
    environment['VIRTUAL_ENV'] = environment.get('VIRTUAL_ENV', venv_dir)
    # TODO: Check if we should add ENV variables
    subprocess.check_call(pipenv_args, env=environment)


if __name__ == '__main__':
    main()
