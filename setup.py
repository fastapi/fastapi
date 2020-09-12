#!/usr/bin/env python

from setuptools import setup

setup(
    name='fastapi',
    version='0.61.1.1',
    author="Sebastián Ramírez",
    author_email="tiangolo@gmail.com",
    url="https://github.com/tiangolo/fastapi",
    install_requires=[
        "requests >=2.24.0,<3.0.0",
        "aiofiles >=0.5.0,<0.6.0",
        "jinja2 >=2.11.2,<3.0.0",
        "python-multipart >=0.0.5,<0.0.6",
        "itsdangerous >=1.1.0,<2.0.0",
        "pyyaml >=5.3.1,<6.0.0",
        "graphene >=2.1.8,<3.0.0",
        "ujson >=3.0.0,<4.0.0",
        "orjson >=3.2.1,<4.0.0",
        "email_validator >=1.1.1,<2.0.0",
        "uvicorn >=0.11.5,<0.12.0",
        "async_exit_stack >=1.0.1,<2.0.0",
        "async_generator >=1.10,<2.0.0"
    ],
)
