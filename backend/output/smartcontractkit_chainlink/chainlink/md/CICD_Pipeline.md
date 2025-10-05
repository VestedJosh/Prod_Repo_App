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
* [GNUmakefile]()
* [core/chainlink.Dockerfile]()
* [plugins/chainlink.Dockerfile]()
* [tools/bin/lint]()

## Purpose and Scope

This document covers the Continuous Integration and Continuous Deployment (CI/CD) infrastructure for the Chainlink repository. The CI/CD system orchestrates code validation, automated testing, Docker image building, and deployment processes across multiple environments and blockchain networks.

For information about the testing framework and test execution, see [Testing Framework](). For detailed build system mechanics and deployment processes, see [Build and Deployment System]().

## CI/CD Architecture Overview

The Chainlink CI/CD pipeline consists of multiple GitHub Actions workflows that handle different aspects of the development and deployment lifecycle. The system supports both development workflows (pull requests, feature branches) and production releases (tagged versions).

**Sources:** [.github/workflows/ci-core.yml]() [.github/workflows/integration-tests.yml]() [.github/workflows/build-publish.yml]() [.github/workflows/docker-build.yml]()

## Core CI Workflow

The `ci-core.yml` workflow serves as the primary code quality gate, executing on every pull request and key branch updates. It implements a sophisticated change detection system and runs appropriate test suites based on affected code paths.

**Sources:** [.github/workflows/ci-core.yml21-44]() [.github/workflows/ci-core.yml113-170]() [.github/workflows/ci-core.yml171-409]()

### Change Detection System

The workflow uses `dorny/paths-filter` to implement intelligent change detection, determining which components require testing based on modified files.

**Key Filter Categories:**

* `core-non-ignored`: Excludes deployment, integration-tests, tools, documentation
* `deployment`: Changes in deployment module
* `workflow`: Changes affecting CI workflow definitions

**Sources:** [.github/workflows/ci-core.yml51-96]()

### Test Matrix Configuration

The core testing matrix adapts execution based on event type and runner availability:

| Test Type | Runner Selection | Conditions |
| --- | --- | --- |
| `go_core_tests` | Self-hosted or GitHub | Always runs |
| `go_core_tests_integration` | Self-hosted or GitHub | Core changes detected |
| `go_core_fuzz` | Self-hosted or GitHub | Core changes detected |
| `go_core_race_tests` | High-memory runners | Core changes detected |
| `go_core_ccip_deployment_tests` | High-CPU runners | Deployment changes detected |

**Sources:** [.github/workflows/ci-core.yml176-209]() [.github/workflows/ci-core.yml620-677]()

## Integration Tests Workflow

The `integration-tests.yml` workflow orchestrates end-to-end testing and Docker image building for integration scenarios. It handles multiple test categories (Core, CRE, CCIP) with different execution contexts.

**Sources:** [.github/workflows/integration-tests.yml85-155]() [.github/workflows/integration-tests.yml157-209]() [.github/workflows/integration-tests.yml210-381]()

### Test Category Matrix

The integration tests workflow supports multiple test categories with different scope and focus:

| Category | Scope | Change Triggers |
| --- | --- | --- |
| Core E2E | Basic Chainlink functionality | `core_changes`, `github_ci_changes` |
| CRE E2E | Capability Registry Engine | `cre_changes`, `github_ci_changes` |
| CCIP E2E | Cross-Chain Interoperability Protocol | `ccip_changes`, `github_ci_changes` |

**Sources:** [.github/workflows/integration-tests.yml108-131]()

### Reusable Test Execution

All E2E test categories delegate to the reusable `smartcontractkit/.github/.github/workflows/run-e2e-tests.yml` workflow, providing consistent execution patterns across different test contexts.

**Sources:** [.github/workflows/integration-tests.yml220-251]() [.github/workflows/integration-tests.yml263-294]()

## Build and Publish Workflow

The `build-publish.yml` workflow handles official release builds, image signing, and publication to container registries. It executes exclusively on tagged releases and implements comprehensive security validation.

**Sources:** [.github/workflows/build-publish.yml12-61]() [.github/workflows/build-publish.yml62-101]() [.github/workflows/build-publish.yml103-135]()

### Release Tag Classification

The build system automatically detects release type based on tag patterns:

| Tag Pattern | Image Target | Configuration |
| --- | --- | --- |
| `v*.*.*-ccip*` | `chainlink/ccip` | CCIP-specific config |
| `v*.*.*` (standard) | `chainlink/chainlink` | Standard config |

**Sources:** [.github/workflows/build-publish.yml27-46]()

### Build Signing and Security

All release images undergo cryptographic signing using `cosign` with keyless OIDC-based signatures:

* **Signing**: Automatic keyless signing via GitHub OIDC
* **Verification**: Certificate chain validation against GitHub identity
* **Attestation**: SLSA build provenance generation

**Sources:** [.github/actions/build-sign-publish-chainlink/action.yml252-271]()

