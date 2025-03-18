from setuptools import setup, find_packages

from smsgateway import __version__


setup(
    name='django-smsgateway',
    version=__version__,
    url='https://github.com/vikingco/smsgateway',
    license='BSD',
    description='SMS gateway for sending text messages',
    long_description=open('README.md', 'r').read(),
    author='Unleashed NV',
    author_email='operations@unleashed.be',
    packages=find_packages('.'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django-statsd-unleashed>=1.0.1',
        'statsd>=2.1.2',
        'redis==2.10.6',
        'pytz>=2020.1',
        'django-db-locking>=2.2,<2.3',
        'phonenumberslite==8.12.9',
        'celery<5',
        'django-admin-rangefilter==0.13.2',
    ],
    setup_requires=['pytest-runner', ],
    dependency_links=[],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
    ],
)
