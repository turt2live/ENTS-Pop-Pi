from setuptools import setup

setup(name='ents-poppi',
      version='1.0',
      description='ENTS RaspberryPi-controller pop machine',
      url='https://github.com/turt2live/ENTS-Pop-Pi',
      install_requires=[
          'RPi.GPIO',
          'gevent-socketio',
          #'MySQLdb', # sudo apt-get install python-mysqldb
          'SQLAlchemy',
          'configobj',
          'observable'
      ],
      zip_safe=False)
