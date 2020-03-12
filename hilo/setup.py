from setuptools import setup

setup(
    name='hilo',
    version='0.1',
    description='hilo command line tool',
    author='eaugeas',
    author_email='eaugeas@gmail.com',
    packages=['hilo_src'],
    install_requires=['hilo_rpc'],
    dependency_links=[
        'hilo_rpc'
    ],
    scripts=['hilo']
)