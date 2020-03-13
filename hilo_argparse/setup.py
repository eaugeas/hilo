from setuptools import setup

setup(
    name='hilo_argparse',
    version='0.1',
    description='common functions on top of argparse',
    author='eaugeas',
    author_email='eaugeas@gmail.com',
    packages=['hilo_argparse'],
    install_requires=['protobuf==3.11.3', 'hilo_rpc'],
    scripts=[]
)
