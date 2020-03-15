from setuptools import setup

setup(
    name='hilo_stage',
    version='0.1',
    description='hilo pipeline stage implementations',
    author='eaugeas',
    author_email='eaugeas@gmail.com',
    packages=['hilo_stage'],
    install_requires=[
        # external dependencies
        'tfx==0.21.2',

        # freeze dependencies. Unfortunately tfx has a ton of
        # dependencies and if the versions are not pinned down,
        # there are version compatibility issues amongst them.
        # it is possible that as modules keep on being updated
        # this list needs to be updated
        'tfx-bsl==0.21.3',
        'google-api-python-client==1.7.11',
        'httplib2==0.12.0',
        'tensorflow==2.1.0',
        'tensorflow-transform==0.21.2',
        'tensorflow-data-validation==0.21.5',
        'tensorflow-model-analysis==0.21.6',
    ],
    scripts=[]
)