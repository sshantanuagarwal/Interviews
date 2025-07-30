#!/usr/bin/env python3
"""
Example usage of the Middleware Router system.

This script demonstrates how to use the middleware router to create
function-based routing with middleware support.
"""

import json
import time
from typing import Dict, Any
from router import MiddlewareRouter
from middleware import MiddlewareFactory, MiddlewareComposer
from models import Request, Response, HttpMethod, HttpStatus, RouterConfig


def create_sample_handlers():
    """Create sample request handlers for demonstration."""
    
    def health_check_handler(request: Request) -> Response:
        """Health check endpoint."""
        return Response(
            status_code=HttpStatus.OK,
            body={
                'status': 'healthy',
                'timestamp': request.timestamp.isoformat(),
                'service': 'middleware-router'
            }
        )
    
    def user_list_handler(request: Request) -> Response:
        """Get list of users."""
        # Simulate database query
        users = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
            {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'}
        ]
        
        # Add query parameters for filtering
        limit = request.get_query_param('limit')
        if limit:
            try:
                users = users[:int(limit)]
            except ValueError:
                pass
        
        return Response(
            status_code=HttpStatus.OK,
            body={'users': users, 'count': len(users)}
        )
    
    def user_detail_handler(request: Request) -> Response:
        """Get user details by ID."""
        user_id = request.metadata.get('path_params', {}).get('id')
        
        if not user_id:
            return Response(
                status_code=HttpStatus.BAD_REQUEST,
                body={'error': 'User ID is required'}
            )
        
        # Simulate database query
        user = {
            'id': int(user_id),
            'name': f'User {user_id}',
            'email': f'user{user_id}@example.com',
            'created_at': '2024-01-01T00:00:00Z'
        }
        
        return Response(
            status_code=HttpStatus.OK,
            body={'user': user}
        )
    
    def create_user_handler(request: Request) -> Response:
        """Create a new user."""
        body = request.get_body_as_dict()
        
        # Validate required fields
        required_fields = ['name', 'email']
        missing_fields = [field for field in required_fields if field not in body]
        
        if missing_fields:
            return Response(
                status_code=HttpStatus.BAD_REQUEST,
                body={'error': 'Missing required fields', 'fields': missing_fields}
            )
        
        # Simulate user creation
        new_user = {
            'id': 999,  # Simulated ID
            'name': body['name'],
            'email': body['email'],
            'created_at': request.timestamp.isoformat()
        }
        
        return Response(
            status_code=HttpStatus.CREATED,
            body={'user': new_user, 'message': 'User created successfully'}
        )
    
    def update_user_handler(request: Request) -> Response:
        """Update user by ID."""
        user_id = request.metadata.get('path_params', {}).get('id')
        body = request.get_body_as_dict()
        
        if not user_id:
            return Response(
                status_code=HttpStatus.BAD_REQUEST,
                body={'error': 'User ID is required'}
            )
        
        # Simulate user update
        updated_user = {
            'id': int(user_id),
            'name': body.get('name', f'User {user_id}'),
            'email': body.get('email', f'user{user_id}@example.com'),
            'updated_at': request.timestamp.isoformat()
        }
        
        return Response(
            status_code=HttpStatus.OK,
            body={'user': updated_user, 'message': 'User updated successfully'}
        )
    
    def delete_user_handler(request: Request) -> Response:
        """Delete user by ID."""
        user_id = request.metadata.get('path_params', {}).get('id')
        
        if not user_id:
            return Response(
                status_code=HttpStatus.BAD_REQUEST,
                body={'error': 'User ID is required'}
            )
        
        # Simulate user deletion
        return Response(
            status_code=HttpStatus.NO_CONTENT,
            body={'message': f'User {user_id} deleted successfully'}
        )
    
    def protected_resource_handler(request: Request) -> Response:
        """Protected resource that requires authentication."""
        user_token = request.metadata.get('user_token', 'unknown')
        
        return Response(
            status_code=HttpStatus.OK,
            body={
                'message': 'Access granted to protected resource',
                'user_token': user_token,
                'authenticated': True
            }
        )
    
    def slow_handler(request: Request) -> Response:
        """Slow handler for testing rate limiting and caching."""
        time.sleep(1)  # Simulate slow operation
        
        return Response(
            status_code=HttpStatus.OK,
            body={
                'message': 'Slow operation completed',
                'timestamp': request.timestamp.isoformat()
            }
        )
    
    return {
        'health_check': health_check_handler,
        'user_list': user_list_handler,
        'user_detail': user_detail_handler,
        'create_user': create_user_handler,
        'update_user': update_user_handler,
        'delete_user': delete_user_handler,
        'protected_resource': protected_resource_handler,
        'slow_handler': slow_handler
    }


