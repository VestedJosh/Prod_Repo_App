## Development Environment Requirements

The LVLidoVault system is built using the Foundry development framework and requires specific toolchain components for compilation, testing, and deployment.

### Required Software

| Component | Version | Purpose |
| --- | --- | --- |
| Foundry | nightly | Smart contract development framework |
| Git | Latest | Version control and submodule management |
| Node.js | 16+ | For any auxiliary scripts |

### Foundry Installation

Install Foundry using the official installer:

Verify the installation:

**Development Environment Setup Flow**

Sources: [.github/workflows/test.yml18-27]() [.gitmodules1-16]()

## Dependencies Overview

The LVLidoVault system relies on several external libraries and protocols integrated as Git submodules. Each dependency serves specific functionality within the system.

### Core Dependencies

| Dependency | Purpose | Repository |
| --- | --- | --- |
| `forge-std` | Foundry testing utilities | foundry-rs/forge-std |
| `openzeppelin-contracts` | Standard contract implementations | OpenZeppelin/openzeppelin-contracts |
| `prb-math` | Fixed-point mathematical operations | PaulRBerg/prb-math |
| `chainlink` | Oracle and automation contracts | smartcontractkit/chainlink |
| `balancer-v2-monorepo` | Flash loan functionality | balancer/balancer-v2-monorepo |

**Dependency Integration Architecture**

Sources: [.gitmodules1-16]()

## Installation Process

### Repository Setup

1. **Clone the repository with submodules:**

2. **If already cloned, initialize submodules:**

3. **Verify submodule installation:**

### Build Verification

The system uses specific Foundry configuration optimized for the complex contract interactions:

This command compiles all contracts and displays their sizes, helping identify potential deployment gas limits.

Sources: [.github/workflows/test.yml38-40]()

## Configuration

### Foundry Configuration

The `foundry.toml` file contains optimized settings for the LVLidoVault system:

| Setting | Value | Purpose |
| --- | --- | --- |
| `src` | "src" | Source code directory |
| `out` | "out" | Build output directory |
| `libs` | ["lib"] | Dependencies directory |
| `viaIR` | true | Enables IR-based compilation for complex contracts |
| `optimizer` | true | Enables Solidity optimizer |
| `optimizer_runs` | 200 | Optimization for deployment cost vs runtime cost |
| `incremental` | true | Speeds up subsequent builds |

### Environment Variables

For deployment and testing, the following environment variables should be configured:

| Variable | Purpose | Example |
| --- | --- | --- |
| `ETHERSCAN_API_KEY` | Contract verification | `abc123...` |
| `PRIVATE_KEY` | Deployment account | `0x123...` |
| `RPC_URL` | Ethereum node endpoint | `https://eth-mainnet.alchemyapi.io/v2/...` |

**Configuration Validation Flow**

Sources: [foundry.toml1-10]()

## Verification

### Build Verification

Verify the environment is correctly configured:

### Expected Output

A successful setup should produce:

* Clean formatting check (no changes needed)
* Successful compilation of all contracts
* All tests passing with detailed verbose output
* Contract size information showing deployability

### Common Issues

| Issue | Cause | Solution |
| --- | --- | --- |
| Submodule errors | Incomplete submodule initialization | Run `git submodule update --init --recursive` |
| Compilation failures | Missing dependencies | Verify all lib/ directories exist |
| Test failures | Environment variables | Set required environment variables |
| IR compilation errors | Complex contract interactions | Verify `viaIR = true` in foundry.toml |

Sources: [.github/workflows/test.yml32-45]() [foundry.toml5-8]()

The development environment is now ready for core contract deployment. Proceed to [Core Contract Deployment]() to begin the deployment process.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Prerequisites and Setup]()
* [Development Environment Requirements]()
* [Required Software]()
* [Foundry Installation]()
* [Dependencies Overview]()
* [Core Dependencies]()
* [Installation Process]()
* [Repository Setup]()
* [Build Verification]()
* [Configuration]()
* [Foundry Configuration]()
* [Environment Variables]()
* [Verification]()
* [Build Verification]()
* [Expected Output]()
* [Common Issues]()