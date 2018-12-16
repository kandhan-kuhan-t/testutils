import setuptools

from distutils.core import setup

setup(
    name='py_testutils',
    version='0.6',
    author='KK',
    author_email='kandhan.kuhan@gmail.com',
    packages=['testutils', ],
    license='LICENSE.txt',
    long_description=open('README.txt').read(),
    install_requires=[
        # "Django >= 1.1.1",
        # "caldav == 0.1.4",
    ],
)