def create_custom_middleware():
    """Create custom middleware functions for demonstration."""
    
    def custom_header_middleware(context: Request, next_middleware: callable) -> Response:
        """Add custom headers to all responses."""
        response = next_middleware()
        response.set_header('X-Custom-Header', 'CustomValue')
        response.set_header('X-Request-ID', f"req_{int(time.time())}")
        return response
    
    def timing_middleware(context: Request, next_middleware: callable) -> Response:
        """Add timing information to responses."""
        start_time = time.time()
        response = next_middleware()
        duration = time.time() - start_time
        
        response.set_header('X-Processing-Time', f"{duration:.3f}s")
        return response
    
    def debug_middleware(context: Request, next_middleware: callable) -> Response:
        """Debug middleware that logs request details."""
        print(f"🔍 Debug: {context.request.method.value} {context.request.path}")
        print(f"   Headers: {context.request.headers}")
        print(f"   Query: {context.request.query_params}")
        
        response = next_middleware()
        
        print(f"   Response: {response.status_code.value}")
        return response
    
    return {
        'custom_header': custom_header_middleware,
        'timing': timing_middleware,
        'debug': debug_middleware
    }


def demonstrate_basic_routing():
    """Demonstrate basic routing functionality."""
    print("\n" + "="*80)
    print("🚀 BASIC ROUTING DEMONSTRATION 🚀")
    print("="*80)
    
    # Create router
    router = MiddlewareRouter()
    handlers = create_sample_handlers()
    
    # Add routes
    router.get('/health', handlers['health_check'])
    router.get('/users', handlers['user_list'])
    router.get('/users/:id', handlers['user_detail'])
    router.post('/users', handlers['create_user'])
    router.put('/users/:id', handlers['update_user'])
    router.delete('/users/:id', handlers['delete_user'])
    
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
            'path': '/users?limit=2',
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
            'method': 'PUT',
            'path': '/users/456',
            'headers': {'Content-Type': 'application/json'},
            'body': {'name': 'Jane Doe', 'email': 'jane@example.com'}
        },
        {
            'method': 'DELETE',
            'path': '/users/789',
            'headers': {'Content-Type': 'application/json'}
        },
        {
            'method': 'GET',
            'path': '/not-found',
            'headers': {'Content-Type': 'application/json'}
        }
    ]
    
    for i, request_data in enumerate(test_requests, 1):
        print(f"\n📝 Test Request {i}: {request_data['method']} {request_data['path']}")
        print("-" * 60)
        
        response = router.handle_request(request_data)
        
        print(f"Status: {response.status_code.value}")
        print(f"Headers: {dict(response.headers)}")
        if response.body:
            print(f"Body: {json.dumps(response.body, indent=2)}")
        print()


def demonstrate_middleware():
    """Demonstrate middleware functionality."""
    print("\n" + "="*80)
    print("🔧 MIDDLEWARE DEMONSTRATION 🔧")
    print("="*80)
    
    # Create router with middleware
    router = MiddlewareRouter()
    handlers = create_sample_handlers()
    custom_middleware = create_custom_middleware()
    
    # Add global middleware
    router.add_global_middleware(MiddlewareFactory.logging_middleware())
    router.add_global_middleware(custom_middleware['custom_header'])
    router.add_global_middleware(custom_middleware['timing'])
    
    # Add routes with specific middleware
    router.get('/health', handlers['health_check'])
    router.get('/users', handlers['user_list'])
    router.get('/users/:id', handlers['user_detail'])
    
    # Add route with debug middleware
    router.get('/debug/users', handlers['user_list'], 
               middleware=[custom_middleware['debug']])
    
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
            'path': '/debug/users',
            'headers': {'Content-Type': 'application/json'}
        }
    ]
    
    for i, request_data in enumerate(test_requests, 1):
        print(f"\n🔧 Test Request {i}: {request_data['method']} {request_data['path']}")
        print("-" * 60)
        
        response = router.handle_request(request_data)
        
        print(f"Status: {response.status_code.value}")
        print(f"Headers: {dict(response.headers)}")
        if response.body:
            print(f"Body: {json.dumps(response.body, indent=2)}")
        print()


