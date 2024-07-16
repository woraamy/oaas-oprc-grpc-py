from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="oaas-sdk-grpc",
    version="0.0.3",
    author="Worawalan Chatlatanagulchai",
    author_email="worawalanc@gmail.com",
    description="GRPC SDK for OAAS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/woraamy/oaas-oprc-grpc-py",
    packages=find_packages(include=["oaas_sdk_grpc", "oaas_sdk_grpc.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
