## System Overview

The LVLidoVault architecture consists of three main contract layers: the core vault logic, automation utilities, and external protocol integrations. The system operates on an epoch-based model where users submit orders that are matched and executed through leveraged borrowing mechanisms.

### Core System Components

Sources: [src/LVLidoVault.sol21-32]() [src/LVLidoVaultUtil.sol19-26]() [test/Main.t.sol30-37]()

### Contract Relationships and Access Control

The system implements a strict access control pattern where the main `LVLidoVault` contract serves as the central authority, with utility contracts acting as authorized proxies.

Sources: [src/LVLidoVault.sol102-107]() [src/LVLidoVaultUtil.sol54-59]() [src/LVLidoVault.sol689-692]()

## Epoch-Based Operational Flow

The system operates through discrete epochs where user orders are collected, matched, and executed. Each epoch follows a deterministic lifecycle managed through Chainlink automation.

### Epoch Lifecycle State Machine

Sources: [src/LVLidoVault.sol440-490]() [src/LVLidoVaultUtil.sol179-436]()

### Order Matching and Flash Loan Architecture

The core financial logic revolves around matching lender and borrower orders while utilizing flash loans to provide leverage.

Sources: [src/LVLidoVault.sol222-432]() [src/LVLidoVault.sol169-213]() [src/LVLidoVault.sol132-154]()

## Token Architecture and Flash Loan Integration

The system uses a dual-token approach with internal `LVToken` wrappers for Ajna pool compatibility and direct integration with underlying tokens for external protocols.

### Token Flow and Conversion Mechanisms

Sources: [src/LVLidoVault.sol132-154]() [src/LVLidoVault.sol78-80]() [src/LVLidoVault.sol184-190]()

## Chainlink Automation Integration

The system relies heavily on Chainlink services for automated operations, price monitoring, and off-chain data integration.

### Automation Task Architecture

Sources: [src/LVLidoVaultUtil.sol79-177]() [src/LVLidoVaultUtil.sol179-437]() [src/LVLidoVaultUtil.sol472-533]()

### Risk Management and Liquidation Prevention

The system implements a multi-tiered risk management approach using collateral lender funds to prevent liquidations through automated price monitoring.

Sources: [src/LVLidoVaultUtil.sol28-33]() [src/LVLidoVaultUtil.sol68-77]() [src/LVLidoVaultUtil.sol104-139]() [src/LVLidoVault.sol665-682]()

## Data Structures and State Management

The vault maintains complex state through structured data types that track user positions, epoch information, and system parameters.

### Core Data Structures

| Structure | Purpose | Key Fields | Storage Location |
| --- | --- | --- | --- |
| `LenderOrder` | Lender deposit tracking | `lender`, `quoteAmount`, `vaultShares` | `lenderOrders[]` |
| `BorrowerOrder` | Borrower collateral tracking | `borrower`, `collateralAmount` | `borrowerOrders[]` |
| `CollateralLenderOrder` | CL deposit tracking | `collateralLender`, `collateralAmount` | `collateralLenderOrders[]` |
| `MatchInfo` | Epoch loan matching | `lender`, `borrower`, `quoteAmount`, `collateralAmount` | `epochToMatches[epoch][]` |

### State Variables and Accounting

The system tracks multiple accounting variables to maintain accurate fund distribution and risk management:

| Variable | Purpose | Updated By |
| --- | --- | --- |
| `totalLenderQTUtilized` | Active lender funds in Ajna | `tryMatchOrders()` |
| `totalLenderQTUnutilized` | Idle lender funds | `createLenderOrder()`, `startEpoch()` |
| `totalBorrowerCT` | Total borrower collateral | `createBorrowerOrder()` |
| `totalCollateralLenderCT` | Available CL collateral | `createCLOrder()` |
| `totalCLDepositsUtilized` | Active CL collateral | `avoidLiquidation()` |
| `collateralLenderTraunche` | Current risk tranche | `setCollateralLenderTraunche()` |
| `epochStartRedemptionRate` | Starting wstETH rate | `startEpoch()` |
| `currentRedemptionRate` | Current wstETH rate | `setCurrentRedemptionRate()` |

Sources: [src/LVLidoVault.sol34-58]() [src/LVLidoVault.sol60-65]() [src/libraries/VaultLib.sol]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Architecture]()
* [System Overview]()
* [Core System Components]()
* [Contract Relationships and Access Control]()
* [Epoch-Based Operational Flow]()
* [Epoch Lifecycle State Machine]()
* [Order Matching and Flash Loan Architecture]()
* [Token Architecture and Flash Loan Integration]()
* [Token Flow and Conversion Mechanisms]()
* [Chainlink Automation Integration]()
* [Automation Task Architecture]()
* [Risk Management and Liquidation Prevention]()
* [Data Structures and State Management]()
* [Core Data Structures]()
* [State Variables and Accounting]()