import os
import httpx
import openai
import contextlib
from dotenv import load_dotenv

load_dotenv(verbose=True)

HTTP_CLIENT = httpx.Client()
ASYNC_HTTP_CLIENT = httpx.AsyncClient()

__all__ = [
    "HTTP_CLIENT",
    "ASYNC_HTTP_CLIENT",
]