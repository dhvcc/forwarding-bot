import os

from setuptools import find_packages
from setuptools import setup


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


pkg_info = {}

with open("forwarding_bot/__version__.py") as f:
    """Executing init to set __version__ value"""
    exec(f.read(), pkg_info)

REPO_URL = "https://github.com/dhvcc/forwarding-bot"

setup(
    name='forwarding-bot',
    author=pkg_info["__author__"],
    version=pkg_info["__version__"],
    author_email=pkg_info["__email__"],
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url=REPO_URL,
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        "vkbottle",
        "aiohttp"
    ],
    extras_require={
        "speedups": [
            "aiohttp[speedups]",
            "uvloop",
            "ujson"
        ],
        "dev": [
            "pre-commit",
            "flake8",
            "autoflake",
            "autopep8",
            "pyupgrade",
            "reorder-python-imports"
        ]
    },
    project_urls={
        "Source": REPO_URL,
        "Documentation": f"{REPO_URL}#documentation",
        "Tracker": f"{REPO_URL}/issues",
    },
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        "console_scripts":
            ["forwarding-bot=forwarding_bot.__main__:main"],
    }

)
