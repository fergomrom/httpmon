from setuptools import find_packages, setup


setup(
    name='httpmon',
    version='1.0.0',
    description='HTTP log monitoring console program',
    author='Fernando Gomez',
    author_email='contact@fernandogr.com',
    packages=find_packages(where='src', exclude=['tests']),
    test_suite='tests',
    entry_points='''
        [console_scripts]
        httpmon=httpmon.cli:httpmon_cli
    '''
)
