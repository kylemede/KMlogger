#!/usr/bin/env python
import os
import sys
import re

try:
    from setuptools import setup
    setup
except ImportError:
    from distutils.core import setup
    setup

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

# Handle encoding
major, minor1, minor2, release, serial = sys.version_info
if major >= 3:
    def rd(filename):
        f = open(filename, encoding="utf-8")
        r = f.read()
        f.close()
        return r
else:
    def rd(filename):
        f = open(filename)
        r = f.read()
        f.close()
        return r

setup(    
    name='KMlogger', 
    packages =['KMlogger'],
    version="1.0.2", 
    author='Kyle Mede',
    author_email = 'kylemede@gmail.com',
    url = 'https://github.com/kylemede/KMlogger',
    license = ['GNU GPLv3'],
    description ='A Python logging object that provided additional functionality beyond the standard module.',
    long_description=rd("README.rst") + "\n\n"
                    + "---------\n\n",
    package_data={"": ["LICENSE", "AUTHORS.rst"]},
    include_package_data=True,
    keywords=['logging'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python'
        ],
    #include_dirs = [np.get_include()],
    install_requires = ['psutil','six'],
    #ext_modules=[]
)
