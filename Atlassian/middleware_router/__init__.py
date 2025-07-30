"""
Middleware Router - A comprehensive system for function-based routing with middleware support.

This package provides a complete solution for building middleware-based routers
with path-based routing, middleware chains, and common middleware functions.
"""

from .models import (
    Request, Response, Route, MiddlewareContext, RouterConfig,
    HttpMethod, HttpStatus
)
from .router import MiddlewareRouter, PathMatcher
from .middleware import MiddlewareFactory, MiddlewareComposer

__version__ = "1.0.0"
__author__ = "Middleware Team"

__all__ = [
    # Models
    'Request', 'Response', 'Route', 'MiddlewareContext', 'RouterConfig',
    'HttpMethod', 'HttpStatus',
    
    # Router
    'MiddlewareRouter', 'PathMatcher',
    
    # Middleware
    'MiddlewareFactory', 'MiddlewareComposer'
] 