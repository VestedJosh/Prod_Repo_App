* [core/web/log\_controller.go]()
* [core/web/log\_controller\_test.go]()
* [core/web/presenters/log.go]()
* [core/web/router.go]()
* [main.go]()
* [main\_test.go]()

This document covers the main entry points and initialization paths for the Chainlink node application, including the binary entry point, CLI interface, web server setup, and application lifecycle management. For information about specific job types and their execution, see [Job System](). For details about the overall system architecture, see [System Architecture]().

## Binary Entry Point

The Chainlink application starts through a simple main function that delegates to the core application logic.

The main entry point is minimal and focuses on process lifecycle management:

**Sources:** [main.go10-12]()

## CLI Application Structure

The CLI application is built using the `urfave/cli` framework and provides both local node operations and remote API client functionality.

### Command Hierarchy

The CLI application is created through `NewApp()` which sets up global flags, command structure, and initialization hooks:

**Sources:** [core/cmd/app.go35-320]()

### Application Factory Pattern

The CLI uses an application factory pattern to create and configure Chainlink application instances:

| Factory Type | Purpose | Authentication |
| --- | --- | --- |
| `InstanceAppFactory` | Basic application creation | None |
| `InstanceAppFactoryWithKeystoreMock` | Test applications with keystore auth | Keystore authentication required |
| `seededAppFactory` | Test applications with seeded data | None |

**Sources:** [core/internal/cltest/mocks.go86-125]()

## Web Server Entry Point

The web server provides the HTTP API interface and web UI for the Chainlink node.

### Router Architecture

The web server is initialized through `NewRouter()` which creates a Gin engine with comprehensive middleware and routing:

**Sources:** [core/web/router.go48-102]()

### Authentication Flow

**Sources:** [core/web/router.go205-216]() [core/web/router.go240-433]()

## Application Lifecycle Management

### Configuration and Initialization

The application follows a structured initialization sequence that handles configuration, database setup, and service startup:

The configuration system supports multiple sources with precedence ordering:

1. Command-line config files (`-c` flag)
2. Command-line secrets files (`-s` flag)
3. Environment variables (e.g., `CL_CONFIG`)
4. Default values

**Sources:** [core/cmd/app.go72-133]() [core/cmd/app.go226-279]() [core/cmd/app.go329-335]()

### Service Management

Core services are managed through the `chainlink.Application` interface, which provides lifecycle methods:

| Method | Purpose |
| --- | --- |
| `Start(ctx)` | Initialize and start all services |
| `Stop()` | Gracefully shutdown all services |
| `StopIfStarted()` | Conditional shutdown for cleanup |
| `GetLogger()` | Access the application logger |
| `GetConfig()` | Access configuration |
| `GetKeyStore()` | Access cryptographic key management |

**Sources:** [core/services/chainlink/application.go]() (referenced but not provided)

## Test Application Patterns

The test infrastructure provides multiple patterns for creating application instances in different test scenarios.

### Test Application Factory

### Test Lifecycle Management

Test applications provide automatic cleanup and resource management:

| Method | Purpose |
| --- | --- |
| `Start(ctx)` | Start test application and register cleanup |
| `Stop()` | Stop application and close server |
| `MustSeedNewSession(email)` | Create authenticated test session |
| `NewHTTPClient(*User)` | Create authenticated HTTP client |
| `Import(ctx, content)` | Import private keys for testing |

**Sources:** [core/internal/cltest/cltest.go204-480]() [core/internal/cltest/cltest.go561-594]()

### Test Database Management

The test infrastructure includes comprehensive database management:

**Sources:** [core/store/store.go40-314]()

## Configuration and Server Management

### Configuration Controllers

The web API provides endpoints for runtime configuration management:

| Controller | Endpoint | Purpose |
| --- | --- | --- |
| `ConfigController` | `GET /v2/config` | Retrieve TOML configuration |
| `LogController` | `GET /v2/log` | Get logging configuration |
| `LogController` | `PATCH /v2/log` | Update log levels and SQL logging |

**Sources:** [core/web/config\_controller.go14-54]() [core/web/log\_controller.go16-105]()

### Rendering System

The CLI supports multiple output formats through a renderer interface:

**Sources:** [core/cmd/renderer.go14-181]()

This architecture provides a comprehensive entry point system that supports both interactive CLI usage and programmatic API access, with robust testing infrastructure and configuration management capabilities.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Application Entry Points]()
* [Binary Entry Point]()
* [CLI Application Structure]()
* [Command Hierarchy]()
* [Application Factory Pattern]()
* [Web Server Entry Point]()
* [Router Architecture]()
* [Authentication Flow]()
* [Application Lifecycle Management]()
* [Configuration and Initialization]()
* [Service Management]()
* [Test Application Patterns]()
* [Test Application Factory]()
* [Test Lifecycle Management]()
* [Test Database Management]()
* [Configuration and Server Management]()
* [Configuration Controllers]()
* [Rendering System]()