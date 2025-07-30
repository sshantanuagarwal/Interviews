import time
import json
import hashlib
from typing import Callable, Dict, Any, Optional, List
from datetime import datetime, timedelta
from collections import defaultdict
import logging

from models import Request, Response, MiddlewareContext, HttpStatus, HttpMethod


class MiddlewareFactory:
    """Factory for creating common middleware functions."""
    
    @staticmethod
    def logging_middleware(logger: Optional[logging.Logger] = None) -> Callable:
        """Create logging middleware that logs request/response details."""
        if logger is None:
            logger = logging.getLogger('RequestLogger')
        
        def logging_middleware(context: MiddlewareContext, next_middleware: Callable) -> Response:
            start_time = time.time()
            
            # Log request
            logger.info(f"Request: {context.request.method.value} {context.request.path}")
            
            # Execute next middleware/handler
            response = next_middleware()
            
            # Log response
            duration = time.time() - start_time
            logger.info(
                f"Response: {response.status_code.value} - {duration:.3f}s"
            )
            
            return response
        
        return logging_middleware
    
    @staticmethod
    def authentication_middleware(
        auth_header: str = 'Authorization',
        token_prefix: str = 'Bearer ',
        validate_token: Optional[Callable[[str], bool]] = None
    ) -> Callable:
        """Create authentication middleware."""
        
        def auth_middleware(context: MiddlewareContext, next_middleware: Callable) -> Response:
            auth_token = context.request.get_header(auth_header)
            
            if not auth_token:
                return Response(
                    status_code=HttpStatus.UNAUTHORIZED,
                    body={'error': 'Authentication required'}
                )
            
            if not auth_token.startswith(token_prefix):
                return Response(
                    status_code=HttpStatus.UNAUTHORIZED,
                    body={'error': 'Invalid token format'}
                )
            
            token = auth_token[len(token_prefix):]
            
            # Use custom validation or default
            if validate_token:
                is_valid = validate_token(token)
            else:
                # Default validation (always true for demo)
                is_valid = len(token) > 0
            
            if not is_valid:
                return Response(
                    status_code=HttpStatus.UNAUTHORIZED,
                    body={'error': 'Invalid token'}
                )
            
            # Add user info to context
            context.set_metadata('user_token', token)
            context.set_metadata('authenticated', True)
            
            return next_middleware()
        
        return auth_middleware
    
    @staticmethod
    def rate_limiting_middleware(
        max_requests: int = 100,
        window_seconds: int = 60,
        key_func: Optional[Callable[[Request], str]] = None
    ) -> Callable:
        """Create rate limiting middleware."""
        
        # In-memory storage for rate limiting (use Redis in production)
        request_counts = defaultdict(list)
        
        def get_client_key(request: Request) -> str:
            if key_func:
                return key_func(request)
            return request.client_ip or 'unknown'
        
        def rate_limit_middleware(context: MiddlewareContext, next_middleware: Callable) -> Response:
            client_key = get_client_key(context.request)
            now = time.time()
            
            # Clean old requests
            request_counts[client_key] = [
                req_time for req_time in request_counts[client_key]
                if now - req_time < window_seconds
            ]
            
            # Check rate limit
            if len(request_counts[client_key]) >= max_requests:
                return Response(
                    status_code=HttpStatus.SERVICE_UNAVAILABLE,
                    body={
                        'error': 'Rate limit exceeded',
                        'retry_after': window_seconds
                    }
                )
            
            # Add current request
            request_counts[client_key].append(now)
            
            # Add rate limit info to response headers
            response = next_middleware()
            response.set_header('X-RateLimit-Limit', str(max_requests))
            response.set_header('X-RateLimit-Remaining', 
                             str(max_requests - len(request_counts[client_key])))
            response.set_header('X-RateLimit-Reset', 
                             str(int(now + window_seconds)))
            
            return response
        
        return rate_limit_middleware
    
    @staticmethod
    def cors_middleware(
        origins: List[str] = None,
        methods: List[str] = None,
        headers: List[str] = None,
        credentials: bool = False
    ) -> Callable:
        """Create CORS middleware."""
        if origins is None:
            origins = ['*']
        if methods is None:
            methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
        if headers is None:
            headers = ['Content-Type', 'Authorization']
        
        def cors_middleware(context: MiddlewareContext, next_middleware: Callable) -> Response:
            # Handle preflight requests
            if context.request.method == HttpMethod.OPTIONS:
                response = Response(status_code=HttpStatus.OK)
                response.set_header('Access-Control-Allow-Origin', '*')
                response.set_header('Access-Control-Allow-Methods', ', '.join(methods))
                response.set_header('Access-Control-Allow-Headers', ', '.join(headers))
                if credentials:
                    response.set_header('Access-Control-Allow-Credentials', 'true')
                return response
            
            # Handle regular requests
            response = next_middleware()
            response.set_header('Access-Control-Allow-Origin', '*')
            response.set_header('Access-Control-Allow-Methods', ', '.join(methods))
            response.set_header('Access-Control-Allow-Headers', ', '.join(headers))
            if credentials:
                response.set_header('Access-Control-Allow-Credentials', 'true')
            
            return response
        
        return cors_middleware
    
    @staticmethod
    def request_validation_middleware(
        required_fields: Optional[List[str]] = None,
        max_body_size: int = 1024 * 1024,  # 1MB
        allowed_content_types: Optional[List[str]] = None
    ) -> Callable:
        """Create request validation middleware."""
        if allowed_content_types is None:
            allowed_content_types = ['application/json', 'application/x-www-form-urlencoded']
        
        def validation_middleware(context: MiddlewareContext, next_middleware: Callable) -> Response:
            request = context.request
            
            # Check content type
            content_type = request.get_header('Content-Type', '')
            if request.method in [HttpMethod.POST, HttpMethod.PUT, HttpMethod.PATCH]:
                if not any(ct in content_type for ct in allowed_content_types):
                    return Response(
                        status_code=HttpStatus.BAD_REQUEST,
                        body={'error': 'Unsupported content type'}
                    )
            
            # Check body size
            if request.raw_body and len(request.raw_body) > max_body_size:
                return Response(
                    status_code=HttpStatus.BAD_REQUEST,
                    body={'error': 'Request body too large'}
                )
            
            # Validate required fields for POST/PUT requests
            if required_fields and request.method in [HttpMethod.POST, HttpMethod.PUT]:
                body = request.get_body_as_dict()
                missing_fields = [field for field in required_fields if field not in body]
                if missing_fields:
                    return Response(
                        status_code=HttpStatus.BAD_REQUEST,
                        body={'error': 'Missing required fields', 'fields': missing_fields}
                    )
            
            return next_middleware()
        
        return validation_middleware
    
    @staticmethod
    def error_handling_middleware() -> Callable:
        """Create error handling middleware."""
        
        def error_middleware(context: MiddlewareContext, next_middleware: Callable) -> Response:
            try:
                return next_middleware()
            except Exception as e:
                # Log the error
                logging.error(f"Error in middleware chain: {str(e)}", exc_info=True)
                
                return Response(
                    status_code=HttpStatus.INTERNAL_SERVER_ERROR,
                    body={
                        'error': 'Internal server error',
                        'message': str(e) if context.request.get_header('X-Debug') else 'An error occurred'
                    }
                )
        
        return error_middleware
    
    @staticmethod
    def caching_middleware(
        cache_duration: int = 300,  # 5 minutes
        cache_key_func: Optional[Callable[[Request], str]] = None
    ) -> Callable:
        """Create caching middleware (in-memory cache)."""
        
        # Simple in-memory cache (use Redis in production)
        cache = {}
        
        def get_cache_key(request: Request) -> str:
            if cache_key_func:
                return cache_key_func(request)
            return f"{request.method.value}:{request.path}:{hash(str(request.query_params))}"
        
        def cache_middleware(context: MiddlewareContext, next_middleware: Callable) -> Response:
            # Only cache GET requests
            if context.request.method != HttpMethod.GET:
                return next_middleware()
            
            cache_key = get_cache_key(context.request)
            now = time.time()
            
            # Check cache
            if cache_key in cache:
                cached_response, timestamp = cache[cache_key]
                if now - timestamp < cache_duration:
                    # Add cache headers
                    cached_response.set_header('X-Cache', 'HIT')
                    cached_response.set_header('X-Cache-Age', str(int(now - timestamp)))
                    return cached_response
            
            # Execute handler
            response = next_middleware()
            
            # Cache successful responses
            if response.status_code == HttpStatus.OK:
                cache[cache_key] = (response, now)
                response.set_header('X-Cache', 'MISS')
            
            return response
        
        return cache_middleware
    
    @staticmethod
    def metrics_middleware(metrics_collector: Optional[Dict[str, Any]] = None) -> Callable:
        """Create metrics collection middleware."""
        if metrics_collector is None:
            metrics_collector = {
                'request_count': 0,
                'response_times': [],
                'status_codes': defaultdict(int)
            }
        
        def metrics_middleware(context: MiddlewareContext, next_middleware: Callable) -> Response:
            start_time = time.time()
            
            # Increment request count
            metrics_collector['request_count'] += 1
            
            # Execute handler
            response = next_middleware()
            
            # Record metrics
            duration = time.time() - start_time
            metrics_collector['response_times'].append(duration)
            metrics_collector['status_codes'][response.status_code.value] += 1
            
            # Keep only last 1000 response times
            if len(metrics_collector['response_times']) > 1000:
                metrics_collector['response_times'] = metrics_collector['response_times'][-1000:]
            
            # Add metrics headers
            response.set_header('X-Response-Time', f"{duration:.3f}s")
            response.set_header('X-Request-Count', str(metrics_collector['request_count']))
            
            return response
        
        return metrics_middleware


