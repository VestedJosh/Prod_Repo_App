* [.github/workflows/dependency-check.yml]()
* [.github/workflows/docker-build.yml]()
* [.github/workflows/integration-chaos-tests.yml]()
* [.github/workflows/integration-tests.yml]()
* [.github/workflows/lint-gh-workflows.yml]()
* [.github/workflows/on-demand-ocr-soak-test.yml]()
* [.github/workflows/on-demand-vrfv2-performance-test.yml]()
* [.github/workflows/on-demand-vrfv2-smoke-tests.yml]()
* [.github/workflows/on-demand-vrfv2plus-performance-test.yml]()
* [.github/workflows/on-demand-vrfv2plus-smoke-tests.yml]()
* [.github/workflows/run-nightly-e2e-tests.yml]()
* [.github/workflows/run-selected-e2e-tests.yml]()
* [.github/workflows/sync-develop-from-smartcontractkit-chainlink.yml]()

This document covers the development tools, testing infrastructure, and CI/CD systems that support the Chainlink codebase. It details the comprehensive testing framework, build processes, and quality assurance mechanisms that ensure code reliability and maintainability.

For information about the core application architecture and job systems, see [Core Services](). For details on configuration management, see [Configuration]().

## Overview

The Chainlink repository employs a sophisticated development and testing infrastructure built around GitHub Actions workflows, comprehensive test suites, and automated quality checks. The system supports multiple test types including unit, integration, end-to-end, performance, and chaos testing, all orchestrated through a matrix of CI/CD pipelines.

## CI/CD Pipeline Architecture

The CI/CD system is structured around several key GitHub Actions workflows that handle different aspects of testing, building, and deployment.

### CI/CD Pipeline Overview

Sources: [.github/workflows/ci-core.yml1-717]() [.github/workflows/integration-tests.yml1-800]() [.github/workflows/build-publish.yml1-178]()

### Workflow Execution Matrix

The CI system uses a sophisticated matrix strategy to run tests across different environments and configurations:

| Test Type | Runner Configuration | Triggers | Flakeguard |
| --- | --- | --- | --- |
| `go_core_tests` | Self-hosted or GitHub-hosted | PR, Push, Schedule | Enabled for non-PR |
| `go_core_tests_integration` | Self-hosted or GitHub-hosted | PR, Push, Schedule | Disabled |
| `go_core_fuzz` | Self-hosted or GitHub-hosted | PR, Push, Schedule | Disabled |
| `go_core_race_tests` | Self-hosted or GitHub-hosted | PR, Push, Schedule | Disabled |
| `go_core_ccip_deployment_tests` | Self-hosted or GitHub-hosted | PR, Push, Schedule | Enabled for non-PR |

Sources: [.github/workflows/ci-core.yml176-209]()

## Test Types and Execution

### Core Test Categories

Sources: [.github/workflows/ci-core.yml176-209]() [.github/workflows/integration-tests.yml210-340]()

### Test Infrastructure Components

The testing system relies on several key infrastructure components:

**Test Runners**: The system supports both GitHub-hosted and self-hosted runners, with dynamic selection based on workload and PR labels.

**Database Setup**: PostgreSQL databases are provisioned for tests requiring persistent storage, configured via the `setup-postgres` action.

**External Dependencies**: Tests requiring blockchain interaction use Solana, Aptos, and wasmd components, set up through dedicated actions.

**Plugin Installation**: LOOP plugins are installed for comprehensive testing of the plugin architecture.

Sources: [.github/workflows/ci-core.yml255-284]()

### Flakeguard Integration

The system integrates Flakeguard for test reliability and failure analysis:

Sources: [.github/workflows/ci-core.yml306-368]()

## Build and Deployment System

### Docker Image Build Pipeline

The build system creates multiple Docker image variants for different use cases:

Sources: [.github/actions/build-sign-publish-chainlink/action.yml1-272]() [.github/workflows/docker-build.yml62-187]()

### Build Configuration Matrix

The build system supports multiple configurations based on git tag types and deployment targets:

| Image Type | Dockerfile | Build Args | ECR Repository |
| --- | --- | --- | --- |
| Core | `core/chainlink.Dockerfile` | `CHAINLINK_USER=chainlink, COMMIT_SHA` | `chainlink/chainlink` |
| Core Plugins | `plugins/chainlink.Dockerfile` | `CL_INSTALL_PRIVATE_PLUGINS=true` | `chainlink` |
| CCIP | `core/chainlink.Dockerfile` | `CL_CHAIN_DEFAULTS=/ccip-config` | `ccip` |
| CCIP Plugins | `plugins/chainlink.Dockerfile` | `CL_CHAIN_DEFAULTS=/ccip-config` | `ccip` |

Sources: [.github/workflows/docker-build.yml68-187]()

## Quality Assurance Tools

### Code Quality Pipeline

Sources: [.github/workflows/ci-core.yml113-170]() [.github/workflows/dependency-check.yml23-48]() [.github/workflows/lint-gh-workflows.yml5-15]()

### SonarQube Integration

The system integrates comprehensive SonarQube analysis with dynamic report path discovery:

**Coverage Reports**: Aggregated from `go_core_tests_logs`, `go_core_tests_integration_logs`, and `go_core_scripts_tests_logs`

**Test Reports**: Collected from `output.txt` files across all test artifact directories

**Lint Reports**: Generated from `golangci-lint-report.xml` files across all modules

Sources: [.github/workflows/ci-core.yml456-556]()

## Test Infrastructure and Environments

### Test Environment Configuration

The testing infrastructure supports multiple environment types and configurations:

**Docker Environments**: Containerized test environments for isolation and reproducibility

**Kubernetes Environments**: Full-scale deployments for integration and load testing

**Local Environments**: Development and debugging support with local runners

**Cloud Environments**: AWS-based infrastructure for large-scale testing

### Runner Configuration Strategy

Sources: [.github/workflows/ci-core.yml614-716]()

### Specialized Test Workflows

The system includes numerous specialized test workflows for different components and scenarios:

**Automation Tests**: Benchmark, load, and on-demand testing for automation functionality

**VRF Tests**: Performance and smoke testing for Verifiable Random Function features

**CCIP Tests**: Load testing and integration testing for Cross-Chain Interoperability Protocol

**Chaos Tests**: Failure injection and resilience testing

Each workflow follows the reusable pattern of calling the central `run-e2e-tests.yml` workflow with specific configuration parameters.

Sources: [.github/workflows/automation-benchmark-tests.yml28-62]() [.github/workflows/on-demand-vrfv2plus-performance-test.yml31-106]() [.github/workflows/ccip-load-tests.yml37-74]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Development and Testing]()
* [Overview]()
* [CI/CD Pipeline Architecture]()
* [CI/CD Pipeline Overview]()
* [Workflow Execution Matrix]()
* [Test Types and Execution]()
* [Core Test Categories]()
* [Test Infrastructure Components]()
* [Flakeguard Integration]()
* [Build and Deployment System]()
* [Docker Image Build Pipeline]()
* [Build Configuration Matrix]()
* [Quality Assurance Tools]()
* [Code Quality Pipeline]()
* [SonarQube Integration]()
* [Test Infrastructure and Environments]()
* [Test Environment Configuration]()
* [Runner Configuration Strategy]()
* [Specialized Test Workflows]()