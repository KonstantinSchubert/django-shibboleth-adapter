import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-shibboleth-adapter',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Adapter for integrating Shibboleth with the Django authentication system.',
    long_description=README,
    url='https://www.example.com/',
    author='Konstantin Schubert',
    author_email='konstantin@schubert.fr',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.7',  # minimum requirement
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)