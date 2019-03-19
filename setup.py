from setuptools import (
    find_packages,
    setup,
)

VERSION = '0.0.1'


with open('README.md', 'r') as read_me:
    long_description = read_me.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    author='Remme',
    description='Python integration library for REMChain.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=required,
    name='remme-client-python',
    packages=find_packages(),
    url='https://github.com/Remmeauth/remme-client-python',
    version=VERSION,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
