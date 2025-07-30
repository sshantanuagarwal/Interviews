#!/usr/bin/env python3
"""
Simple Middleware Router - 45-minute implementation
Function-based routing with basic middleware support
"""

import re
import time
import json
from typing import Dict, List, Callable, Optional, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class HttpStatus(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


@dataclass
class Request:
    method: HttpMethod
    path: str
    headers: Dict[str, str]
    body: Optional[Dict[str, Any]] = None
    client_ip: Optional[str] = None
    
    def get_header(self, key: str) -> Optional[str]:
        return self.headers.get(key)
    
    def get_body(self) -> Dict[str, Any]:
        return self.body or {}


@dataclass
class Response:
    status_code: HttpStatus
    headers: Dict[str, str]
    body: Optional[Dict[str, Any]] = None
    
    def set_header(self, key: str, value: str):
        self.headers[key] = value
    
    def set_body(self, data: Dict[str, Any]):
        self.body = data


class SimpleRouter:
    """Simple middleware router with function-based routing"""
    
    def __init__(self):
        self.routes: Dict[HttpMethod, List[tuple]] = {}
        self.global_middleware: List[Callable] = []
    
    def add_route(self, method: HttpMethod, path: str, handler: Callable, 
                  middleware: List[Callable] = None):
        """Add a route with optional middleware"""
        if method not in self.routes:
            self.routes[method] = []
        
        # Convert path parameters to regex
        pattern = re.sub(r':(\w+)', r'([^/]+)', path)
        pattern = f'^{pattern}$'
        
        self.routes[method].append((
            re.compile(pattern),
            path,
            handler,
            middleware or []
        ))
    
    def get(self, path: str, handler: Callable, middleware: List[Callable] = None):
        self.add_route(HttpMethod.GET, path, handler, middleware)
    
    def post(self, path: str, handler: Callable, middleware: List[Callable] = None):
        self.add_route(HttpMethod.POST, path, handler, middleware)
    
    def put(self, path: str, handler: Callable, middleware: List[Callable] = None):
        self.add_route(HttpMethod.PUT, path, handler, middleware)
    
    def delete(self, path: str, handler: Callable, middleware: List[Callable] = None):
        self.add_route(HttpMethod.DELETE, path, handler, middleware)
    
    def add_middleware(self, middleware: Callable):
        """Add global middleware"""
        self.global_middleware.append(middleware)
    
    def _find_route(self, method: HttpMethod, path: str):
        """Find matching route and extract parameters"""
        if method not in self.routes:
            return None
        
        for pattern, original_path, handler, middleware in self.routes[method]:
            match = pattern.match(path)
            if match:
                # Extract path parameters
                param_names = re.findall(r':(\w+)', original_path)
                params = {}
                for i, param_name in enumerate(param_names):
                    if i + 1 < len(match.groups()):
                        params[param_name] = match.group(i + 1)
                
                return handler, middleware, params
        
        return None
    
    def handle_request(self, request_data: Dict[str, Any]) -> Response:
        """Handle a request and return response"""
        try:
            # Parse request
            request = Request(
                method=HttpMethod(request_data.get('method', 'GET')),
                path=request_data.get('path', '/'),
                headers=request_data.get('headers', {}),
                body=request_data.get('body'),
                client_ip=request_data.get('client_ip')
            )
            
            # Find route
            route_match = self._find_route(request.method, request.path)
            if not route_match:
                return Response(
                    status_code=HttpStatus.NOT_FOUND,
                    headers={},
                    body={'error': 'Route not found'}
                )
            
            handler, route_middleware, path_params = route_match
            
            # Add path parameters to request
            request.path_params = path_params
            
            # Build middleware chain
            middleware_chain = self.global_middleware + route_middleware
            
            # Execute middleware chain
            response = self._execute_middleware_chain(request, middleware_chain, handler)
            
            return response
            
        except Exception as e:
            return Response(
                status_code=HttpStatus.INTERNAL_SERVER_ERROR,
                headers={},
                body={'error': str(e)}
            )
    
    def _execute_middleware_chain(self, request: Request, middleware_chain: List[Callable], 
                                 handler: Callable) -> Response:
        """Execute middleware chain and handler"""
        if not middleware_chain:
            return handler(request)
        
        def execute_middleware(index: int) -> Response:
            if index >= len(middleware_chain):
                return handler(request)
            
            middleware = middleware_chain[index]
            
            def next_middleware() -> Response:
                return execute_middleware(index + 1)
            
            return middleware(request, next_middleware)
        
        return execute_middleware(0)


# Simple middleware functions
def logging_middleware(request: Request, next_middleware: Callable) -> Response:
    """Log request and response"""
    print(f"Request: {request.method.value} {request.path}")
    
    response = next_middleware()
    
    print(f"Response: {response.status_code.value}")
    return response


def auth_middleware(request: Request, next_middleware: Callable) -> Response:
    """Simple authentication middleware"""
    token = request.get_header('Authorization')
    
    if not token or not token.startswith('Bearer '):
        return Response(
            status_code=HttpStatus.UNAUTHORIZED,
            headers={},
            body={'error': 'Authentication required'}
        )
    
    return next_middleware()


def cors_middleware(request: Request, next_middleware: Callable) -> Response:
    """Add CORS headers"""
    response = next_middleware()
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    return response


def rate_limit_middleware(request: Request, next_middleware: Callable) -> Response:
    """Simple rate limiting (in-memory)"""
    # In production, use Redis or database
    client_ip = request.client_ip or 'unknown'
    
    # Simple rate limiting: allow 10 requests per minute
    current_time = time.time()
    if not hasattr(rate_limit_middleware, 'requests'):
        rate_limit_middleware.requests = {}
    
    if client_ip not in rate_limit_middleware.requests:
        rate_limit_middleware.requests[client_ip] = []
    
    # Clean old requests (older than 60 seconds)
    rate_limit_middleware.requests[client_ip] = [
        req_time for req_time in rate_limit_middleware.requests[client_ip]
        if current_time - req_time < 60
    ]
    
    # Check rate limit
    if len(rate_limit_middleware.requests[client_ip]) >= 10:
        return Response(
            status_code=HttpStatus.INTERNAL_SERVER_ERROR,
            headers={},
            body={'error': 'Rate limit exceeded'}
        )
    
    # Add current request
    rate_limit_middleware.requests[client_ip].append(current_time)
    
    return next_middleware()


# Example handlers
def health_check(request: Request) -> Response:
    return Response(
        status_code=HttpStatus.OK,
        headers={},
        body={'status': 'healthy', 'timestamp': datetime.now().isoformat()}
    )


def get_users(request: Request) -> Response:
    users = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'},
        {'id': 3, 'name': 'Charlie'}
    ]
    
    return Response(
        status_code=HttpStatus.OK,
        headers={},
        body={'users': users, 'count': len(users)}
    )