## Docker Build System

The Docker build system supports multiple image variants optimized for different deployment scenarios and includes comprehensive plugin integration.

**Sources:** [core/chainlink.Dockerfile1-103]() [plugins/chainlink.Dockerfile1-103]() [GNUmakefile64-87]()

### Multi-Stage Build Process

Both core and plugins images use multi-stage builds for optimal size and security:

1. **Build Stage** (`golang:1.24-bullseye`): Compilation and plugin installation
2. **Final Stage** (`ubuntu:24.04`): Runtime environment with minimal footprint

**Sources:** [core/chainlink.Dockerfile2-31]() [core/chainlink.Dockerfile56-103]() [plugins/chainlink.Dockerfile4-53]() [plugins/chainlink.Dockerfile57-103]()

### Plugin Installation System

The plugins image supports both public and private plugin ecosystems:

| Plugin Category | Installation Command | Access Level |
| --- | --- | --- |
| Public | `make install-plugins-public` | Open source |
| Private | `make install-plugins-private` | Authenticated |
| Local | `make install-plugins-local` | In-tree |

**Sources:** [GNUmakefile68-87]() [plugins/chainlink.Dockerfile31-40]()

## Make-based Build System

The `GNUmakefile` provides the foundational build system that CI/CD workflows invoke for compilation, testing, and artifact generation.

**Sources:** [GNUmakefile13-254]()

### Build Configuration

The build system uses several key environment variables and build flags:

| Variable | Purpose | Default |
| --- | --- | --- |
| `COMMIT_SHA` | Git commit for build metadata | Current HEAD |
| `VERSION` | Semantic version from package.json | From package.json |
| `GO_LDFLAGS` | Linker flags for Go build | From tools/bin/ldflags |
| `CL_INSTALL_PRIVATE_PLUGINS` | Enable private plugin installation | false |

**Sources:** [GNUmakefile3-11]() [GNUmakefile108-120]()

## Specialized Testing Workflows

Beyond the core CI/CD pipelines, the repository includes numerous specialized workflows for domain-specific testing scenarios.

### Automation Testing Suite

| Workflow | Purpose | Trigger |
| --- | --- | --- |
| `automation-nightly-tests.yml` | Scheduled regression testing | Daily cron |
| `automation-ondemand-tests.yml` | Manual test execution | workflow\_dispatch |
| `automation-benchmark-tests.yml` | Performance validation | workflow\_dispatch |
| `automation-load-tests.yml` | Load testing | workflow\_dispatch |

**Sources:** [.github/workflows/automation-nightly-tests.yml]() [.github/workflows/automation-ondemand-tests.yml]() [.github/workflows/automation-benchmark-tests.yml]() [.github/workflows/automation-load-tests.yml]()

### VRF Testing Suite

| Workflow | Purpose | Test Scope |
| --- | --- | --- |
| `on-demand-vrfv2-smoke-tests.yml` | VRF v2 smoke testing | Basic functionality |
| `on-demand-vrfv2plus-smoke-tests.yml` | VRF v2+ smoke testing | Enhanced features |
| `on-demand-vrfv2-performance-test.yml` | VRF v2 performance | Load scenarios |
| `on-demand-vrfv2plus-performance-test.yml` | VRF v2+ performance | Enhanced load scenarios |

**Sources:** [.github/workflows/on-demand-vrfv2-smoke-tests.yml]() [.github/workflows/on-demand-vrfv2plus-smoke-tests.yml]() [.github/workflows/on-demand-vrfv2-performance-test.yml]() [.github/workflows/on-demand-vrfv2plus-performance-test.yml]()

### Security and Quality Workflows

| Workflow | Purpose | Frequency |
| --- | --- | --- |
| `dependency-check.yml` | Vulnerability scanning | On dependency changes |
| `lint-gh-workflows.yml` | Workflow validation | On push |
| `sync-develop-from-smartcontractkit-chainlink.yml` | Repository synchronization | Every 30 minutes |

**Sources:** [.github/workflows/dependency-check.yml]() [.github/workflows/lint-gh-workflows.yml]() [.github/workflows/sync-develop-from-smartcontractkit-chainlink.yml]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [CI/CD Pipeline]()
* [Purpose and Scope]()
* [CI/CD Architecture Overview]()
* [Core CI Workflow]()
* [Change Detection System]()
* [Test Matrix Configuration]()
* [Integration Tests Workflow]()
* [Test Category Matrix]()
* [Reusable Test Execution]()
* [Build and Publish Workflow]()
* [Release Tag Classification]()
* [Build Signing and Security]()
* [Docker Build System]()
* [Multi-Stage Build Process]()
* [Plugin Installation System]()
* [Make-based Build System]()
* [Build Configuration]()
* [Specialized Testing Workflows]()
* [Automation Testing Suite]()
* [VRF Testing Suite]()
* [Security and Quality Workflows]()