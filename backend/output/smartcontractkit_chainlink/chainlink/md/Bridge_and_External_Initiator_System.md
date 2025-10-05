* [.golangci.yml]()
* [.tool-versions]()
* [CHANGELOG.md]()
* [README.md]()
* [contracts/src/v0.8/automation/testhelpers/MockETHUSDAggregator.sol]()
* [core/internal/cltest/job\_factories.go]()
* [core/services/ocr2/plugins/ccip/internal/ccipdata/factory/price\_registry.go]()
* [core/services/webhook/authorizer.go]()
* [core/services/webhook/authorizer\_test.go]()
* [core/services/webhook/external\_initiator\_manager.go]()
* [core/services/webhook/external\_initiator\_manager\_test.go]()
* [core/utils/deferable\_write\_closer\_test.go]()
* [core/web/bridge\_types\_controller.go]()
* [core/web/bridge\_types\_controller\_test.go]()
* [core/web/external\_initiators\_controller.go]()
* [core/web/external\_initiators\_controller\_test.go]()
* [core/web/helpers.go]()
* [core/web/keys\_controller.go]()
* [core/web/ping\_controller\_test.go]()
* [core/web/router\_test.go]()
* [deployment/.golangci.yml]()
* [deployment/data-feeds/README.md]()
* [integration-tests/.golangci.yml]()
* [integration-tests/.tool-versions]()
* [tools/ci/install\_solana]()

## Purpose and Scope

The Bridge and External Initiator System enables Chainlink nodes to integrate with external systems and services. This system provides two key mechanisms: **Bridge Types** for defining external data adapters, and **External Initiators** for allowing external systems to trigger job executions remotely. Together, these components form the foundation for Chainlink's extensibility and external integration capabilities.

For information about job execution and pipeline processing, see [Job System](). For details about webhook job specifications, see [Workflow System]().

## System Architecture

The Bridge and External Initiator System consists of several interconnected components that manage external integrations through REST APIs, webhook communications, and database persistence.

Sources: [core/web/bridge\_types\_controller.go56-59]() [core/web/external\_initiators\_controller.go45-48]() [core/services/webhook/external\_initiator\_manager.go32-37]() [core/services/webhook/authorizer.go27-34]()

## Bridge Types

Bridge Types define external adapters that Chainlink nodes can communicate with for data processing and external API calls. Each bridge type represents a specific external service or adapter.

### Bridge Type Management

