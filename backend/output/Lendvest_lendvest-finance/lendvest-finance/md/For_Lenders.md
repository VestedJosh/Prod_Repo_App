## Overview

Lenders in the LVLidoVault system provide WETH (Wrapped Ethereum) that borrowers can access to create leveraged positions with their wstETH collateral. The system operates on fixed-term epochs (22 days by default) where lender funds are matched with borrower demands through an automated order matching system.

### Lender Flow Diagram

Sources: [src/LVLidoVault.sol873-887]() [src/LVLidoVault.sol440-490]() [src/LVLidoVault.sol950-999]()

## Creating Lender Orders

### Basic Order Creation

Lenders create orders by calling the `createLenderOrder()` function with the amount of WETH they want to lend:

| Parameter | Type | Description |
| --- | --- | --- |
| `amount` | `uint256` | Amount of WETH to deposit for lending |

The function performs the following operations:

1. Validates the amount is not zero
2. Checks against maximum fund limits via `maxFundsLimiter()`
3. Creates a new `VaultLib.LenderOrder` struct
4. Updates `totalLenderQTUnutilized` accounting
5. Transfers WETH from the lender to the vault

Sources: [src/LVLidoVault.sol873-887]() [src/LVLidoVault.sol109-119]()

### Fund Limits and Safety

The system implements a maximum fund limit of $10,000 USD equivalent through the `maxFundsLimiter()` function. This calculates the total value of all deposits (quote tokens and collateral tokens) using hardcoded prices and prevents excessive exposure.

Sources: [src/LVLidoVault.sol109-119]()

## Order Matching and Epoch System

### Epoch Lifecycle

The vault operates in discrete epochs with the following phases:

| Phase | Duration | Description |
| --- | --- | --- |
| Collection | Variable | Users create orders, no active lending |
| Active Term | 22 days | Funds are utilized, earning interest |
| Settlement | Variable | Withdrawals processed, positions unwound |
| Cooldown | 1 week | Required gap between epochs |

### Order Matching Process

During `startEpoch()`, the `tryMatchOrders()` function matches lender orders with borrower orders based on available collateral and demand:

The matching algorithm:

1. Reserves 2.5% of lender funds for interest payments
2. Uses 97.5% (`initialUtilization = 975e15`) for active lending
3. Matches orders until lender or borrower capacity is exhausted
4. Scales partial orders when full matching isn't possible

Sources: [src/LVLidoVault.sol222-432]() [src/LVLidoVault.sol440-490]()

### Fund Allocation Strategy

Matched lender funds are allocated as follows:

| Allocation | Percentage | Destination | Purpose |
| --- | --- | --- | --- |
| Active Lending | 97.5% | Ajna Pool | Earn interest from borrowers |
| Interest Reserve | 2.5% | Reserved | Cover interest payments |
| Unutilized Funds | Variable | Flagship Vault | Earn yield on unmatched funds |

Sources: [src/LVLidoVault.sol293-295]() [src/LVLidoVault.sol468-489]()

## Interest Earning Mechanism

### Ajna Pool Integration

Matched lender funds are deposited into the Ajna lending pool where they earn interest from borrowers. The vault interacts with Ajna through:

* `pool.addQuoteToken()` - Deposits lender funds
* Interest accrual through Ajna's native mechanisms
* Withdrawal via `pool.removeQuoteToken()` at epoch end

### Flagship Vault Integration

Unutilized lender funds (those not matched with borrowers) are automatically deposited into the Flagship Vault (Morpho) to earn additional yield:

The system tracks flagship vault shares and converts them back to WETH during withdrawals.

Sources: [src/LVLidoVault.sol405-407]() [src/LVLidoVault.sol472-489]() [src/LVLidoVault.sol990-992]()

## Withdrawal Process

### Standard Withdrawal

Lenders can withdraw their funds by calling `withdrawLenderOrder()`. The function handles both types of lender positions:

1. **Direct WETH deposits** - Funds held as `quoteAmount` in orders
2. **Flagship vault shares** - Funds earning yield in Morpho

### Withdrawal Flow

The withdrawal process:

1. Iterates through `lenderOrders` array to find caller's orders
2. Sums up both direct WETH amounts and flagship vault shares
3. Redeems vault shares for WETH if present
4. Transfers total amount to the lender
5. Removes processed orders using swap-and-pop pattern for gas efficiency

Sources: [src/LVLidoVault.sol950-999]()

### Order Management

The system uses an efficient swap-and-pop pattern to remove fulfilled orders, minimizing gas costs by avoiding array shifting operations.

Sources: [src/LVLidoVault.sol964-972]()

## Key Contracts and Functions

### Primary Functions

| Function | Purpose | Access |
| --- | --- | --- |
| `createLenderOrder(uint256)` | Create new lending order | Public |
| `withdrawLenderOrder()` | Withdraw funds and close orders | Public (own orders only) |
| `startEpoch()` | Initiate order matching | Public |

### State Variables

| Variable | Type | Description |
| --- | --- | --- |
| `totalLenderQTUnutilized` | `uint256` | Total unmatched lender WETH |
| `totalLenderQTUtilized` | `uint256` | Total matched lender WETH in Ajna |
| `flagshipVaultShares` | `uint256` | Total shares in Flagship Vault |
| `lenderOrders` | `VaultLib.LenderOrder[]` | Array of pending orders |

Sources: [src/LVLidoVault.sol35-37]() [src/LVLidoVault.sol60]()

### Data Structures

The `VaultLib.LenderOrder` struct contains:

* `lender`: Address of the lender
* `quoteAmount`: Direct WETH deposit amount
* `vaultShares`: Flagship vault shares owned

Sources: [src/libraries/VaultLib.sol]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [For Lenders]()
* [Purpose and Scope]()
* [Overview]()
* [Lender Flow Diagram]()
* [Creating Lender Orders]()
* [Basic Order Creation]()
* [Fund Limits and Safety]()
* [Order Matching and Epoch System]()
* [Epoch Lifecycle]()
* [Order Matching Process]()
* [Fund Allocation Strategy]()
* [Interest Earning Mechanism]()
* [Ajna Pool Integration]()
* [Flagship Vault Integration]()
* [Withdrawal Process]()
* [Standard Withdrawal]()
* [Withdrawal Flow]()
* [Order Management]()
* [Key Contracts and Functions]()
* [Primary Functions]()
* [State Variables]()
* [Data Structures]()