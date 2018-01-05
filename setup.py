from setuptools import setup

setup(name='dh-pipenv',
      version='0.1.1',
      description='Shim between dh-virtualenv and pipenv',
      url='http://github.com/michael-christen/dh-pipenv',
      author='Michael Christen',
      author_email='mchristen96@gmail.com',
      license='MIT',
      zip_safe=False,
      packages=['dh_pipenv'],
      entry_points={
          'console_scripts': ['dh-pipenv=dh_pipenv.command_line:main'],
      },
)
