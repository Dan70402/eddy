#! /usr/bin/env python

from setuptools import setup

setup(
    name                 = 'eddy',
    version              = '0.0.1',
    description          = 'NLP bot',
    url                  = 'https://github.com/Contatta/central-webhook-receiver.git',
    author               = 'Dan Howe',
    packages             = ['eddy'],
    #package_data         = {'central_webhook_receiver': ['*.ini']},
    #include_package_data = True
)

#python setup.py install
#python setup.py develop (to symlink to source)