def get_user(request: Request) -> Response:
    user_id = request.path_params.get('id')
    
    user = {
        'id': int(user_id),
        'name': f'User {user_id}',
        'email': f'user{user_id}@example.com'
    }
    
    return Response(
        status_code=HttpStatus.OK,
        headers={},
        body={'user': user}
    )


def create_user(request: Request) -> Response:
    body = request.get_body()
    
    if 'name' not in body or 'email' not in body:
        return Response(
            status_code=HttpStatus.BAD_REQUEST,
            headers={},
            body={'error': 'Name and email are required'}
        )
    
    new_user = {
        'id': 999,  # Simulated ID
        'name': body['name'],
        'email': body['email']
    }
    
    return Response(
        status_code=HttpStatus.CREATED,
        headers={},
        body={'user': new_user, 'message': 'User created'}
    )


def protected_resource(request: Request) -> Response:
    return Response(
        status_code=HttpStatus.OK,
        headers={},
        body={'message': 'Access granted to protected resource'}
    )


# Demo function
def demo():
    """Demonstrate the simple middleware router"""
    print("🚀 Simple Middleware Router Demo")
    print("=" * 50)
    
    # Create router
    router = SimpleRouter()
    
    # Add global middleware
    router.add_middleware(logging_middleware)
    router.add_middleware(cors_middleware)
    
    # Add routes
    router.get('/health', health_check)
    router.get('/users', get_users)
    router.get('/users/:id', get_user)
    router.post('/users', create_user)
    
    # Protected route
    router.get('/protected', protected_resource, middleware=[auth_middleware])
    
    # Test requests
    test_requests = [
        {
            'method': 'GET',
            'path': '/health',
            'headers': {'Content-Type': 'application/json'}
        },
        {
            'method': 'GET',
            'path': '/users',
            'headers': {'Content-Type': 'application/json'}
        },
        {
            'method': 'GET',
            'path': '/users/123',
            'headers': {'Content-Type': 'application/json'}
        },
        {
            'method': 'POST',
            'path': '/users',
            'headers': {'Content-Type': 'application/json'},
            'body': {'name': 'John Doe', 'email': 'john@example.com'}
        },
        {
            'method': 'GET',
            'path': '/protected',
            'headers': {'Content-Type': 'application/json'}
        },
        {
            'method': 'GET',
            'path': '/protected',
            'headers': {'Content-Type': 'application/json', 'Authorization': 'Bearer valid-token'}
        }
    ]
    
    for i, request_data in enumerate(test_requests, 1):
        print(f"\n📝 Test {i}: {request_data['method']} {request_data['path']}")
        print("-" * 40)
        
        response = router.handle_request(request_data)
        
        print(f"Status: {response.status_code.value}")
        print(f"Headers: {response.headers}")
        if response.body:
            print(f"Body: {json.dumps(response.body, indent=2)}")
        print()
    
    print("✅ Demo completed successfully!")


if __name__ == "__main__":
    demo() 