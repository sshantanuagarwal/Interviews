from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Callable
from enum import Enum
from datetime import datetime
import json


class HttpMethod(Enum):
    """HTTP methods supported by the router."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class HttpStatus(Enum):
    """Common HTTP status codes."""
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


@dataclass
class Request:
    """HTTP request model."""
    method: HttpMethod
    path: str
    headers: Dict[str, str] = field(default_factory=dict)
    query_params: Dict[str, str] = field(default_factory=dict)
    body: Optional[Dict[str, Any]] = None
    raw_body: Optional[str] = None
    client_ip: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_header(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get header value case-insensitively."""
        for header_key, value in self.headers.items():
            if header_key.lower() == key.lower():
                return value
        return default
    
    def get_query_param(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get query parameter value."""
        return self.query_params.get(key, default)
    
    def get_body_as_dict(self) -> Dict[str, Any]:
        """Get request body as dictionary."""
        if self.body:
            return self.body
        if self.raw_body:
            try:
                return json.loads(self.raw_body)
            except json.JSONDecodeError:
                return {}
        return {}


@dataclass
class Response:
    """HTTP response model."""
    status_code: HttpStatus
    headers: Dict[str, str] = field(default_factory=dict)
    body: Optional[Dict[str, Any]] = None
    raw_body: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def set_header(self, key: str, value: str) -> None:
        """Set a response header."""
        self.headers[key] = value
    
    def set_body(self, data: Dict[str, Any]) -> None:
        """Set response body as dictionary."""
        self.body = data
        self.raw_body = json.dumps(data, indent=2)
    
    def set_raw_body(self, data: str) -> None:
        """Set response body as raw string."""
        self.raw_body = data
        self.body = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary for serialization."""
        return {
            'status_code': self.status_code.value,
            'headers': self.headers,
            'body': self.body,
            'raw_body': self.raw_body,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }


@dataclass
class Route:
    """Route definition model."""
    path: str
    method: HttpMethod
    handler: Callable[[Request], Response]
    middleware: List[Callable] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate route after initialization."""
        if not self.path.startswith('/'):
            raise ValueError("Route path must start with '/'")
        
        if not callable(self.handler):
            raise ValueError("Route handler must be callable")


@dataclass
class MiddlewareContext:
    """Context passed between middleware functions."""
    request: Request
    response: Optional[Response] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[Exception] = None
    
    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata in context."""
        self.metadata[key] = value
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata from context."""
        return self.metadata.get(key, default)


@dataclass
class RouterConfig:
    """Configuration for the router."""
    enable_logging: bool = True
    enable_cors: bool = True
    cors_origins: List[str] = field(default_factory=lambda: ["*"])
    cors_methods: List[str] = field(default_factory=lambda: ["GET", "POST", "PUT", "DELETE"])
    cors_headers: List[str] = field(default_factory=lambda: ["Content-Type", "Authorization"])
    max_request_size: int = 1024 * 1024  # 1MB
    timeout_seconds: int = 30
    enable_rate_limiting: bool = False
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds 