* [core/web/resolver/testdata/config-multi-chain-effective.toml]()
* [docs/CONFIG.md]()
* [testdata/scripts/node/validate/default.txtar]()
* [testdata/scripts/node/validate/disk-based-logging-disabled.txtar]()
* [testdata/scripts/node/validate/disk-based-logging-no-dir.txtar]()
* [testdata/scripts/node/validate/disk-based-logging.txtar]()
* [testdata/scripts/node/validate/invalid.txtar]()
* [testdata/scripts/node/validate/valid.txtar]()

This document covers the configuration of blockchain networks and protocol-specific plugins within the Chainlink node. It details how to configure EVM and non-EVM chains, set up multiple blockchain connections, and manage chain-specific settings for various Chainlink services.

For general node configuration settings and feature flags, see [Node Configuration](). For job-specific configuration, see [Job System]().

## Configuration Architecture

The Chainlink node uses a hierarchical TOML configuration system where blockchain networks are defined as top-level array sections. Each chain configuration contains network-specific settings, node connection details, and service configurations.

**Chain Configuration Flow**

Sources: [docs/CONFIG.md1-20]() [core/services/chainlink/testdata/config-multi-chain.toml1-50]()

## EVM Chain Configuration

EVM chains are configured using `[[EVM]]` array sections in the TOML configuration. Each EVM chain requires a unique `ChainID` and at least one node connection.

### Basic EVM Chain Setup

### EVM Configuration Hierarchy

Sources: [docs/CONFIG.md4-107]() [core/config/docs/chains-evm.toml1-135]()

### EVM Gas Estimation Configuration

The gas estimator is crucial for EVM chains and supports multiple modes and fine-tuning options:

| Setting | Description | Default |
| --- | --- | --- |
| `Mode` | Gas estimation strategy: `BlockHistory`, `FixedPrice`, `SuggestedPrice` | `BlockHistory` |
| `PriceDefault` | Default gas price when estimation fails | `20 gwei` |
| `PriceMax` | Maximum allowed gas price | Chain-specific |
| `LimitDefault` | Default gas limit for transactions | `500000` |
| `EIP1559DynamicFees` | Enable EIP-1559 fee estimation | `true` |

Sources: [docs/CONFIG.md370-424]() [core/config/docs/chains-evm.toml135-200]()

### EVM Transaction Management

Transaction management settings control how the node handles transaction submission and confirmation:

**Transaction Manager Components**

Sources: [docs/CONFIG.md352-377]() [core/config/docs/chains-evm.toml108-133]()

## Non-EVM Chain Configuration

### Solana Chain Configuration

Solana chains use the `[[Solana]]` configuration section with blockchain-specific parameters:

### Solana-Specific Settings

| Setting | Purpose | Default |
| --- | --- | --- |
| `BlockTime` | Expected block production time | `500ms` |
| `Commitment` | Transaction commitment level | `confirmed` |
| `ComputeUnitPriceDefault` | Default compute unit price | `0` |
| `SkipPreflight` | Skip preflight transaction checks | `true` |
| `MaxRetries` | Maximum transaction retry attempts | `0` |

Sources: [docs/CONFIG.md662-687]() [core/services/chainlink/testdata/config-multi-chain.toml154-214]()

## Multi-Chain Node Configuration

The Chainlink node supports multiple chains simultaneously, each with independent configurations and node pools.

### Multi-Chain Setup Example

**Multi-Chain Architecture**

Sources: [core/services/chainlink/testdata/config-multi-chain.toml108-216]()

## Service-Specific Chain Configuration

Different Chainlink services require specific chain-level configurations.

### OCR and OCR2 Configuration

Off-Chain Reporting protocols have chain-specific settings:

### Workflow and Automation Configuration

Workflow engine and automation services have chain-specific gas and execution settings:

**Service Configuration Mapping**

Sources: [docs/CONFIG.md419-433]() [docs/CONFIG.md477-483]()

## Node Pool and Connection Management

Each chain maintains a pool of RPC node connections with failover and load balancing capabilities.

### Node Pool Configuration

### Node Connection Types

| Node Type | Purpose | Configuration |
| --- | --- | --- |
| Primary | Full read/write operations | `WSURL` + `HTTPURL` |
| Backup | Failover node | `HTTPURL` only |
| Send-Only | Transaction broadcasting | `SendOnly = true` |

Sources: [docs/CONFIG.md406-450]() [core/config/docs/chains-evm.toml220-280]()

## Configuration Validation and Defaults

The Chainlink node provides configuration validation and applies chain-specific defaults based on the `ChainID`.

### Validation Process

The `chainlink node validate` command provides comprehensive configuration checking and displays the effective configuration with all defaults applied.

Sources: [testdata/scripts/node/validate/valid.txtar1-50]() [core/services/chainlink/config\_test.go219-266]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Chain and Plugin Configuration]()
* [Configuration Architecture]()
* [EVM Chain Configuration]()
* [Basic EVM Chain Setup]()
* [EVM Configuration Hierarchy]()
* [EVM Gas Estimation Configuration]()
* [EVM Transaction Management]()
* [Non-EVM Chain Configuration]()
* [Solana Chain Configuration]()
* [Solana-Specific Settings]()
* [Multi-Chain Node Configuration]()
* [Multi-Chain Setup Example]()
* [Service-Specific Chain Configuration]()
* [OCR and OCR2 Configuration]()
* [Workflow and Automation Configuration]()
* [Node Pool and Connection Management]()
* [Node Pool Configuration]()
* [Node Connection Types]()
* [Configuration Validation and Defaults]()
* [Validation Process]()