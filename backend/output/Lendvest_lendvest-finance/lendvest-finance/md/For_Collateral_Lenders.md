## Overview

Collateral lenders serve as a crucial safety mechanism in the LVLidoVault system by providing additional wstETH collateral that can be automatically deployed to maintain healthy loan-to-value ratios during market downturns. When stETH/ETH prices drop, the system automatically uses collateral lender funds in three sequential tranches to prevent borrower liquidations.

**Collateral Lender Risk Management Flow**

Sources: [src/LVLidoVault.sol924-941]() [src/LVLidoVaultUtil.sol104-140]() [src/LVLidoVaultUtil.sol218-235]()

## Creating Collateral Lender Orders

### Deposit Process

Collateral lenders deposit wstETH tokens using the `createCLOrder()` function:

| Step | Function | Description |
| --- | --- | --- |
| 1 | Approve wstETH | `IERC20(wstETH).approve(vault, amount)` |
| 2 | Create Order | `vault.createCLOrder(amount)` |
| 3 | Wait for Epoch | Order remains in pool until needed |

The system enforces a maximum fund limit via the `maxFundsLimiter()` function, which caps total vault value at $10,000 USD equivalent across all deposited assets.

Sources: [src/LVLidoVault.sol924-941]() [src/LVLidoVault.sol109-119]()

### State Tracking

The system tracks collateral lender deposits through several state variables:

* `totalCollateralLenderCT`: Total collateral lender deposits not yet matched to epochs
* `totalCLDepositsUnutilized`: Collateral lender funds available for risk mitigation
* `totalCLDepositsUtilized`: Collateral lender funds currently deployed in Ajna pool
* `collateralLenderTraunche`: Current tranche level (0-3)

Sources: [src/LVLidoVault.sol40-46]()

## Risk Mitigation System

### Automated Tranche Deployment

The `LVLidoVaultUtil` contract monitors stETH/ETH price ratios using Chainlink price feeds and automatically deploys collateral lender funds when price thresholds are breached:

**Automated Risk Response System**

### Tranche Calculation Logic

The system calculates tranche deployment amounts using equal-sized portions of remaining funds:

| Tranche | Trigger | Amount Deployed |
| --- | --- | --- |
| 1 | -1.0% price drop | 1/3 of unutilized funds |
| 2 | -2.1% price drop | 1/2 of remaining funds |
| 3 | -3.3% price drop | All remaining funds |

Sources: [src/LVLidoVaultUtil.sol31-33]() [src/LVLidoVaultUtil.sol222-227]() [src/LVLidoVault.sol665-682]()

## Rewards and Settlement

### Interest Calculation

Collateral lenders earn a fixed 0.5% APY on their deployed funds, calculated based on the time their capital is utilized:

### Epoch Settlement Process

At epoch end, the system:

1. Calculates total collateral lender rewards based on utilization time
2. Distributes proportional shares to each collateral lender
3. Creates new `CollateralLenderOrder` entries with updated amounts
4. Resets utilization tracking variables

**Collateral Lender Settlement Flow**

Sources: [src/LVLidoVaultUtil.sol333-336]() [src/LVLidoVaultUtil.sol415-427]()

## Order Management

### Withdrawing Unutilized Funds

Collateral lenders can withdraw their funds using `withdrawCLOrder()` as long as they haven't been utilized in the current epoch:

### Withdrawal Restrictions

* Funds can only be withdrawn if not currently utilized (`totalCLDepositsUtilized`)
* Once funds are deployed to prevent liquidations, they remain locked until epoch settlement
* The system uses a swap-and-pop pattern for efficient order removal from arrays

Sources: [src/LVLidoVault.sol1044-1068]()

## Technical Implementation

### Core Data Structures

The system uses several key data structures for collateral lender management:

### Integration with Order Matching

During epoch start, the `tryMatchOrders()` function reserves collateral lender funds proportional to borrower debt:

The `inverseBorrowCLAmount` parameter (defaulting to 2) means collateral lenders back 50% of new borrower debt.

**Collateral Lender Order Matching Process**

Sources: [src/LVLidoVault.sol62-64]() [src/LVLidoVault.sol369-402]() [src/LVLidoVault.sol47]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [For Collateral Lenders]()
* [Overview]()
* [Creating Collateral Lender Orders]()
* [Deposit Process]()
* [State Tracking]()
* [Risk Mitigation System]()
* [Automated Tranche Deployment]()
* [Tranche Calculation Logic]()
* [Rewards and Settlement]()
* [Interest Calculation]()
* [Epoch Settlement Process]()
* [Order Management]()
* [Withdrawing Unutilized Funds]()
* [Withdrawal Restrictions]()
* [Technical Implementation]()
* [Core Data Structures]()
* [Integration with Order Matching]()