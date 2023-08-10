"""FastAPI framework, high performance, easy to learn, fast to code, ready for production"""

__version__ = "0.101.0"

from starlette import status as status

from .applications import FastAPI as FastAPI
from .background import BackgroundTasks as BackgroundTasks
from .datastructures import UploadFile as UploadFile
from .exceptions import HTTPException as HTTPException
from .exceptions import WebSocketException as WebSocketException
from .param_shortcuts import Body as Body
from .param_shortcuts import BodyEx as BodyEx
from .param_shortcuts import Cookie as Cookie
from .param_shortcuts import CookieEx as CookieEx
from .param_shortcuts import Depends as Depends
from .param_shortcuts import DependsEx as DependsEx
from .param_shortcuts import File as File
from .param_shortcuts import FileEx as FileEx
from .param_shortcuts import Form as Form
from .param_shortcuts import FormEx as FormEx
from .param_shortcuts import Header as Header
from .param_shortcuts import HeaderEx as HeaderEx
from .param_shortcuts import Path as Path
from .param_shortcuts import PathEx as PathEx
from .param_shortcuts import Query as Query
from .param_shortcuts import QueryEx as QueryEx
from .param_shortcuts import Security as Security
from .param_shortcuts import SecurityEx as SecurityEx
from .requests import Request as Request
from .responses import Response as Response
from .routing import APIRouter as APIRouter
from .websockets import WebSocket as WebSocket
from .websockets import WebSocketDisconnect as WebSocketDisconnect
