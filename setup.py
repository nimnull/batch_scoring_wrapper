import codecs
import os.path
import re

from setuptools import setup

fname = os.path.join(os.path.abspath(os.path.dirname(
    __file__)), 'batch_wrapper', '__init__.py')

with codecs.open(fname, 'r', 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = \"([^']+)\"\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

fname = os.path.join(os.path.abspath(os.path.dirname(
    __file__)), 'requirements.txt')

extra = {
    'entry_points': {
        'console_scripts': ['wrap_scoring = batch_wrapper.main:main']
    },
    'install_requires': open(fname, 'r').readlines()
}


setup(
    name='batch_wrapper',
    version=version,
    description=("A script to wrap batch scoring util"),
    author='DataRobot',
    author_email='support@datarobot.com',
    maintainer='DataRobot',
    maintainer_email='support@datarobot.com',
    license='BSD',
    url='http://www.datarobot.com/',
    packages=['batch_wrapper'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    **extra
)
