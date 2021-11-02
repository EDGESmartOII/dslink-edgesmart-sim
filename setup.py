from setuptools import setup

setup(
    name="dslink-esPy-responder",
    version="0.0.1",
    description="Python DSLink for EDGEsmart",
    url="https://github.com/EDGESmartOII/dslink-esPy-master",
    author="Mike Neal",
    author_email="mneal@oceaneering.com",
    license="Apache 2.0",
    install_requires=[
        "dslink == 0.7.3", 'icecream'
    ],
    dependency_links=[
        "https://github.com/IOT-DSA/sdk-dslink-python/archive/v0.7.1.tar.gz#egg=dslink-0.7.2"
    ]
)
