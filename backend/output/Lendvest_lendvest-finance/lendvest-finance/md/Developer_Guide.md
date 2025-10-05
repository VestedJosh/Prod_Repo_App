## Development Environment Architecture

The LVLidoVault system is built using Foundry as the primary development framework, with Solidity smart contracts deployed on Ethereum mainnet. The development environment integrates with multiple external DeFi protocols and requires specific tooling for testing and deployment.

### Development Stack Overview

**Sources:** [foundry.toml1-10]() [.github/workflows/test.yml1-46]() [test/Main.t.sol1-25]()

## Core Contract Development Structure

The system follows a modular architecture where each contract has specific responsibilities. Understanding these relationships is crucial for development work.

### Contract Interaction Map

**Sources:** [test/Main.t.sol30-42]() [test/Main.t.sol68-82]()

## Test Framework Architecture

The testing framework uses Foundry's forge with mainnet forking to test against real protocol states. The main test contract demonstrates the complete system lifecycle.

### Test Structure

| Component | Purpose | Key Features |
| --- | --- | --- |
| `LogicTests` | Main test contract | Inherits from `Test` and `TestHelpers` |
| `TestHelpers` | Utility functions | Provides common test setup and helpers |
| Mainnet Forking | Real protocol state | Tests against actual Ajna, Lido, Chainlink |
| `vm.prank()` | Address impersonation | Simulates different user interactions |
| `deal()` | Token allocation | Provides test tokens to addresses |

The test setup process in `setUp()` demonstrates the complete deployment flow:

1. **Token Deployment**: Creates `LVToken` instances for LVWETH and LVWSTETH
2. **Pool Creation**: Deploys Ajna pool via `IERC20PoolFactory.deployPool()`
3. **Contract Deployment**: Deploys vault, utility, and liquidation proxy contracts
4. **Ownership Transfer**: Transfers token and proxy ownership to vault
5. **Configuration**: Sets forwarder address for Chainlink automation

**Sources:** [test/Main.t.sol43-86]() [test/Main.t.sol25-41]()

## Key Development Patterns

### Ownership and Access Control

The system uses a specific ownership pattern where:

* `LVToken` contracts are owned by `LVLidoVault`
* `LiquidationProxy` is owned by `LVLidoVault`
* `LVLidoVaultUtil` has a dedicated `forwarder` address for Chainlink automation
* Final ownership is often renounced for security

**Sources:** [test/Main.t.sol73-82]()

### Automation Integration Pattern

The system integrates with Chainlink Automation using a specific pattern:

1. `LVLidoVaultUtil.checkUpkeep()` returns boolean and encoded task data
2. `LVLidoVaultUtil.performUpkeep()` decodes task ID and executes appropriate function
3. Task IDs map to specific automation functions (0=collateral, 1=withdrawal, etc.)

### Test User Simulation Pattern

Testing follows a consistent pattern for simulating different user types:

**Sources:** [test/Main.t.sol101-106]()

## Testing Scenarios

The test suite covers several critical scenarios:

| Test Scenario | Purpose | Key Components |
| --- | --- | --- |
| Manual Repayment Flow | Tests debt repayment after Lido delays | `repayAjnaDebt()`, Lido queue processing |
| Ideal Scenario | Tests profitable outcome for lenders/CL | Standard epoch lifecycle |
| Collateral Addition | Tests automated risk management | `avoidLiquidation()`, price drops |
| Liquidation Auction | Tests liquidation mechanics | `lenderKick()`, auction settlement |

### Automation Task Testing

The system defines specific task IDs for different automation functions:

* **Task 0**: Add collateral when price drops
* **Task 1**: Queue Lido withdrawals at term end
* **Task 2**: Settle epoch after claim delay
* **Task 3**: Enable liquidation (`allowKick`)
* **Task 221**: Fetch final interest rates

**Sources:** [test/Main.t.sol134-138]() [test/Main.t.sol457-460]() [test/Main.t.sol513-515]()

## Configuration and Build Settings

The development environment uses specific Foundry configurations optimized for the DeFi contract patterns:

| Setting | Value | Purpose |
| --- | --- | --- |
| `viaIR` | `true` | Enables intermediate representation for complex contracts |
| `optimizer` | `true` | Gas optimization enabled |
| `optimizer_runs` | `200` | Balanced optimization for deployment vs execution |
| `incremental` | `true` | Faster rebuilds during development |

**Sources:** [foundry.toml5-8]()

The CI pipeline runs comprehensive checks including formatting, building with size analysis, and verbose test execution to ensure code quality and catch integration issues early.

**Sources:** [.github/workflows/test.yml32-45]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Developer Guide]()
* [Development Environment Architecture]()
* [Development Stack Overview]()
* [Core Contract Development Structure]()
* [Contract Interaction Map]()
* [Test Framework Architecture]()
* [Test Structure]()
* [Key Development Patterns]()
* [Ownership and Access Control]()
* [Automation Integration Pattern]()
* [Test User Simulation Pattern]()
* [Testing Scenarios]()
* [Automation Task Testing]()
* [Configuration and Build Settings]()