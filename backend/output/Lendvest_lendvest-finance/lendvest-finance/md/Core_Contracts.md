## Contract Architecture Overview

The LVLidoVault system is built around three core contracts that work together to provide leveraged lending functionality with automated risk management.

### Core Contract Hierarchy

**Sources:** [src/LVLidoVault.sol1-83]() [src/LVLidoVaultUtil.sol1-52]() [script/postDeployment2.s.sol1-21]()

### Contract Relationships and Communication

**Sources:** [src/LVLidoVault.sol440-490]() [src/LVLidoVaultUtil.sol79-177]() [src/LVLidoVault.sol1084-1095]()

## LVLidoVault Contract

The `LVLidoVault` contract serves as the primary coordination point for all vault operations, managing user orders, epoch lifecycle, and external protocol interactions.

### Key State Variables

| Variable | Type | Purpose |
| --- | --- | --- |
| `pool` | `IERC20Pool` | Ajna lending pool interface |
| `liquidationProxy` | `ILiquidationProxy` | Liquidation management contract |
| `LVLidoVaultUtil` | `address` | Automation contract address |
| `totalBorrowAmount` | `uint256` | Total amount borrowed from Ajna |
| `epochStarted` | `bool` | Current epoch state flag |
| `currentBucketIndex` | `uint256` | Ajna pool bucket for operations |

**Sources:** [src/LVLidoVault.sol22-69]()

### Order Management System

**Sources:** [src/LVLidoVault.sol60-62]() [src/LVLidoVault.sol873-941]() [src/LVLidoVault.sol950-1068]() [src/LVLidoVault.sol222-432]()

### Flash Loan Integration

The vault implements Balancer's `IFlashLoanRecipient` interface to enable leveraged borrowing:

**Sources:** [src/LVLidoVault.sol169-213]() [src/LVLidoVault.sol428-432]()

### Epoch Lifecycle Management

| Function | Purpose | Access Control |
| --- | --- | --- |
| `startEpoch()` | Initiates new epoch, matches orders | Public with conditions |
| `tryMatchOrders()` | Internal order matching logic | Internal |
| `end_epoch()` | Resets epoch state | `onlyProxy` |

**Sources:** [src/LVLidoVault.sol440-490]() [src/LVLidoVault.sol222-432]() [src/LVLidoVault.sol630-636]()

## LVLidoVaultUtil Contract

The `LVLidoVaultUtil` contract provides automated risk management and oracle functionality through Chainlink integration.

### Automation Interface Implementation

**Sources:** [src/LVLidoVaultUtil.sol79-177]() [src/LVLidoVaultUtil.sol179-438]()

### Risk Management Parameters

| Parameter | Value | Purpose |
| --- | --- | --- |
| `FACTOR_COLLATERAL_INCREASE` | `11e15` (1.1%) | Tranche trigger threshold |
| `MAX_TRANCHES` | `3` | Maximum collateral tranches |
| `priceDifferencethreshold` | `-1e16` (-1%) | Initial liquidation threshold |

**Sources:** [src/LVLidoVaultUtil.sol31-33]() [src/LVLidoVault.sol55]()

### Chainlink Functions Integration

**Sources:** [src/LVLidoVaultUtil.sol472-486]() [src/LVLidoVaultUtil.sol495-533]() [src/LVLidoVaultUtil.sol460-465]()

## Contract Integration Patterns

### Access Control Architecture

The contracts implement a multi-tier access control system:

**Sources:** [src/LVLidoVault.sol95-107]() [src/LVLidoVault.sol689-692]() [src/LVLidoVaultUtil.sol54-59]()

### Token Management Interface

| Contract | Token Operations | Purpose |
| --- | --- | --- |
| `LVLidoVault` | `mintForProxy()`, `burnForProxy()` | Test token lifecycle |
| `LVLidoVault` | `approveForProxy()`, `transferForProxy()` | Proxy token operations |
| `LVLidoVault` | `wethToWsteth()` | WETH → wstETH conversion |

**Sources:** [src/LVLidoVault.sol786-807]() [src/LVLidoVault.sol571-584]() [src/LVLidoVault.sol132-154]()

### External Protocol Interfaces

The core contracts maintain connections to external protocols through well-defined interfaces:

**Sources:** [src/LVLidoVault.sol25-31]() [src/LVLidoVaultUtil.sol22-26]() [src/LVLidoVaultUtil.sol48-52]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Core Contracts]()
* [Contract Architecture Overview]()
* [Core Contract Hierarchy]()
* [Contract Relationships and Communication]()
* [LVLidoVault Contract]()
* [Key State Variables]()
* [Order Management System]()
* [Flash Loan Integration]()
* [Epoch Lifecycle Management]()
* [LVLidoVaultUtil Contract]()
* [Automation Interface Implementation]()
* [Risk Management Parameters]()
* [Chainlink Functions Integration]()
* [Contract Integration Patterns]()
* [Access Control Architecture]()
* [Token Management Interface]()
* [External Protocol Interfaces]()