This system is distinct from the [Pipeline System]() which handles individual task orchestration, and from the [Job System]() which manages job lifecycle. For information about feeds management, see [Feeds Manager]().

## Architecture Overview

The Workflow System is built around the `Engine` struct which serves as the core orchestrator for individual workflow executions. The system integrates with the broader Chainlink architecture through the job system via the `Delegate` pattern.

**Sources:** [core/services/workflows/engine.go108-152]() [core/services/workflows/delegate.go28-36]() [core/services/workflows/models.go37-49]()

## Workflow Representation

Workflows are represented as directed acyclic graphs where each node is a `step` containing a capability to execute. The `workflow` struct encapsulates this graph structure along with metadata and trigger definitions.

**Sources:** [core/services/workflows/models.go37-49]() [core/services/workflows/models.go100-106]() [core/services/workflows/models.go108-118]()

## Engine Execution Model

The `Engine` manages workflow execution through a multi-goroutine architecture with dedicated workers, step update loops, and trigger event handlers. Each workflow execution maintains isolated state while sharing the underlying workflow definition.

**Sources:** [core/services/workflows/engine.go154-188]() [core/services/workflows/engine.go497-547]() [core/services/workflows/engine.go703-765]() [core/services/workflows/engine.go471-495]()

## Step Execution and State Management

Each workflow step execution is managed through a sophisticated state machine with timeout handling, dependency resolution, and result propagation.

**Sources:** [core/services/workflows/engine.go767-859]() [core/services/workflows/engine.go957-1048]() [core/services/workflows/engine.go549-607]() [core/services/workflows/engine.go609-638]()

## Configuration and Capability Integration

The system integrates with the capabilities registry to resolve and configure step capabilities, supporting both local and remote capabilities with configuration merging and secret interpolation.

| Component | Purpose | Key Methods |
| --- | --- | --- |
| `SecretsFor` | Fetches workflow secrets | Function type for secret resolution |
| `configForStep()` | Merges capability and user config | Secret interpolation, registry config |
| `merge()` | Combines configurations | Handles restricted keys and defaults |
| `interpolateEnvVars()` | Environment variable substitution | Uses `exec.FindAndInterpolateEnvVars()` |

**Sources:** [core/services/workflows/engine.go102]() [core/services/workflows/engine.go916-955]() [core/services/workflows/engine.go861-893]() [core/services/workflows/engine.go895-911]()

## Rate Limiting and Resource Management

The Workflow System implements comprehensive rate limiting at multiple levels to prevent resource exhaustion and ensure fair usage across workflow owners.

**Sources:** [core/services/workflows/engine.go735-748]() [core/services/workflows/engine.go160-171]() [core/services/workflows/ratelimiter]() [core/services/workflows/syncerlimiter]()

## Monitoring and Telemetry

The system provides extensive monitoring capabilities including execution tracking, capability invocation metrics, and billing integration.

| Metric Type | Implementation | Purpose |
| --- | --- | --- |
| Execution Events | `events.EmitExecutionStartedEvent()` | Track workflow lifecycle |
| Capability Events | `events.EmitCapabilityStartedEvent()` | Monitor step execution |
| Metering Reports | `metering.Reports` | Resource usage tracking |
| Duration Metrics | Histogram updates | Performance monitoring |
| Error Counters | Various error metrics | Failure rate tracking |

**Sources:** [core/services/workflows/engine.go501-504]() [core/services/workflows/engine.go1022-1025]() [core/services/workflows/engine.go650-663]() [core/services/workflows/events]() [core/services/workflows/metering]()

## Job System Integration

The Workflow System integrates with Chainlink's job management through the `Delegate` pattern, enabling workflows to be managed as standard job types.

**Sources:** [core/services/workflows/delegate.go53-93]() [core/services/workflows/delegate.go115-156]() [core/services/workflows/delegate.go28-36]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Workflow System]()
* [Architecture Overview]()
* [Workflow Representation]()
* [Engine Execution Model]()
* [Step Execution and State Management]()
* [Configuration and Capability Integration]()
* [Rate Limiting and Resource Management]()
* [Monitoring and Telemetry]()
* [Job System Integration]()