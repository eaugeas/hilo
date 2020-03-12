from setuptools import setup

setup(
    name='hilo_server',
    version='0.1',
    description='hilo api server implementation',
    author='eaugeas',
    author_email='eaugeas@gmail.com',
    packages=['hilo_server'],
    install_requires=['hilo_rpc'],
    dependency_links=[
        'hilo_rpc'
    ],
    scripts=[]
)