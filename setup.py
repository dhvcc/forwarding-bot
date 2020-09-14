import os

from setuptools import find_packages
from setuptools import setup


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


with open("transfer_bot/__init__.py") as f:
    exec(f.read())

setup(
    name='VK-TG-transfer-bot',
    author='dhvcc',
    version=locals()["__version__"],
    author_email='1337kwiz@gmail.com',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/dhvcc/VK-TG-transfer-bot",
    packages=find_packages(),
    python_requires='~=3.7',
    classifiers=[
        'Natural Language :: Russian',
        'Programming Language :: Python :: 3.7',
    ],
)
