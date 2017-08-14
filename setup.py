from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Dollar_Drop',
    version='1.2.0',
    description='Totally NOT a Walmart Scraper...',
    long_description=long_description,
    url='https://github.com/theriley106/Dollar_Drop',
    author='Christopher Lambert',
    author_email='christopherlambert106@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='retail arbitrage finder walmart scan search',
    packages=find_packages(),
    install_requires=['flask', 'bs4', 'requests'],
)