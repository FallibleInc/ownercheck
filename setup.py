from setuptools import setup

setup(
    name='ownercheck',
    version='0.1',
    description='Verify ownership of domain and mobile apps using DNS and other methods',
    author='Fallible',
    author_email='hello@fallible.co',
    packages=['ownercheck'],
    install_requires=[
        'dnspython',
        'requests',
        'pytest',
        'responses',
    ],
)
