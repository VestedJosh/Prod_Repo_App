For Lenders
-----------

Lenders provide WETH to earn interest from borrowers. They benefit from leveraged lending through the Ajna protocol integration and earn additional yield from unutilized funds in the flagship vault.

### Creating Lender Orders

Lenders deposit WETH using the `createLenderOrder` function:

**Requirements:**

* `amount > 0` to prevent zero-value transactions
* Must approve WETH transfer to the vault contract
* Total system value must not exceed the `maxFundsLimiter` threshold (10,000 USD equivalent)

**Process:**

1. Approve WETH spending: `IERC20(WETH_ADDRESS).approve(vaultAddress, amount)`
2. Call `createLenderOrder(amount)`
3. WETH is transferred to the vault and tracked in `totalLenderQTUnutilized`

| State Variable | Purpose |
| --- | --- |
| `totalLenderQTUnutilized` | Tracks unmatched lender deposits |
| `totalLenderQTUtilized` | Tracks deposits actively earning interest |
| `lenderOrders[]` | Array storing pending lender orders |

### Lender Order Matching

During `startEpoch()`, lender orders are matched with borrower orders using a 97.5% utilization rate:

* 97.5% of deposited WETH is used for lending
* 2.5% is reserved for interest payments
* Unutilized funds are deposited into the flagship vault for additional yield

### Withdrawing Lender Orders

Lenders can withdraw using `withdrawLenderOrder()`:

**Before Epoch Start:**

* Withdraw full unutilized WETH amount
* No fees or penalties

**After Epoch Settlement:**

* Withdraw principal plus interest earned
* Includes gains from flagship vault if funds were unutilized
* May include liquidation proceeds if applicable

Sources: [src/LVLidoVault.sol873-887]() [src/LVLidoVault.sol950-999]() [src/LVLidoVault.sol222-432]()

For Borrowers
-------------

Borrowers deposit wstETH as collateral to obtain leveraged positions. The system provides 10x leverage through flash loans and Ajna protocol integration.

### Creating Borrower Orders

Borrowers deposit wstETH collateral using the `createBorrowerOrder` function:

**Requirements:**

* `collateralAmount > 0`
* Must approve wstETH transfer to the vault contract
* System value limits enforced by `maxFundsLimiter`

**Process:**

1. Approve wstETH spending: `IERC20(WSTETH_ADDRESS).approve(vaultAddress, collateralAmount)`
2. Call `createBorrowerOrder(collateralAmount)`
3. wstETH is transferred and tracked in global accounting variables

### Leverage Mechanism

When orders are matched during `startEpoch()`:

1. **Flash Loan Execution**: System borrows additional wstETH via Balancer flash loan
2. **Leverage Calculation**: `flashLoanAmount = collateralAmount * (leverageFactor - 10) / 10`
3. **Ajna Integration**: Combined collateral deposited into Ajna pool to draw WETH debt
4. **Conversion**: Borrowed WETH converted to wstETH to repay flash loan

| Parameter | Value | Purpose |
| --- | --- | --- |
| `leverageFactor` | 100 (10x) | Determines leverage multiplier |
| `inverseBorrowCLAmount` | 2 | Requires 50% CL backing for new debt |

### Risk and Liquidation

Borrowers face liquidation risk if wstETH/ETH price drops significantly:

* Automated collateral addition at -1%, -2.1%, -3.3% price drops
* Liquidation enabled if collateral lender funds exhausted
* Borrowers may lose deposited collateral during liquidation auctions

### Withdrawing Borrower Orders

Use `withdrawBorrowerOrder()` to withdraw:

**Before Epoch Start:**

* Full collateral withdrawal available
* No penalties

**After Liquidation:**

* May have zero withdrawable funds if fully liquidated
* Function will revert with `NoUnfilledOrdersFound` if no funds available

Sources: [src/LVLidoVault.sol895-914]() [src/LVLidoVault.sol169-213]() [src/LVLidoVault.sol1008-1034]()

For Collateral Lenders
----------------------

Collateral lenders provide additional wstETH collateral to earn fees while helping maintain system health and preventing liquidations.

### Creating Collateral Lender Orders

Collateral lenders deposit wstETH using the `createCLOrder` function:

**Requirements:**

* `amount > 0`
* Must approve wstETH transfer
* System value limits apply

### Collateral Lender Utilization

Collateral lenders earn fees through a tiered utilization system:

1. **Initial Matching**: 50% of new borrower debt backed by CL funds
2. **Automated Risk Response**: Additional tranches deployed at price drops:
   * Tranche 1: -1% price drop → 1/3 of remaining CL funds
   * Tranche 2: -2.1% price drop → 1/2 of remaining CL funds
   * Tranche 3: -3.3% price drop → All remaining CL funds

### Risk Management Role

### Fee Structure and Returns

Collateral lenders earn fees based on:

* Utilization rate of their deposits
* Duration of utilization during the 22-day term
* Risk assumed (higher utilization = higher risk = higher rewards)

### Withdrawing Collateral Lender Orders

Use `withdrawCLOrder()` to withdraw:

**Before Utilization:**

* Full deposit withdrawal available

**After Utilization:**

* Remaining unutilized funds plus earned fees
* May have reduced amounts if utilized funds were lost to liquidation

Sources: [src/LVLidoVault.sol924-941]() [src/LVLidoVault.sol665-682]() [src/LVLidoVault.sol1044-1068]()

Community Functions
-------------------

### Starting Epochs

Any user can call `startEpoch()` to begin a new term:

**Requirements:**

* Epoch cooldown period elapsed (`epochCoolDownPeriod` = 1 week)
* Previous epoch not currently active
* Minimum 72 hours since contract deployment

**Process:**

1. Sets current wstETH redemption rate
2. Matches pending orders via `tryMatchOrders()`
3. Deposits unutilized lender funds into flagship vault
4. Begins 22-day active term

### Emergency Debt Repayment

Community members can help prevent liquidations using `repayAjnaDebt()`:

This function allows anyone to repay vault debt using their own WETH, which may be necessary when Lido withdrawal delays extend beyond the claim period.

Sources: [src/LVLidoVault.sol440-490]() [src/LVLidoVault.sol701-719]()