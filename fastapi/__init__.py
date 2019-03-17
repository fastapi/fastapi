"""FastAPI framework, high performance, easy to learn, fast to code, ready for production"""

__version__ = "0.8.0"

from .applications import FastAPI
from .datastructures import UploadFile
from .exceptions import HTTPException
from .params import Body, Cookie, Depends, File, Form, Header, Path, Query, Security
from .routing import APIRouter
