from setuptools import setup

setup(
    name='ownercheck',
    version='0.2',
    description='Verify ownership of domain and mobile apps using DNS and other methods',
    author='Fallible',
    author_email='hello@fallible.co',
    url='https://github.com/FallibleInc/ownercheck',
    download_url='https://github.com/FallibleInc/ownercheck/tarball/0.2',
    packages=['ownercheck'],
    install_requires=[
        'dnspython',
        'requests',
        'pytest',
        'responses',
    ],
)
