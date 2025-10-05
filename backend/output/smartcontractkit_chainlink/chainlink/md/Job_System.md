* [core/services/job/mocks/orm.go]()
* [core/services/job/mocks/service\_ctx.go]()
* [core/services/job/mocks/spawner.go]()
* [core/services/job/models.go]()
* [core/services/job/orm.go]()
* [core/services/job/runner\_integration\_test.go]()
* [core/services/job/spawner.go]()
* [core/services/job/spawner\_test.go]()
* [core/services/ocr2/delegate.go]()
* [core/services/periodicbackup/backup.go]()
* [core/services/periodicbackup/backup\_test.go]()
* [core/services/pipeline/mocks/config.go]()
* [core/services/pipeline/mocks/orm.go]()
* [core/services/pipeline/mocks/pipeline\_param\_unmarshaler.go]()
* [core/services/pipeline/mocks/runner.go]()
* [core/services/relay/evm/evm.go]()
* [core/services/synchronization/helpers\_test.go]()
* [core/services/synchronization/metrics.go]()
* [core/services/synchronization/mocks/telem\_client.go]()
* [core/services/synchronization/telemetry\_ingress\_batch\_client.go]()
* [core/services/synchronization/telemetry\_ingress\_batch\_client\_test.go]()
* [core/services/synchronization/telemetry\_ingress\_batch\_worker.go]()
* [core/services/synchronization/telemetry\_ingress\_batch\_worker\_test.go]()
* [core/services/synchronization/telemetry\_ingress\_client.go]()
* [core/services/synchronization/telemetry\_ingress\_client\_test.go]()
* [core/services/vrf/delegate.go]()
* [core/services/vrf/delegate\_test.go]()
* [core/services/webhook/mocks/external\_initiator\_manager.go]()
* [core/services/webhook/mocks/http\_client.go]()
* [core/testdata/testspecs/v2\_specs.go]()
* [core/utils/http/http.go]()
* [core/utils/http/http\_allowed\_ips.go]()
* [core/utils/http/http\_allowed\_ips\_test.go]()
* [core/utils/utils.go]()
* [core/utils/utils\_test.go]()
* [core/web/jobs\_controller.go]()
* [core/web/jobs\_controller\_test.go]()
* [core/web/pipeline\_runs\_controller.go]()
* [core/web/pipeline\_runs\_controller\_test.go]()
* [core/web/presenters/job.go]()
* [core/web/presenters/job\_test.go]()
* [core/web/resolver/spec.go]()
* [core/web/resolver/spec\_test.go]()
* [core/web/schema/type/spec.graphql]()

The Chainlink Job System manages the lifecycle of jobs within a Chainlink node through a coordinated architecture of spawners, delegates, and persistent storage. The system handles job creation, service instantiation, execution coordination, and cleanup through a delegate pattern that allows type-specific implementations while maintaining consistent lifecycle management.

## Overview

The Job System centers around the `job.Spawner` component, which coordinates with type-specific `job.Delegate` implementations to manage job services. The system persists job specifications through `job.ORM` and maintains active job state through service lifecycle management.

### Job System Architecture

Sources: [core/services/job/spawner.go45-57]() [core/services/chainlink/application.go500-577]() [core/services/job/orm.go44-86]()

## Job Types

Chainlink supports numerous job types that serve different purposes within the oracle ecosystem. Each job type is designed for specific use cases and has its own configuration parameters and behavior.

Sources: [core/services/job/models.go38-58]()

### Common Job Types

| Job Type | Description | Trigger Mechanism |
| --- | --- | --- |
| DirectRequest | Responds to on-chain requests for data | On-chain event (log) |
| Cron | Executes tasks on a schedule | Time-based schedule |
| FluxMonitor | Monitors and reports price data | Polling and on-chain events |
| OCR / OCR2 | Off-chain reporting for decentralized oracle networks | Protocol-specific |
| VRF | Provides verifiable randomness | On-chain request |
| Keeper | Performs automated maintenance of smart contracts | Polling on-chain state |
| Webhook | Executes in response to HTTP requests | HTTP request |

