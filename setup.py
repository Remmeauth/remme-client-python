from setuptools import (
    find_packages,
    setup,
)


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    author='Remme',
    description='Python integration library for REMChain.',
    install_requires=required,
    name='remme-client-python',
    packages=find_packages(),
    url='https://remme.io',
    version='0.0.1',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
    ],
)