The `BridgeTypesController` provides REST API endpoints for managing bridge types:

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/v2/bridge_types` | POST | Create new bridge type |
| `/v2/bridge_types` | GET | List all bridge types |
| `/v2/bridge_types/:name` | GET | Get specific bridge type |
| `/v2/bridge_types/:name` | PATCH | Update bridge type |
| `/v2/bridge_types/:name` | DELETE | Delete bridge type |

Sources: [core/web/bridge\_types\_controller.go61-109]() [core/web/bridge\_types\_controller.go112-123]() [core/web/bridge\_types\_controller.go125-147]()

### Bridge Type Validation

Bridge types undergo validation to ensure they meet required criteria:

* **Name validation**: Must be alphanumeric and follow naming conventions
* **URL validation**: Must have a valid URL endpoint
* **Payment validation**: `MinimumContractPayment` must be non-negative
* **Uniqueness**: Bridge names must be unique across the system

Sources: [core/web/bridge\_types\_controller.go36-54]() [core/web/bridge\_types\_controller.go23-34]()

## External Initiators

External Initiators enable external systems to trigger Chainlink job executions remotely through authenticated HTTP requests. They provide a secure mechanism for external services to initiate job runs.

### External Initiator Components

Sources: [core/web/external\_initiators\_controller.go45-48]() [core/services/webhook/external\_initiator\_manager.go21-26]() [core/services/webhook/authorizer.go17-19]()

### External Initiator Lifecycle

The `ExternalInitiatorManager` handles the complete lifecycle of external initiator communications:

1. **Job Notification**: Notifies external initiators when jobs are created
2. **Job Deletion**: Notifies external initiators when jobs are deleted
3. **Authentication**: Manages secure communication with external services

Sources: [core/services/webhook/external\_initiator\_manager.go47-84]() [core/services/webhook/external\_initiator\_manager.go170-175]()

### JobSpecNotice Structure

When notifying external initiators, the system sends a `JobSpecNotice`:

Sources: [core/services/webhook/external\_initiator\_manager.go170-175]()

## Authorization System

The authorization system controls access to job execution based on user credentials and external initiator permissions.

### Authorization Flow

| Authorizer Type | Condition | Behavior |
| --- | --- | --- |
| `alwaysAuthorizer` | User session present | Always allows execution |
| `eiAuthorizer` | External initiator credentials | Checks database permissions |
| `neverAuthorizer` | No credentials | Always denies execution |

Sources: [core/services/webhook/authorizer.go27-34]() [core/services/webhook/authorizer.go45-62]() [core/services/webhook/authorizer.go64-74]()

## Database Schema

The system uses several database tables to manage bridges and external initiators:

### Key Tables

Sources: [core/services/webhook/external\_initiator\_manager.go86-108]() [core/services/webhook/external\_initiator\_manager.go111-133]()

## REST API Reference

### Bridge Types API

The Bridge Types API provides full CRUD operations for managing external adapters:

Sources: [core/web/bridge\_types\_controller.go61-109]() [core/web/bridge\_types\_controller.go112-147]() [core/web/bridge\_types\_controller.go149-193]() [core/web/bridge\_types\_controller.go195-233]()

### External Initiators API

The External Initiators API manages external initiator lifecycle and permissions:

| Endpoint | Method | Purpose | Response |
| --- | --- | --- | --- |
| `/v2/external_initiators` | GET | List external initiators | Paginated list |
| `/v2/external_initiators` | POST | Create external initiator | Auth credentials |
| `/v2/external_initiators/:name` | DELETE | Delete external initiator | 204 No Content |

Sources: [core/web/external\_initiators\_controller.go50-58]() [core/web/external\_initiators\_controller.go61-100]() [core/web/external\_initiators\_controller.go102-118]()

### Authentication Headers

External initiator communications use specific HTTP headers for authentication:

| Header | Purpose | Usage |
| --- | --- | --- |
| `X-Chainlink-EA-AccessKey` | Access key identification | Incoming requests |
| `X-Chainlink-EA-Secret` | Secret authentication | Incoming requests |
| `Content-Type` | Request format | Always `application/json` |

Sources: [core/services/webhook/external\_initiator\_manager.go197-201]() [core/static/static.go29-30]()

## Configuration and Security

### External Initiator Configuration

External initiators can be enabled or disabled through configuration:

When disabled, external initiators cannot trigger job executions even with valid credentials.

Sources: [core/services/webhook/authorizer.go13-15]() [core/services/webhook/authorizer.go46-48]()

### Security Features

* **Credential Generation**: Automatic generation of access keys and secrets
* **Token-based Authentication**: Separate incoming and outgoing tokens
* **Name Validation**: Alphanumeric names with underscore and dash support
* **URL Validation**: Required valid URLs for external initiator endpoints
* **Audit Logging**: All operations logged for security auditing

Sources: [core/web/external\_initiators\_controller.go27-43]() [core/web/external\_initiators\_controller.go71-80]() [core/web/external\_initiators\_controller.go92-96]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Bridge and External Initiator System]()
* [Purpose and Scope]()
* [System Architecture]()
* [Bridge Types]()
* [Bridge Type Management]()
* [Bridge Type Validation]()
* [External Initiators]()
* [External Initiator Components]()
* [External Initiator Lifecycle]()
* [JobSpecNotice Structure]()
* [Authorization System]()
* [Authorization Flow]()
* [Database Schema]()
* [Key Tables]()
* [REST API Reference]()
* [Bridge Types API]()
* [External Initiators API]()
* [Authentication Headers]()
* [Configuration and Security]()
* [External Initiator Configuration]()
* [Security Features]()