For information about the core vault contracts and their relationships, see [Core Contracts](). For details on risk management mechanisms, see [Risk Management]().

## Architecture Overview

The automation system is built around the `LVLidoVaultUtil` contract, which serves as the central coordinator for automated vault operations. It integrates with Chainlink's decentralized automation network to execute time-sensitive and condition-based tasks.

### Core Automation Components

**Sources:** [src/LVLidoVaultUtil.sol1-535]() [src/UpkeepAdmin.sol1-64]()

The `LVLidoVaultUtil` contract implements two key Chainlink interfaces:

* `AutomationCompatibleInterface` for scheduled and conditional task execution
* `FunctionsClient` for fetching external data and computing interest rates

### Task-Based Automation Framework

The automation system operates through a task-based framework where different `taskId` values trigger specific operations:

| Task ID | Purpose | Trigger Condition |
| --- | --- | --- |
| 0 | Add Collateral (Avoid Liquidation) | Price drop exceeds tranche threshold |
| 1 | Queue Withdrawals | Term duration complete, debt exists |
| 2 | Settle Epoch | ETH claimable or auction completed |
| 3 | Allow Liquidation | All collateral tranches exhausted |
| 221 | Fetch Interest Rate | Term complete, rate update needed |

**Sources:** [src/LVLidoVaultUtil.sol79-177]() [src/LVLidoVaultUtil.sol179-438]()

## Chainlink Integration Architecture

### Automation Service Integration

The `checkUpkeep` function continuously monitors vault conditions and determines when automated actions are required:

**Sources:** [src/LVLidoVaultUtil.sol79-177]() [src/LVLidoVaultUtil.sol179-438]()

### Functions Service Integration

The system uses Chainlink Functions to fetch interest rate data from external sources:

The `fulfillRequest` function processes responses containing aggregated rate data:

**Sources:** [src/LVLidoVaultUtil.sol472-486]() [src/LVLidoVaultUtil.sol495-533]()

## Automated Risk Management

### Collateral Tranche System

The automation system implements a three-tranche collateral management system to prevent liquidations:

**Sources:** [src/LVLidoVaultUtil.sol28-33]() [src/LVLidoVaultUtil.sol104-140]()

The system uses the `FACTOR_COLLATERAL_INCREASE` constant (1.1%) and `MAX_TRANCHES` (3) to calculate threshold points:

* Tranche 1: -1.1% price movement
* Tranche 2: -2.2% cumulative price movement
* Tranche 3: -3.3% cumulative price movement

### Price Monitoring Implementation

Price monitoring compares the current wstETH redemption rate against the rate stored at epoch start:

**Sources:** [src/LVLidoVaultUtil.sol68-77]() [src/LVLidoVaultUtil.sol91-99]()

## Epoch Lifecycle Automation

### Term Completion Handling

The automation system manages the complex process of settling completed epochs:

**Sources:** [src/LVLidoVaultUtil.sol242-261]() [src/LVLidoVaultUtil.sol263-436]()

### Settlement Process Detail

The settlement process (Task 2) handles complex calculations for profit/loss distribution:

**Sources:** [src/LVLidoVaultUtil.sol298-436]()

Key settlement operations include:

* Calculating actual debt based on elapsed time and interest rate
* Processing Lido ETH claims and converting to WETH
* Distributing profits/losses among lenders, borrowers, and collateral lenders
* Cleaning up Ajna pool positions and burning vault tokens
* Preparing new orders for the next epoch

## Configuration and Management

### Upkeep Administration

The `UpkeepAdmin` contract provides administrative functions for managing Chainlink upkeep tasks:

**Sources:** [src/UpkeepAdmin.sol39-63]() [script/postDeployment5.s.sol7-18]()

### Functions Configuration

The `LVLidoVaultUtil` contract includes configuration methods for Chainlink Functions:

* `setForwarderAddress()`: Sets the authorized forwarder for meta-transactions
* `setRequest()`: Configures the CBOR-encoded Functions request parameters

**Sources:** [src/LVLidoVaultUtil.sol446-465]()

### Constants and Parameters

Key configuration constants defined in the system:

| Constant | Value | Purpose |
| --- | --- | --- |
| `FACTOR_COLLATERAL_INCREASE` | 11e15 (1.1%) | Tranche threshold increment |
| `MAX_TRANCHES` | 3 | Maximum collateral tranches |
| `lidoClaimDelay` | 10 days | Lido withdrawal processing time |
| `PRICE_FEED_DECIMALS` | 8 | Chainlink price feed precision |

**Sources:** [src/LVLidoVaultUtil.sol28-35]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Automation System]()
* [Purpose and Scope]()
* [Architecture Overview]()
* [Core Automation Components]()
* [Task-Based Automation Framework]()
* [Chainlink Integration Architecture]()
* [Automation Service Integration]()
* [Functions Service Integration]()
* [Automated Risk Management]()
* [Collateral Tranche System]()
* [Price Monitoring Implementation]()
* [Epoch Lifecycle Automation]()
* [Term Completion Handling]()
* [Settlement Process Detail]()
* [Configuration and Management]()
* [Upkeep Administration]()
* [Functions Configuration]()
* [Constants and Parameters]()