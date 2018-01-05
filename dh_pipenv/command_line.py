"""Shim between dh_virtualenv and pipenv
"""
import subprocess
import sys


def main():
    dh_pipenv = sys.argv[0]
    args = sys.argv[1:]
    # assert dh_pipenv == 'dh-pipenv'
    print args
    # Check that -r requirements.txt is there
    assert '-r' in args, "-r not in args to pip-tool"
    # TODO: requirements.txt isn't always it, ie) ./requirements.txt
    r_index = args.index('-r')
    assert 'requirements.txt' in args[r_index+1], "requirements.txt not after -r in args to pip-tool"
    # Remove -r requirements.txt
    args = args[:r_index] + args[r_index + 2:]
    # Call pipenv
    # Ensure this returns non-0 if pipenv fails
    # TODO: May need to add --system
    subprocess.check_call(['pipenv'] + args)


if __name__ == '__main__':
    main()
