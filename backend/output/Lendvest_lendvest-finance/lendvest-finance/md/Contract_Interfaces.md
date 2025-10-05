## Core Contract Interfaces

The LVLidoVault system exposes several primary interfaces that enable user interaction, automated management, and protocol integration.

### LVLidoVault Main Interface

The `LVLidoVault` contract serves as the central hub with over 80 public functions categorized into distinct operational areas:

**Order Creation Interface Functions:**

| Function | Purpose | Access | Returns |
| --- | --- | --- | --- |
| `createLenderOrder(uint256)` | Create WETH lending order | Public | `uint256 amount` |
| `createBorrowerOrder(uint256)` | Create wstETH borrowing order | Public | `uint256 collateralAmount` |
| `createCLOrder(uint256)` | Create collateral lender order | Public | `uint256 amount` |

**Withdrawal Interface Functions:**

| Function | Purpose | Access | Returns |
| --- | --- | --- | --- |
| `withdrawLenderOrder()` | Withdraw unutilized lender funds | Public | `uint256 withdrawn` |
| `withdrawBorrowerOrder()` | Withdraw unutilized borrower collateral | Public | `uint256 withdrawn` |
| `withdrawCLOrder()` | Withdraw unutilized CL collateral | Public | `uint256 withdrawn` |

**Epoch Management Interface:**

| Function | Purpose | Access | Modifiers |
| --- | --- | --- | --- |
| `startEpoch()` | Initialize new lending epoch | Public | `lock` |
| `tryMatchOrders()` | Match pending orders | Internal | - |
| `end_epoch()` | Finalize current epoch | Proxy Only | - |

Sources: [src/LVLidoVault.sol865-941]() [src/LVLidoVault.sol943-1068]() [src/LVLidoVault.sol440-490]()

### Proxy Function Interface

The vault exposes numerous proxy functions restricted to `LVLidoVaultUtil` and `LiquidationProxy` contracts:

**Key Proxy Functions:**

| Function Category | Representative Functions | Purpose |
| --- | --- | --- |
| Order Management | `lenderOrdersPush()`, `borrowerOrdersPush()` | Array manipulation for order books |
| Token Operations | `mintForProxy()`, `burnForProxy()` | Test token mint/burn operations |
| Lido Integration | `requestWithdrawalsWstETH()`, `claimWithdrawal()` | Manage Lido withdrawal queue |
| State Updates | `setTotalLenderQTUtilized()`, `setCurrentRedemptionRate()` | Update vault accounting state |

Sources: [src/LVLidoVault.sol498-563]() [src/LVLidoVault.sol596-624]() [src/LVLidoVault.sol665-808]()

### UpkeepAdmin Interface

The `UpkeepAdmin` contract provides a simple interface for managing Chainlink automation upkeep:

| Function | Purpose | Parameters | Access |
| --- | --- | --- | --- |
| `acceptUpkeepAdmin(uint256)` | Accept upkeep admin role | `id` - upkeep ID | Public |
| `transferLinkToken(uint256, uint96)` | Fund upkeep with LINK | `id, amount` | Public |
| `getUpkeep(uint256)` | Get upkeep information | `id` - upkeep ID | View |

**UpkeepInfo Structure:**

Sources: [src/UpkeepAdmin.sol39-63]() [src/UpkeepAdmin.sol20-31]()

## External Protocol Interfaces

The LVLidoVault system integrates with multiple external protocols through well-defined interfaces:

### Ajna Pool Interface Integration

The vault interacts with Ajna lending pools through the `IERC20Pool` interface:

**Key Ajna Functions Used:**

* `drawDebt(address, uint256, uint256, uint256)` - Borrow against collateral
* `addQuoteToken(uint256, uint256, uint256)` - Deposit lending funds
* `removeQuoteToken(uint256, uint256)` - Withdraw lending funds
* `lenderKick(uint256, uint256)` - Initiate liquidation auction
* `repayDebt(address, uint256, uint256, address, uint256)` - Repay borrowed funds

### Lido Protocol Interface Integration

Multiple Lido interfaces enable stETH/wstETH operations:

**IWsteth Interface:**

* `wrap(uint256)` - Convert stETH to wstETH
* `stEthPerToken()` - Get current redemption rate

**ISteth Interface:**

* `submit(address)` - Stake ETH for stETH

**Withdrawal Queue Interface:**

* `requestWithdrawalsWstETH(uint256[], address)` - Request wstETH withdrawals
* `claimWithdrawal(uint256)` - Claim finalized withdrawals

### Balancer Flash Loan Interface

The vault implements `IFlashLoanRecipient` to handle flash loans:

Sources: [src/LVLidoVault.sol25-31]() [src/LVLidoVault.sol169-213]() [src/LVLidoVault.sol132-154]()

## Data Structures and Types

The system defines several key data structures used across interfaces:

### VaultLib Order Structures

**Order Structure Definitions:**

| Structure | Fields | Purpose |
| --- | --- | --- |
| `LenderOrder` | `lender`, `quoteAmount`, `vaultShares` | Track WETH lending deposits |
| `BorrowerOrder` | `borrower`, `collateralAmount` | Track wstETH borrowing collateral |
| `CollateralLenderOrder` | `collateralLender`, `collateralAmount` | Track additional wstETH collateral |
| `MatchInfo` | `lender`, `borrower`, amounts, reserves | Record matched loan details |

### State Variables Interface

The vault exposes numerous state variables through getter functions:

**Accounting Variables:**

* `totalBorrowAmount` - Total amount borrowed
* `totalLenderQTUtilized/Unutilized` - Lender fund tracking
* `totalBorrowerCT/CTUnutilized` - Borrower collateral tracking
* `totalCollateralLenderCT` - Collateral lender deposits
* `totalCLDepositsUtilized/Unutilized` - CL deposit utilization

**Epoch Variables:**

* `epoch` - Current epoch number
* `epochStarted` - Boolean epoch state
* `epochStart` - Epoch start timestamp
* `termDuration` - Epoch duration (22 days)
* `lastEpochEnd` - Previous epoch end time

**Rate Variables:**

* `epochStartRedemptionRate` - Starting wstETH/stETH rate
* `currentRedemptionRate` - Current wstETH/stETH rate
* `rate` - Interest rate (221e14 = 2.21%)

Sources: [src/LVLidoVault.sol34-68]() [src/libraries/VaultLib.sol]()

## Interface Relationships

The following diagram illustrates how different interfaces interact within the system:

**Interface Access Control:**

| Interface Category | Access Level | Contracts |
| --- | --- | --- |
| User Functions | Public | Any address |
| Proxy Functions | Restricted | `LVLidoVaultUtil`, `LiquidationProxy` |
| Owner Functions | Restricted | Contract owner only |
| Internal Functions | Private | Same contract only |

The `onlyProxy` modifier ensures critical vault operations can only be performed by authorized automation and liquidation contracts, while maintaining public access for user deposit/withdrawal functions.

Sources: [src/LVLidoVault.sol102-107]() [src/interfaces/ILVLidoVault.sol10-70]() [src/LVLidoVault.sol689-692]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Contract Interfaces]()
* [Core Contract Interfaces]()
* [LVLidoVault Main Interface]()
* [Proxy Function Interface]()
* [UpkeepAdmin Interface]()
* [External Protocol Interfaces]()
* [Ajna Pool Interface Integration]()
* [Lido Protocol Interface Integration]()
* [Balancer Flash Loan Interface]()
* [Data Structures and Types]()
* [VaultLib Order Structures]()
* [State Variables Interface]()
* [Interface Relationships]()