import os
import sys
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
    
requirements = ['httplib2', 'poster']
if sys.version_info <= (2,6):
    requirements.append('simplejson')

setup(
    name = "python-storymarket",
    version = "1.0b4",
    description = "Client library for the Storymarket",
    long_description = read('README.rst'),
    url = 'http://packages.python.org/python-storymarket',
    license = 'BSD',
    author = 'Jacob Kaplan-Moss',
    author_email = 'jacob@jacobian.org',
    packages = find_packages(exclude=['tests']),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires = requirements,
    tests_require = ["nose", "mock"],
    test_suite = "nose.collector",
)