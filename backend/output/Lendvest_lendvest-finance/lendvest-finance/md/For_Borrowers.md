## Overview

Borrowers in the LVLidoVault system deposit wstETH (wrapped staked ETH) as collateral to obtain leveraged exposure to staking yields. The system provides leverage through flash loans from Balancer, allowing borrowers to amplify their stETH staking position while borrowing WETH from lenders through Ajna pools.

**Key Borrower Flow:**

1. Deposit wstETH collateral via `createBorrowerOrder()`
2. Wait for epoch to start and orders to be matched
3. Receive leveraged stETH position automatically
4. At epoch end, withdraw remaining collateral via `withdrawBorrowerOrder()`

Sources: [src/LVLidoVault.sol895-914]() [src/LVLidoVault.sol1008-1034]()

## Borrower Order Creation

### Creating a Borrower Order

Borrowers deposit wstETH collateral by calling the `createBorrowerOrder()` function. This creates a pending order that will be matched with lender orders during the next epoch start.

**Technical Implementation:**

* Function: `createBorrowerOrder(uint256 collateralAmount)` at [src/LVLidoVault.sol895-914]()
* Updates global accounting: `totalBorrowerCT` and `totalBorrowerCTUnutilized`
* Stores order in `borrowerOrders[]` array with `BorrowerOrder` struct
* Protected by `lock` modifier to prevent reentrancy

**Requirements:**

* `collateralAmount > 0` (prevents zero-value transactions)
* Must not exceed `maxFundsLimiter()` constraints
* Borrower must approve wstETH transfer to vault

Sources: [src/LVLidoVault.sol895-914]() [src/libraries/VaultLib.sol]()

## Leveraged Lending Mechanism

### Order Matching Process

During `startEpoch()`, the system matches borrower orders with lender orders through the `tryMatchOrders()` internal function. This process determines the leverage and debt structure for each borrower.

**Leverage Calculation:**

* Flash loan amount: `collateralAmount * (leverageFactor - 10) / 10`
* Borrow amount: `(flashLoanAmount * epochStartRedemptionRate) / 1e19`
* Total collateral: `baseLoanCollateral + flashLoanAmount`

**Key Variables:**

* `VaultLib.leverageFactor`: Determines leverage multiplier
* `epochStartRedemptionRate`: wstETH/stETH conversion rate at epoch start
* `currentBucketIndex`: Ajna pool price bucket for deposits

Sources: [src/LVLidoVault.sol222-432]() [src/LVLidoVault.sol234-245]()

### Flash Loan Execution

The leverage mechanism uses Balancer flash loans processed through the `receiveFlashLoan()` callback function.

**Flash Loan Process:**

1. Mint test collateral tokens for total position size
2. Draw debt from Ajna pool using collateral
3. Convert borrowed WETH to wstETH through Lido staking
4. Repay flash loan with converted wstETH plus fees

Sources: [src/LVLidoVault.sol169-213]() [src/LVLidoVault.sol132-154]()

## Epoch Lifecycle for Borrowers

### Active Term Management

Once orders are matched and the epoch begins, borrowers have leveraged stETH positions managed automatically by the vault. The system monitors collateral health through Chainlink automation.

**Epoch States:**

* **Order Collection**: Borrowers can create/withdraw orders
* **Active Term**: 22-day term with automated risk management
* **Term End**: Lido withdrawal process and settlement
* **Post-Epoch**: Borrowers can withdraw remaining collateral

**Automated Risk Response:**

* Collateral lenders provide additional backing if stETH price drops
* Liquidation protection through tranched collateral deployment
* Manual debt repayment option for community intervention

Sources: [src/LVLidoVault.sol48-51]() [src/LVLidoVaultUtil.sol]()

### Withdrawal Process

Borrowers can withdraw their collateral in two scenarios:

1. **Pre-Epoch**: Cancel unfulfilled orders via `withdrawBorrowerOrder()`
2. **Post-Epoch**: Withdraw remaining collateral after settlement

**Withdrawal Logic:**

* Uses swap-and-pop pattern for gas-efficient array management
* Updates `totalBorrowerCT` and `totalBorrowerCTUnutilized` tracking
* Reverts with `NoUnfilledOrdersFound` if no orders exist
* Protected by `lock` modifier against reentrancy

Sources: [src/LVLidoVault.sol1008-1034]()

## Risk Management

### Liquidation Risk

Borrowers face liquidation risk if their collateral value drops significantly relative to their debt. The system implements a multi-tier protection mechanism:

**Protection Tiers:**

1. **Collateral Lender Tranches**: Automatic deployment at -1%, -2.1%, -3.3% stETH drops
2. **Liquidation Threshold**: `allowKick` enabled when all tranches exhausted
3. **Auction Process**: Ajna-based liquidation auctions for debt recovery

**Risk Monitoring:**

* Continuous price monitoring via Chainlink oracles
* `priceDifferencethreshold = -1e16` (-1%) for first intervention
* Automated response through `LVLidoVaultUtil` contract

Sources: [src/LVLidoVault.sol55]() [src/LVLidoVault.sol665-682]()

### Collateral Requirements

The system enforces collateral backing requirements through the `inverseBorrowCLAmount` parameter:

**Collateral Ratios:**

* Base collateral: Borrower's wstETH deposit
* Additional backing: 50% of debt value from collateral lenders
* Flash loan leverage: Amplifies total position size

**Fund Limits:**

* `maxFundsLimiter()` enforces $10,000 total value cap during testing phase
* Combines lender funds, borrower collateral, and collateral lender deposits

Sources: [src/LVLidoVault.sol47]() [src/LVLidoVault.sol109-119]() [src/LVLidoVault.sol364-367]()

## Technical Integration Points

### Token Conversions

The system handles multiple token conversions for leveraged positions:

**Conversion Flow in `wethToWsteth()`:**

1. Unwrap WETH to ETH via `IWeth.withdraw()`
2. Submit ETH to Lido via `steth.submit()`
3. Wrap stETH to wstETH via `wsteth.wrap()`

Sources: [src/LVLidoVault.sol132-154]()

### Contract Interactions

Borrowers interact with multiple DeFi protocols through the vault:

| Protocol | Purpose | Key Functions |
| --- | --- | --- |
| **Ajna** | Lending pool for WETH/wstETH | `pool.drawDebt()`, `pool.repayDebt()` |
| **Lido** | ETH staking and wstETH minting | `steth.submit()`, `wsteth.wrap()` |
| **Balancer** | Flash loans for leverage | `vault.flashLoan()` |
| **Flagship Vault** | Yield on unutilized funds | `flagshipVault.deposit()` |

Sources: [src/LVLidoVault.sol25-31]() [src/interfaces/ILVLidoVault.sol10-70]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [For Borrowers]()
* [Overview]()
* [Borrower Order Creation]()
* [Creating a Borrower Order]()
* [Leveraged Lending Mechanism]()
* [Order Matching Process]()
* [Flash Loan Execution]()
* [Epoch Lifecycle for Borrowers]()
* [Active Term Management]()
* [Withdrawal Process]()
* [Risk Management]()
* [Liquidation Risk]()
* [Collateral Requirements]()
* [Technical Integration Points]()
* [Token Conversions]()
* [Contract Interactions]()