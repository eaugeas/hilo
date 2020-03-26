from setuptools import setup

setup(
    name='hilo_rpc',
    version='0.1',
    description='hilo rpc interface definitions',
    author='eaugeas',
    author_email='eaugeas@gmail.com',
    packages=['hilo_rpc/proto'],
    install_requires=['grpcio==1.27.1', 'grpcio-tools==1.27.1', 'protobuf==3.11.3', 'PyYAML'],
    scripts=[]
)