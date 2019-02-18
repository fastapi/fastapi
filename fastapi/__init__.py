"""FastAPI framework, high performance, easy to learn, fast to code, ready for production"""

__version__ = "0.5.0"

from .applications import FastAPI
from .exceptions import HTTPException
from .params import Body, Cookie, Depends, File, Form, Header, Path, Query, Security
from .routing import APIRouter
