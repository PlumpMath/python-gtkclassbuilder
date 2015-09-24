from setuptools import setup

setup(name='gtkclassbuilder',
      version='0.1',
      url='https://github.com/zenhack/python-gtkclassbuilder',
      packages=['gtkclassbuilder'],
      install_requires=[
          'pygobject>=3.16,<4.0',
      ],
      )
