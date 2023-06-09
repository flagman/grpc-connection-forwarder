from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="grpc_connection_forwarder",
    version="0.1.5",
    author="Pavel Malay",
    author_email="flagmansupport@gmail.com",
    description="A small package for counting gRPC connections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flagman/grpc-connection-forwarder",
    packages=find_packages(),

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
