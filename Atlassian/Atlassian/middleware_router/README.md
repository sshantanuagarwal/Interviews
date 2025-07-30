# Middleware Router System

A comprehensive middleware-based router system with function-based routing, middleware chains, and common middleware functions.

## 🏗️ Architecture Overview

The Middleware Router system follows a clean architecture pattern with clear separation of concerns:

```
middleware_router/
├── models.py          # Data models and entities
├── router.py          # Core router with path matching
├── middleware.py      # Middleware factory and composer
├── __init__.py        # Package initialization
├── example_usage.py   # Comprehensive usage examples
└── README.md          # This file
```

## 🎯 Key Features

### 🚀 Function-Based Routing
- **Path-based routing** with parameter extraction (`/users/:id`)
- **HTTP method support** (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
- **Query parameter parsing** and validation
- **Request/Response models** with type safety

### 🔧 Middleware System
- **Middleware chains** with sequential execution
- **Global middleware** for all requests
- **Route-specific middleware** for individual endpoints
- **Middleware composition** utilities

### 🛡️ Built-in Middleware
- **Authentication** - Token-based authentication
- **Rate Limiting** - Request rate limiting per client
- **CORS** - Cross-origin resource sharing
- **Request Validation** - Input validation and sanitization
- **Caching** - Response caching for performance
- **Logging** - Request/response logging
- **Error Handling** - Centralized error handling
- **Metrics** - Request metrics collection

### 📊 Advanced Features
- **Path parameter extraction** (`/users/:id` → `{"id": "123"}`)
- **Query parameter parsing** (`/users?limit=10&page=1`)
- **Request body parsing** (JSON, form data)
- **Response formatting** with proper headers
- **Route inspection** and debugging tools

## 🚀 Quick Start

### Basic Usage

```python
from middleware_router import MiddlewareRouter, HttpMethod, HttpStatus

# Create router
router = MiddlewareRouter()

# Define handlers
def health_check(request):
    return Response(
        status_code=HttpStatus.OK,
        body={'status': 'healthy'}
    )

def get_users(request):
    users = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'}
    ]
    return Response(
        status_code=HttpStatus.OK,
        body={'users': users}
    )

# Add routes
router.get('/health', health_check)
router.get('/users', get_users)

# Handle request
request_data = {
    'method': 'GET',
    'path': '/health',
    'headers': {'Content-Type': 'application/json'}
}

response = router.handle_request(request_data)
print(response.status_code.value)  # 200
```

### Middleware Usage

```python
from middleware_router import MiddlewareFactory

# Create middleware
auth_middleware = MiddlewareFactory.authentication_middleware()
rate_limit_middleware = MiddlewareFactory.rate_limiting_middleware()

# Add global middleware
router.add_global_middleware(MiddlewareFactory.logging_middleware())

# Add route with specific middleware
router.get('/protected', protected_handler, middleware=[auth_middleware])
router.get('/limited', slow_handler, middleware=[rate_limit_middleware])
```

## 📋 Data Models

### Request
```python
@dataclass
class Request:
    method: HttpMethod
    path: str
    headers: Dict[str, str]
    query_params: Dict[str, str]
    body: Optional[Dict[str, Any]]
    raw_body: Optional[str]
    client_ip: Optional[str]
    timestamp: datetime
    metadata: Dict[str, Any]
```

### Response
```python
@dataclass
class Response:
    status_code: HttpStatus
    headers: Dict[str, str]
    body: Optional[Dict[str, Any]]
    raw_body: Optional[str]
    timestamp: datetime
    metadata: Dict[str, Any]
```

### Route
```python
@dataclass
class Route:
    path: str
    method: HttpMethod
    handler: Callable[[Request], Response]
    middleware: List[Callable]
    metadata: Dict[str, Any]
```

## 🔧 Middleware Examples

### Authentication Middleware
```python
auth_middleware = MiddlewareFactory.authentication_middleware(
    auth_header='Authorization',
    token_prefix='Bearer ',
    validate_token=custom_token_validator
)
```

### Rate Limiting Middleware
```python
rate_limit_middleware = MiddlewareFactory.rate_limiting_middleware(
    max_requests=100,
    window_seconds=60,
    key_func=lambda req: req.client_ip
)
```

### Caching Middleware
```python
cache_middleware = MiddlewareFactory.caching_middleware(
    cache_duration=300,  # 5 minutes
    cache_key_func=lambda req: f"{req.method.value}:{req.path}"
)
```

### Custom Middleware
```python
def custom_middleware(context, next_middleware):
    # Pre-processing
    print(f"Processing: {context.request.path}")
    
    # Execute next middleware/handler
    response = next_middleware()
    
    # Post-processing
    response.set_header('X-Custom-Header', 'CustomValue')
    
    return response
```

## 🏗️ Standard Middleware Stack

```python
from middleware_router import MiddlewareComposer

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

# Add to router
for middleware in standard_middleware:
    router.add_global_middleware(middleware)
```

## 📊 Path Parameter Examples

```python
# Route with path parameters
router.get('/users/:id', get_user_handler)
router.get('/posts/:postId/comments/:commentId', get_comment_handler)

# Request: GET /users/123
# Path params: {"id": "123"}

# Request: GET /posts/456/comments/789
# Path params: {"postId": "456", "commentId": "789"}
```

## 🔍 Route Inspection

```python
# Get all registered routes
routes_info = router.get_routes()

for method, routes in routes_info.items():
    print(f"{method.value} Routes:")
    for route in routes:
        print(f"  {route['path']}")
        print(f"    Handler: {route['handler']}")
        print(f"    Middleware: {route['middleware_count']} functions")
```

## 🎨 Design Patterns Used

1. **Middleware Pattern** - Chain of responsibility for request processing
2. **Factory Pattern** - MiddlewareFactory for creating middleware
3. **Composer Pattern** - MiddlewareComposer for combining middleware
4. **Router Pattern** - Path-based routing with parameter extraction
5. **Builder Pattern** - Standard middleware stack builder
6. **Observer Pattern** - Logging and metrics collection

## 🔒 Security Features

- **Input validation** and sanitization
- **Rate limiting** to prevent abuse
- **Authentication** middleware for protected routes
- **CORS** support for cross-origin requests
- **Error handling** with proper status codes

## 🚀 Performance Features

- **Compiled path patterns** for fast matching
- **Response caching** for frequently accessed data
- **Metrics collection** for performance monitoring
- **Efficient middleware chains** with minimal overhead

## 📝 Usage Examples

### RESTful API
```python
# User management API
router.get('/users', list_users)
router.get('/users/:id', get_user)
router.post('/users', create_user)
router.put('/users/:id', update_user)
router.delete('/users/:id', delete_user)
```

### Protected Routes
```python
# Public routes
router.get('/health', health_check)
router.get('/public', public_handler)

# Protected routes
router.get('/admin', admin_handler, middleware=[auth_middleware])
router.post('/admin/users', create_admin_user, middleware=[auth_middleware])
```

### Custom Middleware Chain
```python
# Create custom middleware chain
custom_chain = MiddlewareComposer.compose(
    MiddlewareFactory.logging_middleware(),
    custom_middleware,
    MiddlewareFactory.error_handling_middleware()
)

router.get('/custom', handler, middleware=[custom_chain])
```

## 🤝 Contributing

1. Follow the existing code structure and patterns
2. Add comprehensive type hints
3. Include docstrings for all public methods
4. Write unit tests for new features
5. Update documentation as needed

## 📄 License

This project is designed for internal use and learning purposes. 