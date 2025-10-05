
The Chainlink configuration system uses two primary TOML files:

* **Main Configuration File** (`config.toml`): Contains operational settings, chain configurations, and feature flags
* **Secrets Configuration File** (`secrets.toml`): Contains sensitive data like database URLs and keystores

Sources: [docs/CONFIG.md1-20]() [core/services/chainlink/config\_test.go42-217]()

Configuration Structure and Hierarchy
-------------------------------------

The configuration system follows a hierarchical structure with global settings at the root level and specialized sections for different subsystems:

### Global Configuration Sections

| Section | Purpose | Key Settings |
| --- | --- | --- |
| `[Feature]` | Enable/disable node features | `FeedsManager`, `LogPoller`, `CCIP` |
| `[Database]` | Database connection and behavior | Connection pools, timeouts, migrations |
| `[Log]` | Logging configuration | Log levels, file rotation, JSON formatting |
| `[WebServer]` | HTTP API and UI settings | Ports, authentication, rate limiting |
| `[JobPipeline]` | Job execution parameters | Timeouts, queue depths, HTTP settings |

### Chain-Specific Configuration

Each blockchain network requires its own configuration section:

Sources: [docs/CONFIG.md96-106]() [core/services/chainlink/testdata/config-multi-chain.toml328-661]()

Configuration Processing Flow
-----------------------------

Sources: [core/services/chainlink/config\_test.go219-266]() [testdata/scripts/node/validate/valid.txtar1-52]()

Key Configuration Categories
----------------------------

### Feature Flags

The `[Feature]` section controls which services and capabilities are enabled:

### Database Configuration

Database settings control connection behavior and operational parameters:

### Web Server Configuration

Controls the HTTP API server and authentication:

Sources: [docs/CONFIG.md56-106]() [docs/CONFIG.md467-722]()

Chain Configuration Management
------------------------------

### EVM Chain Configuration

EVM chains require extensive configuration for gas estimation, transaction management, and node connectivity:

### Multi-Chain Configuration Example

Sources: [core/config/docs/chains-evm.toml1-106]() [core/services/chainlink/testdata/config-multi-chain-effective.toml328-661]()

Configuration Validation
------------------------

The configuration validation process ensures all settings are valid and compatible:

The validation process checks:

* Required fields are present (database URL, chain configurations)
* Numeric values are within acceptable ranges
* URL formats are valid
* Chain-specific constraints are met
* Cross-field dependencies are satisfied

Sources: [core/services/chainlink/config\_test.go219-840]() [testdata/scripts/node/validate/invalid.txtar1-24]()

Secrets Management
------------------

Sensitive configuration data is separated into a dedicated secrets file:

The secrets are masked in configuration output for security:

Sources: [testdata/scripts/node/validate/valid.txtar25-40]() [docs/CONFIG.md4-5]()

Configuration CLI Commands
--------------------------

The Chainlink CLI provides configuration validation and inspection capabilities:

The validation output includes three sections:

1. **Secrets**: Masked sensitive configuration
2. **Input Configuration**: User-provided settings
3. **Effective Configuration**: Complete configuration with defaults applied

Sources: [testdata/scripts/node/validate/valid.txtar1-13]() [testdata/scripts/node/validate/disk-based-logging.txtar1-8]()