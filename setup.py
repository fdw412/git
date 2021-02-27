from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='gmun-tests',
    version='0.1.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    include_package_data=True,
    test_suite='test',
    install_requires=[
        'selenium==3.141.0',
        'requests==2.22.0',
        'celery==4.3.0',
        'sentry-sdk==0.11.2',
        'redis==3.3.11',
    ],
)
