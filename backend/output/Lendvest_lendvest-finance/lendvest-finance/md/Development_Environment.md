## Prerequisites

The LVLidoVault project uses Foundry as its primary development framework. The following tools must be installed before setting up the project:

### Required Tools

| Tool | Purpose | Installation |
| --- | --- | --- |
| Foundry | Solidity development framework | `curl -L https://foundry.paradigm.xyz | bash && foundryup` |
| Git | Version control and submodule management | System package manager or official installer |
| Node.js | JavaScript runtime for tooling | `nvm install node` or official installer |

### Foundry Components

The project utilizes several Foundry tools:

**Sources:** [foundry.toml1-10]()

## Repository Setup

### Clone Repository

### Initialize Submodules

The project uses several external libraries as Git submodules. Initialize them with:

### Dependency Architecture

The project's dependency structure is defined in the submodule configuration:

**Sources:** [.gitmodules1-16]()

## Project Configuration

### Foundry Configuration

The project's build settings are configured in `foundry.toml`:

**Key Configuration Details:**

| Setting | Value | Purpose |
| --- | --- | --- |
| `viaIR` | `true` | Enables IR-based compilation for complex contracts |
| `optimizer` | `true` | Optimizes bytecode for gas efficiency |
| `optimizer_runs` | `200` | Balances deployment vs runtime gas costs |
| `incremental` | `true` | Enables incremental compilation for faster builds |

**Sources:** [foundry.toml1-10]()

### Environment Variables

The project expects certain environment variables for testing and deployment. Create a `.env` file based on your requirements:

**Sources:** [.gitignore15]()

## Build Verification

### Compile Contracts

Verify the development environment by compiling all contracts:

Expected output structure:

**Sources:** [foundry.toml2-3]() [.gitignore2-3]()

### Verify Dependencies

Confirm all submodules are correctly initialized:

### Test Basic Functionality

Run a quick test to verify the environment:

## Development Workflow

### File Structure Overview

The development environment organizes files according to Foundry conventions:

### Ignored Files

The development environment excludes certain files from version control:

| Pattern | Purpose |
| --- | --- |
| `cache/` | Compilation cache files |
| `out/` | Build artifacts and bytecode |
| `/broadcast/*/31337/` | Local Anvil deployment logs |
| `/broadcast/**/dry-run/` | Deployment dry-run artifacts |
| `.env` | Environment variables and secrets |

**Sources:** [.gitignore1-16]()

## Troubleshooting

### Common Issues

1. **Submodule Initialization Failures**
2. **Compilation Errors with IR**

   * The `viaIR` setting may cause issues with certain contract sizes
   * Consider temporarily disabling in `foundry.toml` if needed
3. **Optimizer Issues**

   * If deployment gas estimation fails, adjust `optimizer_runs` value
   * Lower values optimize for deployment, higher values for runtime

**Sources:** [foundry.toml5-7]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Development Environment]()
* [Prerequisites]()
* [Required Tools]()
* [Foundry Components]()
* [Repository Setup]()
* [Clone Repository]()
* [Initialize Submodules]()
* [Dependency Architecture]()
* [Project Configuration]()
* [Foundry Configuration]()
* [Environment Variables]()
* [Build Verification]()
* [Compile Contracts]()
* [Verify Dependencies]()
* [Test Basic Functionality]()
* [Development Workflow]()
* [File Structure Overview]()
* [Ignored Files]()
* [Troubleshooting]()
* [Common Issues]()