import re
from typing import Dict, List, Callable, Optional, Tuple, Any
from collections import defaultdict
from urllib.parse import urlparse, parse_qs
import time
import logging

from models import Request, Response, Route, MiddlewareContext, HttpMethod, HttpStatus, RouterConfig


class PathMatcher:
    """Handles path matching with parameter extraction."""
    
    def __init__(self):
        self.param_pattern = re.compile(r':(\w+)')
    
    def compile_pattern(self, path: str) -> Tuple[re.Pattern, List[str]]:
        """Compile a path pattern and extract parameter names."""
        # Convert path parameters to regex pattern
        pattern = self.param_pattern.sub(r'([^/]+)', path)
        pattern = f'^{pattern}$'
        
        # Extract parameter names
        param_names = self.param_pattern.findall(path)
        
        return re.compile(pattern), param_names
    
    def match_path(self, pattern: re.Pattern, param_names: List[str], 
                   request_path: str) -> Optional[Dict[str, str]]:
        """Match a request path against a pattern and extract parameters."""
        match = pattern.match(request_path)
        if not match:
            return None
        
        # Extract parameters
        params = {}
        for i, param_name in enumerate(param_names):
            if i + 1 < len(match.groups()):
                params[param_name] = match.group(i + 1)
        
        return params


class MiddlewareRouter:
    """Main router class with middleware support and path-based routing."""
    
    def __init__(self, config: Optional[RouterConfig] = None):
        self.config = config or RouterConfig()
        self.routes: Dict[HttpMethod, List[Route]] = defaultdict(list)
        self.global_middleware: List[Callable] = []
        self.path_matcher = PathMatcher()
        self.logger = self._setup_logger()
        
        # Compile patterns for faster matching
        self._compiled_patterns: Dict[HttpMethod, List[Tuple[re.Pattern, List[str], Route]]] = defaultdict(list)
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for the router."""
        logger = logging.getLogger('MiddlewareRouter')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO if self.config.enable_logging else logging.WARNING)
        return logger
    
    def add_route(self, path: str, method: HttpMethod, 
                  handler: Callable[[Request], Response],
                  middleware: Optional[List[Callable]] = None,
                  metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a route to the router."""
        route = Route(
            path=path,
            method=method,
            handler=handler,
            middleware=middleware or [],
            metadata=metadata or {}
        )
        
        self.routes[method].append(route)
        
        # Compile pattern for faster matching
        pattern, param_names = self.path_matcher.compile_pattern(path)
        self._compiled_patterns[method].append((pattern, param_names, route))
        
        self.logger.info(f"Added route: {method.value} {path}")
    
    def get(self, path: str, handler: Callable[[Request], Response],
            middleware: Optional[List[Callable]] = None,
            metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a GET route."""
        self.add_route(path, HttpMethod.GET, handler, middleware, metadata)
    
    def post(self, path: str, handler: Callable[[Request], Response],
             middleware: Optional[List[Callable]] = None,
             metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a POST route."""
        self.add_route(path, HttpMethod.POST, handler, middleware, metadata)
    
    def put(self, path: str, handler: Callable[[Request], Response],
            middleware: Optional[List[Callable]] = None,
            metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a PUT route."""
        self.add_route(path, HttpMethod.PUT, handler, middleware, metadata)
    
    def delete(self, path: str, handler: Callable[[Request], Response],
               middleware: Optional[List[Callable]] = None,
               metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a DELETE route."""
        self.add_route(path, HttpMethod.DELETE, handler, middleware, metadata)
    
    def patch(self, path: str, handler: Callable[[Request], Response],
              middleware: Optional[List[Callable]] = None,
              metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a PATCH route."""
        self.add_route(path, HttpMethod.PATCH, handler, middleware, metadata)
    
    def add_global_middleware(self, middleware: Callable) -> None:
        """Add global middleware that runs for all requests."""
        self.global_middleware.append(middleware)
        self.logger.info(f"Added global middleware: {middleware.__name__}")
    
    def _parse_request(self, raw_request: Dict[str, Any]) -> Request:
        """Parse raw request data into Request object."""
        # Parse URL and query parameters
        parsed_url = urlparse(raw_request.get('path', '/'))
        query_params = parse_qs(parsed_url.query)
        # Convert query parameters from list to single values
        query_params = {k: v[0] if v else '' for k, v in query_params.items()}
        
        return Request(
            method=HttpMethod(raw_request.get('method', 'GET')),
            path=parsed_url.path,
            headers=raw_request.get('headers', {}),
            query_params=query_params,
            body=raw_request.get('body'),
            raw_body=raw_request.get('raw_body'),
            client_ip=raw_request.get('client_ip'),
            metadata=raw_request.get('metadata', {})
        )
    
    def _find_route(self, request: Request) -> Optional[Tuple[Route, Dict[str, str]]]:
        """Find matching route and extract path parameters."""
        method = request.method
        request_path = request.path
        
        for pattern, param_names, route in self._compiled_patterns[method]:
            params = self.path_matcher.match_path(pattern, param_names, request_path)
            if params is not None:
                # Add path parameters to request metadata
                request.metadata['path_params'] = params
                return route, params
        
        return None
    
    def _execute_middleware_chain(self, context: MiddlewareContext, 
                                 middleware_chain: List[Callable]) -> Response:
        """Execute middleware chain and return response."""
        if not middleware_chain:
            # No middleware, execute handler directly
            return context.request.metadata.get('route').handler(context.request)
        
        def execute_middleware(index: int) -> Response:
            """Recursively execute middleware chain."""
            if index >= len(middleware_chain):
                # End of middleware chain, execute handler
                return context.request.metadata.get('route').handler(context.request)
            
            middleware = middleware_chain[index]
            
            def next_middleware() -> Response:
                return execute_middleware(index + 1)
            
            # Execute middleware with next function
            return middleware(context, next_middleware)
        
        return execute_middleware(0)
    
    def handle_request(self, raw_request: Dict[str, Any]) -> Response:
        """Handle a request and return a response."""
        start_time = time.time()
        
        try:
            # Parse request
            request = self._parse_request(raw_request)
            
            # Create middleware context
            context = MiddlewareContext(request=request)
            
            # Find matching route
            route_match = self._find_route(request)
            if not route_match:
                # No route found
                response = Response(
                    status_code=HttpStatus.NOT_FOUND,
                    body={'error': 'Route not found', 'path': request.path}
                )
                context.response = response
                return response
            
            route, path_params = route_match
            request.metadata['route'] = route
            request.metadata['path_params'] = path_params
            
            # Build middleware chain: global + route-specific
            middleware_chain = self.global_middleware + route.middleware
            
            # Execute middleware chain
            response = self._execute_middleware_chain(context, middleware_chain)
            
            # Add CORS headers if enabled
            if self.config.enable_cors:
                response.set_header('Access-Control-Allow-Origin', '*')
                response.set_header('Access-Control-Allow-Methods', 
                                 ', '.join(self.config.cors_methods))
                response.set_header('Access-Control-Allow-Headers', 
                                 ', '.join(self.config.cors_headers))
            
            # Log request
            duration = time.time() - start_time
            self.logger.info(
                f"{request.method.value} {request.path} - {response.status_code.value} "
                f"({duration:.3f}s)"
            )
            
            return response
            
        except Exception as e:
            # Handle unexpected errors
            self.logger.error(f"Error handling request: {str(e)}", exc_info=True)
            
            return Response(
                status_code=HttpStatus.INTERNAL_SERVER_ERROR,
                body={'error': 'Internal server error', 'message': str(e)}
            )
    
    def get_routes(self) -> Dict[HttpMethod, List[Dict[str, Any]]]:
        """Get all registered routes for inspection."""
        routes_info = {}
        for method, routes in self.routes.items():
            routes_info[method] = []
            for route in routes:
                routes_info[method].append({
                    'path': route.path,
                    'method': route.method.value,
                    'handler': route.handler.__name__,
                    'middleware_count': len(route.middleware),
                    'metadata': route.metadata
                })
        return routes_info
    
    def clear_routes(self) -> None:
        """Clear all registered routes."""
        self.routes.clear()
        self._compiled_patterns.clear()
        self.logger.info("Cleared all routes") 