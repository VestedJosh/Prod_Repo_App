Sources: [core/web/router.go], [core/cmd/app.go]

Web Server Architecture
-----------------------

### Initialization

The web server is built with the Gin web framework and configured during application startup. The main router is initialized in the `NewRouter` function, which sets up middleware, routes, and authentication.

Sources: [core/web/router.go:47-102]

The router creates several route groups with different authentication requirements and rate limiting settings. It applies middleware such as CORS, secure connections, logging, and request size limiting.

### Key Middleware Components

The web server uses several middleware components:

| Middleware | Purpose |
| --- | --- |
| OpenTelemetry | Provides tracing for web requests |
| RequestSizeLimiter | Limits the size of incoming requests |
| Logger | Logs HTTP requests with detailed information |
| Recovery | Recovers from panics during request handling |
| CORS | Manages Cross-Origin Resource Sharing |
| SecureMiddleware | Handles TLS redirection and security headers |
| RateLimiter | Limits request rates to prevent abuse |
| Sessions | Manages user sessions |
| Authentication | Verifies user authentication |

Sources: [core/web/router.go:61-86]

API Routes and Controllers
--------------------------

The API is organized into several route groups and controllers for different functional areas:

Sources: [core/web/router.go:88-102], [core/web/router.go:234-432]

### Main API Route Groups

The web API is organized into the following route groups:

1. **v2** - Core API endpoints with authentication required
2. **debug** - Debug information endpoints
3. **health** - Health check endpoints
4. **sessions** - Authentication endpoints
5. **loop** - Plugin discovery and metrics
6. **metrics** - Prometheus metrics (optional)

### V2 API Routes

The v2 routes provide the main API functionality and are organized by resource type. Most of these routes require authentication.

Here's a summary of key v2 endpoints:

| Route Group | Description | Key Endpoints |
| --- | --- | --- |
| users | User management | GET, POST, PATCH, DELETE |
| external\_initiators | External initiator management | GET, POST, DELETE |
| bridge\_types | Bridge adapter management | GET, POST, PATCH, DELETE |
| transfers | Asset transfers | POST |
| config | Node configuration | GET |
| keys | Cryptographic key management | GET, POST, DELETE, IMPORT, EXPORT |
| jobs | Job management | GET, POST, PUT, DELETE |
| log | Log configuration | GET, PATCH |
| pipeline | Pipeline execution | GET, POST, PATCH |
| chains | Chain configuration | GET |
| nodes | Node configuration | GET |

Sources: [core/web/router.go:234-431]

Frontend and UI
---------------

The Chainlink node provides a web-based operator UI served as static assets. The UI is a React application that communicates with the backend API.

### Static Asset Serving

The static assets for the UI are embedded in the application binary. These are served from the /assets path with optional rate limiting.

Sources: [core/web/router.go:436-506]

The web server serves:

* Static assets at `/assets/*` paths
* The React application's `index.html` for any unmatched routes (except API paths)
* API endpoints at `/v2/*` and other API paths

Authentication and Security
---------------------------

The API supports multiple authentication methods:

1. **Session-based Authentication**: Cookie-based sessions for the web UI
2. **API Token Authentication**: Token-based authentication for API clients
3. **External Initiator Authentication**: Special authentication for external job initiators

### Authentication Middleware

Authentication is handled by middleware that verifies the user's credentials before allowing access to protected routes. Different routes have different authentication requirements.

Sources: [core/web/router.go:240-243], [core/web/router.go:424-432]

### Rate Limiting

The API implements rate limiting to prevent abuse. Different rate limits apply to authenticated and unauthenticated requests:

Sources: [core/web/router.go:79-86], [core/web/router.go:207-211]

GraphQL API
-----------

In addition to the REST API, Chainlink provides a GraphQL API for more flexible queries. The GraphQL API is available at the `/query` endpoint.

Sources: [core/web/router.go:96-100], [core/web/router.go:105-130]

The GraphQL API uses the same authentication mechanisms as the REST API and provides a single endpoint that can efficiently query multiple resources using the DataLoader pattern to avoid N+1 query problems.

CLI HTTP Client
---------------

The Chainlink command-line interface (CLI) communicates with the node's API through an HTTP client. This client handles authentication and provides methods for making API requests.

Sources: [core/cmd/app.go:96-123]

Key Components and Classes
--------------------------

The web API system consists of several key components:

| Component | Purpose | Implementation |
| --- | --- | --- |
| Router | Sets up routes and middleware | [core/web/router.go:NewRouter] |
| Controllers | Handle API requests | Various files in core/web/ |
| Middleware | Process requests before controllers | [core/web/router.go] |
| Presenters | Format API responses | [core/web/presenters] |
| Authenticator | Handle user authentication | [core/web/auth] |
| HTTP Client | Make API requests | [core/cmd/app.go] |
| Renderer | Format CLI output | [core/cmd/renderer.go] |

Sources: [core/cmd/renderer.go], [core/web/router.go]

Conclusion
----------

The Web API and Frontend system provides a comprehensive interface for interacting with the Chainlink node. It combines a RESTful API, GraphQL interface, and web-based UI to enable node operation and management. The system is designed with security in mind, implementing authentication, rate limiting, and role-based access control to protect sensitive operations.