def demonstrate_authentication():
    """Demonstrate authentication middleware."""
    print("\n" + "="*80)
    print("🔐 AUTHENTICATION DEMONSTRATION 🔐")
    print("="*80)
    
    # Create router with authentication
    router = MiddlewareRouter()
    handlers = create_sample_handlers()
    
    # Add authentication middleware
    auth_middleware = MiddlewareFactory.authentication_middleware()
    
    # Add routes
    router.get('/health', handlers['health_check'])  # Public
    router.get('/users', handlers['user_list'])      # Public
    router.get('/protected', handlers['protected_resource'], 
               middleware=[auth_middleware])         # Protected
    
    # Test requests
    test_requests = [
        {
            'method': 'GET',
            'path': '/health',
            'headers': {'Content-Type': 'application/json'}
        },
        {
            'method': 'GET',
            'path': '/protected',
            'headers': {'Content-Type': 'application/json'}
        },
        {
            'method': 'GET',
            'path': '/protected',
            'headers': {'Content-Type': 'application/json', 'Authorization': 'Bearer invalid'}
        },
        {
            'method': 'GET',
            'path': '/protected',
            'headers': {'Content-Type': 'application/json', 'Authorization': 'Bearer valid-token-123'}
        }
    ]
    
    for i, request_data in enumerate(test_requests, 1):
        print(f"\n🔐 Test Request {i}: {request_data['method']} {request_data['path']}")
        print("-" * 60)
        
        response = router.handle_request(request_data)
        
        print(f"Status: {response.status_code.value}")
        print(f"Headers: {dict(response.headers)}")
        if response.body:
            print(f"Body: {json.dumps(response.body, indent=2)}")
        print()


def demonstrate_rate_limiting():
    """Demonstrate rate limiting middleware."""
    print("\n" + "="*80)
    print("⏱️  RATE LIMITING DEMONSTRATION ⏱️")
    print("="*80)
    
    # Create router with rate limiting
    router = MiddlewareRouter()
    handlers = create_sample_handlers()
    
    # Add rate limiting middleware (5 requests per 10 seconds)
    rate_limit_middleware = MiddlewareFactory.rate_limiting_middleware(
        max_requests=5, window_seconds=10
    )
    
    # Add routes
    router.get('/health', handlers['health_check'])
    router.get('/limited', handlers['slow_handler'], 
               middleware=[rate_limit_middleware])
    
    # Test rate limiting
    print("Testing rate limiting (5 requests allowed per 10 seconds):")
    print("-" * 60)
    
    for i in range(7):  # Try 7 requests
        request_data = {
            'method': 'GET',
            'path': '/limited',
            'headers': {'Content-Type': 'application/json'},
            'client_ip': '192.168.1.1'  # Same client
        }
        
        response = router.handle_request(request_data)
        
        print(f"Request {i+1}: Status {response.status_code.value}")
        if response.status_code == HttpStatus.SERVICE_UNAVAILABLE:
            print(f"  Rate limited: {response.body}")
        else:
            print(f"  Success: {response.body.get('message', '')}")
        print()


def demonstrate_caching():
    """Demonstrate caching middleware."""
    print("\n" + "="*80)
    print("💾 CACHING DEMONSTRATION 💾")
    print("="*80)
    
    # Create router with caching
    router = MiddlewareRouter()
    handlers = create_sample_handlers()
    
    # Add caching middleware (5 minutes cache)
    cache_middleware = MiddlewareFactory.caching_middleware(cache_duration=300)
    
    # Add routes
    router.get('/health', handlers['health_check'])
    router.get('/cached', handlers['slow_handler'], 
               middleware=[cache_middleware])
    
    # Test caching
    print("Testing caching (first request should be slow, second should be fast):")
    print("-" * 60)
    
    for i in range(3):
        request_data = {
            'method': 'GET',
            'path': '/cached',
            'headers': {'Content-Type': 'application/json'}
        }
        
        start_time = time.time()
        response = router.handle_request(request_data)
        duration = time.time() - start_time
        
        print(f"Request {i+1}:")
        print(f"  Duration: {duration:.3f}s")
        print(f"  Cache Header: {response.headers.get('X-Cache', 'N/A')}")
        print(f"  Status: {response.status_code.value}")
        print()