Sources: [core/services/job/models.go38-58]() [core/web/jobs\_controller.go12-35]()

## Job Spawner

The `job.Spawner` is the central orchestrator for job lifecycle management. It maintains a registry of type-specific delegates and manages active job state through the `activeJob` data structure.

### Spawner Implementation

The `spawner` struct implements the `Spawner` interface and maintains thread-safe access to active jobs through `activeJobsMu`. The `jobTypeDelegates` map routes job creation to appropriate delegates based on `job.Type`.

Sources: [core/services/job/spawner.go45-57]() [core/services/job/spawner.go79-84]()

### Spawner Initialization

The spawner is initialized in the main application with a complete delegate registry:

Sources: [core/services/chainlink/application.go500-577]() [core/services/job/spawner.go87-101]()

## Job Delegates

The delegate pattern allows type-specific job implementations while maintaining consistent lifecycle management. Each delegate implements the `job.Delegate` interface and is responsible for creating appropriate services for its job type.

### Delegate Interface

The `ServicesForSpec` method is the core delegate responsibility - it returns a slice of `job.ServiceCtx` instances that implement the job's functionality.

Sources: [core/services/job/spawner.go60-77]()

### Delegate Implementations

#### DirectRequest Delegate

The `directrequest.Delegate` creates log listeners for on-chain oracle requests:

The delegate validates EVM chain configuration and creates listeners that monitor smart contract events.

Sources: [core/services/directrequest/delegate.go44-116]()

#### OCR2 Delegate

The `ocr2.Delegate` handles Off-Chain Reporting jobs with complex service creation:

The OCR2 delegate performs extensive validation including key bundle verification, transmitter address validation, and plugin-specific configuration.

Sources: [core/services/ocr2/delegate.go108-128]() [core/services/ocr2/delegate.go417-539]()

#### VRF Delegate

The `vrf.Delegate` manages Verifiable Random Function services:

Sources: [core/services/vrf/delegate.go35-70]()

### Service Creation Pattern

All delegates follow a consistent pattern for service creation:

Sources: [core/services/job/spawner.go200-244]()

## Job ORM and Data Management

The `job.ORM` interface provides persistent storage for job specifications and metadata. The ORM handles validation, foreign key relationships, and job-specific database operations.

### ORM Interface

Sources: [core/services/job/orm.go44-86]() [core/services/job/orm.go92-98]()

### Job Validation and Creation

The ORM performs comprehensive validation during job creation:

The validation process includes:

* Key bundle existence verification for OCR jobs
* Transmitter address validation for EVM jobs
* Bridge existence checks for pipeline tasks
* Chain ID and contract address validation
* Plugin-specific configuration validation

Sources: [core/services/job/orm.go173-533]()

## Active Job Management

The spawner maintains active job state through the `activeJob` structure and provides thread-safe access to running jobs.

### Active Job Structure

The `activeJobs` map uses job ID as the key and maintains references to the delegate, job specification, and running services.

Sources: [core/services/job/spawner.go79-84]()

### Service Lifecycle Management

Services are started in order and stopped in reverse order to handle dependencies. Each service is registered with the health checker for monitoring.

Sources: [core/services/job/spawner.go188-244]() [core/services/job/spawner.go246-283]()

## Job Lifecycle Management

The job system implements a comprehensive lifecycle management process that coordinates between the API layer, spawner, ORM, and delegates to ensure consistent job creation, execution, and cleanup.

### Job Creation Flow

Sources: [core/services/job/spawner.go200-244]() [core/services/job/orm.go173-533]() [core/web/jobs\_controller.go122-177]()

### Job Deletion Flow

Sources: [core/services/job/spawner.go246-283]() [core/web/jobs\_controller.go178-196]()

### Spawner Startup Process

When the Chainlink application starts, the spawner loads and starts all existing jobs:

Sources: [core/services/job/spawner.go127-158]()

