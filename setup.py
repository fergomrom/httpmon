from setuptools import setup

install_requires = [
    'click==7.0',
],

setup(
    name='httpmon',
    version='1.0.0',
    description='HTTP log monitoring console program',
    author='Fernando Gomez',
    author_email='contact@fernandogr.com',
    install_requires=install_requires,
    test_suite='tests',
    entry_points='''
        [console_scripts]
        httpmon=httpmon.cli:httpmon_cli
    '''
)
