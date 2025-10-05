* [core/services/synchronization/telemetry\_ingress\_batch\_client.go]()
* [core/services/synchronization/telemetry\_ingress\_batch\_client\_test.go]()
* [core/services/synchronization/telemetry\_ingress\_batch\_worker.go]()
* [core/services/synchronization/telemetry\_ingress\_batch\_worker\_test.go]()
* [core/services/synchronization/telemetry\_ingress\_client.go]()
* [core/services/synchronization/telemetry\_ingress\_client\_test.go]()
* [core/services/webhook/mocks/external\_initiator\_manager.go]()
* [core/services/webhook/mocks/http\_client.go]()
* [core/store/migrate/migrations/0151\_bridge\_last\_good\_value\_use\_tz.sql]()
* [core/utils/utils.go]()
* [core/utils/utils\_test.go]()

This document covers the monitoring and telemetry infrastructure within the Chainlink node, specifically focusing on the telemetry ingress system that collects and forwards telemetry data to external monitoring services. The system handles real-time telemetry collection from various job types (OCR, VRF, Functions, etc.) and efficiently transmits this data to telemetry ingress servers via secure WSRPC connections.

For information about the broader job system that generates telemetry data, see [Job System](). For details about configuration of telemetry endpoints, see [Node Configuration]().

## Architecture Overview

The telemetry system consists of multiple clients that collect telemetry data from various sources and forward it to external telemetry ingress servers. The system supports both single-message and batched transmission modes for optimal performance.

Sources: [core/services/synchronization/telemetry\_ingress\_batch\_client.go1-253]() [core/services/synchronization/telemetry\_ingress\_client.go1-184]() [core/services/synchronization/telemetry\_ingress\_batch\_worker.go1-120]()

## Telemetry Service Interface

The telemetry system is built around the `TelemetryService` interface, which provides a unified API for sending telemetry data regardless of the underlying implementation.

The system supports multiple telemetry types for different job categories:

| Telemetry Type | Description | Usage |
| --- | --- | --- |
| `OCR` | Off-Chain Reporting telemetry | Price feed aggregation |
| `OCR2Functions` | Functions-specific OCR2 telemetry | Serverless functions execution |
| `VRF` | Verifiable Random Function telemetry | Random number generation |

Sources: [core/services/synchronization/telemetry\_ingress\_batch\_client.go27-41]() [core/services/synchronization/telemetry\_ingress\_client.go20-36]() [core/services/synchronization/telemetry\_ingress\_batch\_worker.go16-31]()

## Batch Processing System

The batch client creates dedicated workers for each unique combination of contract ID and telemetry type, enabling efficient parallel processing and batching of telemetry data.

### Worker Lifecycle and Configuration

Each worker is configured with specific parameters for optimal performance:

| Parameter | Default Value | Description |
| --- | --- | --- |
| `telemBufferSize` | 100 | Channel buffer size per worker |
| `telemMaxBatchSize` | 50 | Maximum messages per batch |
| `telemSendInterval` | Configurable | How often to send batches |
| `telemSendTimeout` | 1 second | Timeout for RPC calls |

Sources: [core/services/synchronization/telemetry\_ingress\_batch\_client.go75-95]() [core/services/synchronization/telemetry\_ingress\_batch\_worker.go35-57]() [core/services/synchronization/telemetry\_ingress\_batch\_worker.go104-119]()

## Message Buffering and Backpressure

The system implements sophisticated buffering and backpressure handling to prevent memory exhaustion and data loss during high load or connectivity issues.

The exponential backoff logging mechanism prevents log spam while still providing visibility into buffer overflow conditions:

Sources: [core/services/synchronization/telemetry\_ingress\_batch\_client.go201-221]() [core/services/synchronization/telemetry\_ingress\_batch\_worker.go94-101]() [core/services/synchronization/telemetry\_ingress\_client.go158-163]()

## Metrics and Monitoring

The telemetry system exposes comprehensive Prometheus metrics for monitoring connection health, message throughput, and error rates.

### Metrics Configuration

| Metric | Labels | Purpose |
| --- | --- | --- |
| `telemetry_client_connection_status` | `endpoint` | Monitor WSRPC connection health |
| `telemetry_client_messages_sent` | `endpoint`, `telemetry_type` | Track successful transmissions |
| `telemetry_client_messages_send_errors` | `endpoint`, `telemetry_type` | Track transmission failures |
| `telemetry_client_messages_dropped` | `endpoint`, `telemetry_type` | Track buffer overflows |
| `telemetry_client_workers` | `endpoint`, `telemetry_type` | Track worker scaling |

Sources: [core/services/synchronization/metrics.go1-34]() [core/services/synchronization/telemetry\_ingress\_batch\_client.go159-182]() [core/services/synchronization/telemetry\_ingress\_batch\_worker.go68-80]()

## Connection Management and Security

The telemetry system establishes secure WSRPC connections using CSA (Chainlink Signing Authority) keys for authentication and TLS for transport security.

### Authentication Flow

The authentication process uses Ed25519 signatures for secure client identification:

1. **Key Retrieval**: CSA keystore provides the default signing key
2. **Signer Creation**: `core.NewEd25519Signer` wraps the key for signing operations
3. **TLS Setup**: `credentials.NewClientTLSSigner` creates mutual TLS configuration
4. **Connection**: WSRPC establishes authenticated, encrypted connection

Sources: [core/services/synchronization/telemetry\_ingress\_batch\_client.go103-157]() [core/services/synchronization/telemetry\_ingress\_client.go78-117]() [core/services/synchronization/telemetry\_ingress\_batch\_client.go159-182]()

## Error Handling and Resilience

The telemetry system implements multiple layers of error handling to ensure reliable operation under various failure conditions.

Sources: [core/services/synchronization/telemetry\_ingress\_batch\_client.go185-196]() [core/services/synchronization/telemetry\_ingress\_batch\_worker.go67-80]() [core/services/synchronization/telemetry\_ingress\_client.go93-117]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Monitoring and Telemetry]()
* [Architecture Overview]()
* [Telemetry Service Interface]()
* [Batch Processing System]()
* [Worker Lifecycle and Configuration]()
* [Message Buffering and Backpressure]()
* [Metrics and Monitoring]()
* [Metrics Configuration]()
* [Connection Management and Security]()
* [Authentication Flow]()
* [Error Handling and Resilience]()