def demonstrate_standard_stack():
    """Demonstrate standard middleware stack."""
    print("\n" + "="*80)
    print("🏗️  STANDARD MIDDLEWARE STACK DEMONSTRATION 🏗️")
    print("="*80)
    
    # Create router with standard middleware stack
    router = MiddlewareRouter()
    handlers = create_sample_handlers()
    
    # Create standard middleware stack
    standard_middleware = MiddlewareComposer.create_standard_stack(
        enable_logging=True,
        enable_auth=False,
        enable_rate_limiting=True,
        enable_cors=True,
        enable_validation=True,
        enable_caching=True,
        enable_metrics=True
    )
    
    # Add global middleware
    for middleware in standard_middleware:
        router.add_global_middleware(middleware)
    
    # Add routes
    router.get('/health', handlers['health_check'])
    router.get('/users', handlers['user_list'])
    router.post('/users', handlers['create_user'])
    
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
            'method': 'POST',
            'path': '/users',
            'headers': {'Content-Type': 'application/json'},
            'body': {'name': 'Test User', 'email': 'test@example.com'}
        }
    ]
    
    for i, request_data in enumerate(test_requests, 1):
        print(f"\n🏗️  Test Request {i}: {request_data['method']} {request_data['path']}")
        print("-" * 60)
        
        response = router.handle_request(request_data)
        
        print(f"Status: {response.status_code.value}")
        print(f"Headers: {dict(response.headers)}")
        if response.body:
            print(f"Body: {json.dumps(response.body, indent=2)}")
        print()


def demonstrate_route_inspection():
    """Demonstrate route inspection functionality."""
    print("\n" + "="*80)
    print("🔍 ROUTE INSPECTION DEMONSTRATION 🔍")
    print("="*80)
    
    # Create router
    router = MiddlewareRouter()
    handlers = create_sample_handlers()
    
    # Add routes with different middleware
    router.get('/health', handlers['health_check'])
    router.get('/users', handlers['user_list'])
    router.get('/users/:id', handlers['user_detail'])
    router.post('/users', handlers['create_user'])
    router.put('/users/:id', handlers['update_user'])
    router.delete('/users/:id', handlers['delete_user'])
    
    # Get route information
    routes_info = router.get_routes()
    
    print("Registered Routes:")
    print("-" * 60)
    
    for method, routes in routes_info.items():
        print(f"\n{method.value} Routes:")
        for route in routes:
            print(f"  {route['path']}")
            print(f"    Handler: {route['handler']}")
            print(f"    Middleware: {route['middleware_count']} functions")
            print(f"    Metadata: {route['metadata']}")
            print()


def main():
    """Main demonstration function."""
    print("🚀 MIDDLEWARE ROUTER SYSTEM DEMONSTRATION 🚀")
    print("="*80)
    
    # Run demonstrations
    demonstrate_basic_routing()
    demonstrate_middleware()
    demonstrate_authentication()
    demonstrate_rate_limiting()
    demonstrate_caching()
    demonstrate_standard_stack()
    demonstrate_route_inspection()
    
    print("\n" + "="*80)
    print("🎉 DEMONSTRATION COMPLETED SUCCESSFULLY! 🎉")
    print("="*80)
    print("\n📋 Key Features Demonstrated:")
    print("  ✅ Path-based routing with parameters")
    print("  ✅ Middleware chain execution")
    print("  ✅ Authentication middleware")
    print("  ✅ Rate limiting middleware")
    print("  ✅ Caching middleware")
    print("  ✅ CORS middleware")
    print("  ✅ Request validation")
    print("  ✅ Error handling")
    print("  ✅ Metrics collection")
    print("  ✅ Standard middleware stack")
    print("  ✅ Route inspection")


if __name__ == "__main__":
    main() 