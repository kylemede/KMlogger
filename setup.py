#!/usr/bin/env python
import os
import sys

try:
    from setuptools import setup
    setup
except ImportError:
    from distutils.core import setup
    setup

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

setup(    
    name='KMlogger', 
    packages =['KMlogger'],
    version="1.0.4", 
    author='Kyle Mede',
    author_email = 'kylemede@gmail.com',
    url = 'https://github.com/kylemede/KMlogger',
    license = ['GNU GPLv3'],
    description ='A Python logging object that provides additional functionality beyond the standard module.',
    long_description="For examples of how to use KMlogger"+
    " please visit:\nhttps://github.com/kylemede/KMlogger",
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
