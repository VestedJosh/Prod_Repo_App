* [core/services/job/orm.go]()
* [core/services/job/runner\_integration\_test.go]()
* [core/services/job/spawner\_test.go]()
* [core/services/ocr2/delegate.go]()
* [core/services/pipeline/mocks/config.go]()
* [core/services/pipeline/mocks/orm.go]()
* [core/services/pipeline/mocks/pipeline\_param\_unmarshaler.go]()
* [core/services/pipeline/mocks/runner.go]()
* [core/services/relay/evm/evm.go]()
* [core/testdata/testspecs/v2\_specs.go]()
* [core/web/jobs\_controller.go]()
* [core/web/jobs\_controller\_test.go]()
* [core/web/pipeline\_runs\_controller.go]()
* [core/web/pipeline\_runs\_controller\_test.go]()
* [core/web/presenters/job.go]()
* [core/web/presenters/job\_test.go]()
* [core/web/resolver/spec.go]()
* [core/web/resolver/spec\_test.go]()
* [core/web/schema/type/spec.graphql]()

This document covers the core services architecture of the Chainlink node, focusing on the central orchestration layer that manages job lifecycle, pipeline execution, and service coordination. The core services layer sits between the application entry points and the blockchain integration layer, providing the fundamental job management and execution infrastructure.

For information about specific job types and their implementations, see [Job System](). For pipeline task execution details, see [Pipeline System](). For blockchain-specific integrations, see [Blockchain Integration]().

## Application Architecture

The core services are orchestrated by the `chainlink.Application` which serves as the central coordinator for all node operations. The application manages the lifecycle of services, coordinates job execution, and provides the runtime environment for the Chainlink node.

### Core Application Structure

The `ChainlinkApplication` struct contains all the core components needed for node operation, including job management, pipeline execution, and service coordination.

**Sources:** [core/services/chainlink/application.go157-187]()

### Application Initialization

The application initialization process sets up all required services and their dependencies:

The application creates delegates for each supported job type and registers all services with the health checker for monitoring.

**Sources:** [core/services/chainlink/application.go272-757]() [core/services/chainlink/application.go500-685]()

## Job Management System

The job management system is the core of the Chainlink node's functionality, responsible for creating, managing, and executing jobs. It consists of the Job ORM for persistence, the Job Spawner for lifecycle management, and various delegates for job-specific logic.

### Job Spawner Architecture

The `job.Spawner` manages the complete lifecycle of jobs, from creation through deletion, coordinating with job-specific delegates to create and manage the appropriate services.

**Sources:** [core/services/job/spawner\_test.go112-189]()

### Job Creation and Lifecycle

The job lifecycle involves creation through the ORM, service instantiation through delegates, and proper cleanup on deletion.

**Sources:** [core/services/job/spawner\_test.go132-189]() [core/services/chainlink/application.go129-134]()

### Job Types and Delegates

The system supports multiple job types, each with its own delegate that knows how to create and manage the appropriate services:

| Job Type | Delegate | Purpose |
| --- | --- | --- |
| `DirectRequest` | `directrequest.Delegate` | Handle direct blockchain requests |
| `FluxMonitor` | `fluxmonitorv2.Delegate` | Monitor price feeds |
| `OffchainReporting` | `ocr.Delegate` | OCR consensus protocol |
| `OffchainReporting2` | `ocr2.Delegate` | OCR2 consensus protocol |
| `Keeper` | `keeper.Delegate` | Automated upkeep tasks |
| `VRF` | `vrf.Delegate` | Verifiable random function |
| `Webhook` | `webhook.Delegate` | HTTP webhook endpoints |
| `Cron` | `cron.Delegate` | Scheduled task execution |
| `Workflow` | `workflows.Delegate` | Multi-step workflow execution |

**Sources:** [core/services/chainlink/application.go500-578]() [core/services/job/models.go39-57]()

## Pipeline Integration

The core services integrate tightly with the pipeline system to execute job tasks. The `pipeline.Runner` is responsible for executing the task graphs defined in job specifications.

### Pipeline Runner Integration

The pipeline runner executes the directed acyclic graph (DAG) of tasks defined in each job's pipeline specification.

**Sources:** [core/services/chainlink/application.go469-478]() [core/services/job/runner\_integration\_test.go96-104]()

## Service Lifecycle Management

The core services implement a comprehensive service lifecycle management system that ensures proper startup, health monitoring, and shutdown coordination.

### Service Registration and Health Monitoring

All services are registered with the health checker which monitors their status and coordinates startup/shutdown sequences.

**Sources:** [core/services/chainlink/application.go678-726]() [core/services/chainlink/application.go1007-1060]()

### Application Start/Stop Sequence

The application coordinates the startup and shutdown of all services, ensuring proper dependency ordering and graceful shutdown.

**Sources:** [core/services/chainlink/application.go1007-1060]() [core/services/chainlink/application.go1062-1113]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Core Services]()
* [Application Architecture]()
* [Core Application Structure]()
* [Application Initialization]()
* [Job Management System]()
* [Job Spawner Architecture]()
* [Job Creation and Lifecycle]()
* [Job Types and Delegates]()
* [Pipeline Integration]()
* [Pipeline Runner Integration]()
* [Service Lifecycle Management]()
* [Service Registration and Health Monitoring]()
* [Application Start/Stop Sequence]()