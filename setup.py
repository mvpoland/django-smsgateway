from setuptools import setup, find_packages

from smsgateway import __version__


setup(
    name='django-smsgateway',
    version=__version__,
    url='https://github.com/vikingco/smsgateway',
    license='BSD',
    description='SMS gateway for sending text messages',
    long_description=open('README.rst', 'r').read(),
    author='Unleashed NV',
    author_email='operations@unleashed.be',
    packages=find_packages('.'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django-statsd-unleashed>=1.0.1',
        'statsd>=2.1.2',
        'redis>=2.10.5',
        'pytz>=2016.7',
        'django-db-locking==2.1.0',
        'phonenumberslite==7.3.2',
        'six<2.0,>=1.11.0',
        'future>=0.16.0'
    ],
    setup_requires=['pytest-runner', ],
    dependency_links=[],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
