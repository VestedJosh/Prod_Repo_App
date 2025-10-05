* [core/web/resolver/testdata/config-multi-chain-effective.toml]()
* [docs/CONFIG.md]()
* [testdata/scripts/node/validate/default.txtar]()
* [testdata/scripts/node/validate/disk-based-logging-disabled.txtar]()
* [testdata/scripts/node/validate/disk-based-logging-no-dir.txtar]()
* [testdata/scripts/node/validate/disk-based-logging.txtar]()
* [testdata/scripts/node/validate/invalid.txtar]()
* [testdata/scripts/node/validate/valid.txtar]()

This document provides detailed documentation of TOML configuration options, feature flags, and core node settings for the Chainlink node. It covers the structure and format of configuration files, global node settings, feature toggles, and service-specific configurations that control node behavior.

For information about chain-specific configuration (EVM, Solana, etc.) and plugin settings, see [Chain and Plugin Configuration]().

## Configuration File Structure

Chainlink nodes use TOML format for configuration, with a hierarchical structure that separates global settings, feature flags, and service-specific configurations. The configuration system supports both a main configuration file and a separate secrets file for sensitive data.

The configuration system validates all settings during node startup and provides detailed error messages for invalid configurations. The `chainlink node validate` command can be used to validate configuration without starting the node.

**Sources:** [docs/CONFIG.md1-20]() [core/services/chainlink/config\_test.go52-216]() [testdata/scripts/node/validate/valid.txtar1-15]()

## Global Node Settings

Global settings control fundamental node behavior and are defined at the top level of the configuration file.

| Setting | Default | Description |
| --- | --- | --- |
| `RootDir` | `'~/.chainlink'` | Root directory for node data, logs, and temporary files |
| `ShutdownGracePeriod` | `'5s'` | Maximum time allowed for graceful shutdown |
| `InsecureFastScrypt` | `false` | Use fast scrypt for development (DO NOT use in production) |
| `InsecurePPROFHeap` | `false` | Enable heap dumps in pprof (may expose sensitive data) |

The `RootDir` setting is particularly important as it determines where the node stores its database backups, log files, and other persistent data. The directory permissions are automatically set to 700 to protect sensitive data.

**Sources:** [docs/CONFIG.md44-54]() [docs/CONFIG.md22-40]()

## Feature Flags

Feature flags enable or disable major node functionality and are grouped under the `[Feature]` section.

### Core Feature Flags

* **`FeedsManager`**: Enables the feeds manager service for handling job proposals and configurations
* **`LogPoller`**: Enables experimental log polling approach (required for certain job types)
* **`UICSAKeys`**: Shows CSA keys in the web UI
* **`CCIP`**: Enables Cross-Chain Interoperability Protocol services
* **`MultiFeedsManagers`**: Allows connections to multiple feeds managers

**Sources:** [docs/CONFIG.md56-95]()

## Database Configuration

Database settings control PostgreSQL connection behavior, performance tuning, and backup configurations.

### Key Database Settings

| Setting | Default | Description |
| --- | --- | --- |
| `MaxOpenConns` | `100` | Maximum database connections |
| `MaxIdleConns` | `10` | Baseline idle connections |
| `DefaultQueryTimeout` | `'10s'` | Standard query timeout |
| `MigrateOnStartup` | `true` | Auto-run migrations on startup |

### Backup Configuration

The database backup system supports three modes:

* **`none`**: No automatic backups
* **`lite`**: Essential tables only (keys, configuration)
* **`full`**: Complete database dump

**Sources:** [docs/CONFIG.md97-197]()

## Web Server and API Configuration

The web server configuration controls the HTTP API, authentication, and security settings for the node's web interface.

### Core Web Server Settings

### LDAP Integration

For enterprise deployments, LDAP authentication can be configured:

**Sources:** [docs/CONFIG.md467-743]()

## Logging Configuration

Logging configuration controls both console output and file-based logging with rotation.

### Log Level Configuration

Log levels determine verbosity:

* **`debug`**: Detailed debugging information
* **`info`**: General operational messages (default)
* **`warn`**: Warning conditions that may need attention
* **`error`**: Error conditions requiring action
* **`crit`**: Critical errors that may affect node operation

**Sources:** [docs/CONFIG.md387-465]()

## Job Pipeline Configuration

The job pipeline system executes and manages job runs across different job types.

### Key Pipeline Settings

| Setting | Default | Description |
| --- | --- | --- |
| `MaxRunDuration` | `'10m'` | Maximum execution time per job run |
| `MaxSuccessfulRuns` | `10000` | Maximum successful runs to keep in database |
| `ReaperInterval` | `'1h'` | How often to clean up old job runs |
| `ExternalInitiatorsEnabled` | `false` | Allow external webhook job triggers |

**Sources:** [docs/CONFIG.md792-857]()

## Monitoring and Telemetry

The node supports comprehensive monitoring through telemetry ingress, metrics collection, and external monitoring services.

### Telemetry Configuration

### Auto-Profiling

**Sources:** [docs/CONFIG.md264-351]() [docs/CONFIG.md537-560]()

## Configuration Validation

The Chainlink node provides comprehensive configuration validation through the `chainlink node validate` command. This validation process checks configuration syntax, validates settings against constraints, and reports detailed error messages.

The validation command outputs three sections:

1. **Secrets**: Sensitive configuration with values masked
2. **Input Configuration**: User-provided configuration
3. **Effective Configuration**: Complete configuration with defaults applied

Example validation command:

**Sources:** [testdata/scripts/node/validate/valid.txtar1-15]() [testdata/scripts/node/validate/invalid.txtar1-5]() [core/services/chainlink/config\_test.go219-266]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Node Configuration]()
* [Configuration File Structure]()
* [Global Node Settings]()
* [Feature Flags]()
* [Core Feature Flags]()
* [Database Configuration]()
* [Key Database Settings]()
* [Backup Configuration]()
* [Web Server and API Configuration]()
* [Core Web Server Settings]()
* [LDAP Integration]()
* [Logging Configuration]()
* [Log Level Configuration]()
* [Job Pipeline Configuration]()
* [Key Pipeline Settings]()
* [Monitoring and Telemetry]()
* [Telemetry Configuration]()
* [Auto-Profiling]()
* [Configuration Validation]()