class MiddlewareComposer:
    """Utility class for composing multiple middleware functions."""
    
    @staticmethod
    def compose(*middleware_functions: Callable) -> Callable:
        """Compose multiple middleware functions into a single middleware."""
        
        def composed_middleware(context: MiddlewareContext, next_middleware: Callable) -> Response:
            # Create a chain of middleware functions
            def create_chain(index: int) -> Callable:
                if index >= len(middleware_functions):
                    return next_middleware
                
                current_middleware = middleware_functions[index]
                
                def middleware_wrapper() -> Response:
                    return current_middleware(context, create_chain(index + 1))
                
                return middleware_wrapper
            
            return create_chain(0)()
        
        return composed_middleware
    
    @staticmethod
    def create_standard_stack(
        enable_logging: bool = True,
        enable_auth: bool = False,
        enable_rate_limiting: bool = False,
        enable_cors: bool = True,
        enable_validation: bool = True,
        enable_caching: bool = False,
        enable_metrics: bool = False
    ) -> List[Callable]:
        """Create a standard middleware stack with common middleware."""
        stack = []
        
        if enable_logging:
            stack.append(MiddlewareFactory.logging_middleware())
        
        if enable_auth:
            stack.append(MiddlewareFactory.authentication_middleware())
        
        if enable_rate_limiting:
            stack.append(MiddlewareFactory.rate_limiting_middleware())
        
        if enable_cors:
            stack.append(MiddlewareFactory.cors_middleware())
        
        if enable_validation:
            stack.append(MiddlewareFactory.request_validation_middleware())
        
        if enable_caching:
            stack.append(MiddlewareFactory.caching_middleware())
        
        if enable_metrics:
            stack.append(MiddlewareFactory.metrics_middleware())
        
        # Always add error handling at the end
        stack.append(MiddlewareFactory.error_handling_middleware())
        
        return stack 