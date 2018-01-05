"""Shim between dh_virtualenv and pipenv

When -r is used for pip to install dependencies use pipenv instead and remove
incompatible arguments.
"""
import os
import subprocess
import sys


def _remove_kwarg(args, kwarg):
    """Remove kwarg and its value from args.

    If both are in one arg (--log=hi), remove that element, but if they are
    split between two args ['--log', 'hi'] remove both.

    Args:
        args ([str, ...]): List of strings
        kwarg (str): Usually of the form '--<name>' ie) '--log'
    """
    args = [arg for arg in args if '%s=' % kwarg not in arg]
    # If kwarg is by self, remove it and its value
    try:
        index = args.index(kwarg)
    except ValueError:
        pass
    else:
        args = args[:index] + args[index + 2:]
    return args


def convert_pip_args_to_pipenv_args(pip_args):
    """Remove non pipenv compatible args from arg list meant for pip_args.
    """
    # Remove -r requirements.txt
    try:
        r_index = pip_args.index('-r')
    except ValueError:
        # Unsupported behavior, but if you want to use this outside of this
        # package, go for it and "good luck"
        pass
    else:
        pip_args = pip_args[:r_index] + pip_args[r_index + 2:]
    for kwarg in [
            '--index-url',
            '--extra-index-url',
            '--log']:
        pip_args = _remove_kwarg(pip_args, kwarg)
    # Add additional args
    # Can't be specified by --extra-pip-arg in debian/rules because used by pip
    # when installing preinstall packages ie) pipenv
    return pip_args + ['--system', '--deploy']


def main():
    dh_pipenv = sys.argv[0]
    # Get path of dh_pipenv pipenv
    assert os.path.isfile(dh_pipenv), "We should have a full path to dh_pipenv"
    bin_dir = os.path.dirname(dh_pipenv)
    pip_path = os.path.join(bin_dir, 'pip')
    pipenv_path = os.path.join(bin_dir, 'pipenv')
    assert os.path.isfile(pip_path), "Can't find pip: %s" % pip_path
    assert os.path.isfile(pipenv_path), "Can't find pipenv: %s" % pipenv_path
    # Setup environment variables
    environment = os.environ.copy()
    # Fallback to pip if requirements.txt not specified
    pip_args = sys.argv[1:]
    if '-r' not in pip_args:
        cmd_args = [pip_path] + pip_args
    else:
        pipenv_args = convert_pip_args_to_pipenv_args(sys.argv[1:])
        cmd_args = [pipenv_path] + pipenv_args
        # Set VIRTUAL_ENV only for `pipenv`, to make sure it installs files in
        # the right location.
        venv_dir = os.path.dirname(bin_dir)
        environment['VIRTUAL_ENV'] = environment.get('VIRTUAL_ENV', venv_dir)
    subprocess.check_call(cmd_args, env=environment)


if __name__ == '__main__':
    main()
