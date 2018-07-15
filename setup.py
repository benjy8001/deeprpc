from setuptools import setup, find_packages

__NAME__ = 'deeprpc'
__VERSION__ = '0.1'


setup(
    name=__NAME__,
    version=__VERSION__,
    description="deeprpc",
    author='ugloo',
    author_email='support@ugloo.com',
    url='https://lelab.ubiquitus.info:27443/p2pgroup/deeprpc',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'kademlia>=1.0',
        'rpcudp>=3.0',
    ],
    entry_points={
        'console_scripts': [
            'udht_bootstrap_node = deeprpc.dht.bootstrap_node:main',
            'udht_node = deeprpc.dht.storer_node:main',
        ]
    }
)
