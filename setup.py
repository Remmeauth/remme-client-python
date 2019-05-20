from setuptools import (
    find_packages,
    setup,
)

VERSION = '1.1.1'


with open('README.md', 'r', encoding='utf-8') as read_me:
    long_description = read_me.read()

with open('requirements.txt', encoding='utf-8') as f:
    required = f.read().splitlines()

setup(
    author='Remme',
    description='Python integration library for REMChain.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    install_requires=required,
    name='remme',
    packages=find_packages(),
    url='https://github.com/Remmeauth/remme-client-python',
    version=VERSION,
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