### Error Handling and Recovery

The job system includes comprehensive error handling throughout the lifecycle:

The ORM provides error management methods:

* `RecordError(ctx, jobID, description)` - Creates or increments error records
* `DismissError(ctx, errorID)` - Marks errors as dismissed
* `FindSpecError(ctx, id)` - Retrieves specific error details

Sources: [core/services/job/orm.go55-58]() [core/services/job/spawner.go188-244]()

## Job Execution

Jobs are executed differently depending on their type, but typically follow these stages:

Different job types are triggered by different mechanisms:

| Job Type | Trigger Mechanism |
| --- | --- |
| Cron | Internal ticker based on schedule |
| DirectRequest | Log events from blockchain |
| FluxMonitor | On-chain events or polling |
| Keeper | Block events and polling |
| OCR/OCR2 | Protocol-specific triggers |
| VRF | On-chain randomness requests |
| Webhook | HTTP requests |

Sources: [core/services/job/runner\_integration\_test.go104-176]()

## Job System Initialization

When the Chainlink application starts, the Job System is initialized as follows:

Sources: [core/services/chainlink/application.go674-676]() [core/services/job/spawner.go127-158]()

## Job Specification Format

Jobs are defined using TOML specifications. Here's a simplified example of a Cron job specification:

Each job type has its own specific configuration parameters, but most jobs include a pipeline specification in the `observationSource` field, which defines the tasks to execute.

Sources: [core/testdata/testspecs/v2\_specs.go24-36]()

## Web API Interface

The Job System exposes several REST API endpoints for job management:

| Endpoint | Method | Description |
| --- | --- | --- |
| `/v2/jobs` | GET | List all jobs |
| `/v2/jobs` | POST | Create a new job |
| `/v2/jobs/:id` | GET | Get job details |
| `/v2/jobs/:id` | DELETE | Delete a job |
| `/v2/jobs/:id/runs` | GET | List runs for a job |
| `/v2/jobs/:id/runs` | POST | Trigger a job run |

Sources: [core/web/jobs\_controller.go46-196]() [core/web/pipeline\_runs\_controller.go]()

## Integration with Other Systems

The Job System integrates with several other components of the Chainlink node:

Sources: [core/services/chainlink/application.go489-505]()

## Error Handling and Monitoring

The Job System includes mechanisms for recording and tracking errors:

* Jobs have associated `SpecError` records that track errors encountered during execution
* The `JobORM` provides methods like `RecordError` and `DismissError` to manage these errors
* The `JobSpawner` registers job services with a health checker for monitoring

Sources: [core/services/job/orm.go246-245]() [core/services/job/spawner.go188-194]()

## Conclusion

The Job System is a central component of the Chainlink node that manages the lifecycle of various jobs. It provides a unified interface for creating, executing, and deleting jobs of different types, each with its own specific behavior and configuration. The Job System interacts with many other components of the Chainlink node, enabling the automation of various tasks related to blockchain interaction, external API calls, and data processing.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Job System]()
* [Overview]()
* [Job System Architecture]()
* [Job Types]()
* [Common Job Types]()
* [Job Spawner]()
* [Spawner Implementation]()
* [Spawner Initialization]()
* [Job Delegates]()
* [Delegate Interface]()
* [Delegate Implementations]()
* [DirectRequest Delegate]()
* [OCR2 Delegate]()
* [VRF Delegate]()
* [Service Creation Pattern]()
* [Job ORM and Data Management]()
* [ORM Interface]()
* [Job Validation and Creation]()
* [Active Job Management]()
* [Active Job Structure]()
* [Service Lifecycle Management]()
* [Job Lifecycle Management]()
* [Job Creation Flow]()
* [Job Deletion Flow]()
* [Spawner Startup Process]()
* [Error Handling and Recovery]()
* [Job Execution]()
* [Job System Initialization]()
* [Job Specification Format]()
* [Web API Interface]()
* [Integration with Other Systems]()
* [Error Handling and Monitoring]()
* [Conclusion]()