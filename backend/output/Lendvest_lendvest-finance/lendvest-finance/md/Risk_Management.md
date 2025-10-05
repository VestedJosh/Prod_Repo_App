## Risk Monitoring Architecture

The LVLidoVault implements a comprehensive risk monitoring system that continuously tracks collateral price movements and automatically responds to protect the system from liquidation.

### Price Feed Integration

The system monitors the wstETH/WETH exchange rate by converting through USD pricing feeds. The `getWstethToWeth()` function calculates the current redemption rate by:

1. Converting wstETH to stETH using `IWsteth.stEthPerToken()`
2. Getting stETH price in USD from Chainlink feed
3. Converting to ETH value using ETH/USD price feed

**Sources:** [src/LVLidoVaultUtil.sol68-77]() [src/LVLidoVaultUtil.sol24-26]() [src/LVLidoVaultUtil.sol50-51]()

## Collateral Lender Tranche System

The system implements a three-tier collateral lender tranche mechanism that automatically adds protective collateral as the wstETH price declines relative to the initial redemption rate.

### Tranche Trigger Logic

### Tranche Calculation Algorithm

The system calculates which tranches to trigger using the following logic in `performUpkeep()`:

**Sources:** [src/LVLidoVaultUtil.sol28-33]() [src/LVLidoVaultUtil.sol104-140]() [src/LVLidoVaultUtil.sol204-235]()

## Liquidation System

When all collateral lender tranches are exhausted and the price continues to decline, the system enables liquidation through the Ajna protocol integration.

### Liquidation Process Flow

### Liquidation Proxy Integration

The `LiquidationProxy` contract serves as an intermediary between the vault and Ajna's liquidation mechanisms:

| Function | Purpose | Access Control |
| --- | --- | --- |
| `lenderKick()` | Initiate liquidation auction | External kickers with bond |
| `take()` | Purchase collateral during auction | External takers |
| `settle()` | Finalize liquidation process | Anyone after auction |
| `getBondSize()` | Query required kicker bond | View function |
| `auctionStatus()` | Get current auction state | View function |

**Sources:** [src/LiquidationProxy.sol]() [script/postDeployment2.s.sol11-16]()

## Automated Risk Mitigation Tasks

The `LVLidoVaultUtil` contract implements multiple automation tasks through Chainlink Automation to handle different risk scenarios:

### Task Classification

### Task Execution Logic

The `checkUpkeep()` function implements a priority-based task selection:

1. **Rate Update (Task 221)** - Highest priority when term ends
2. **Collateral Addition (Task 0)** - During active term with price drops
3. **Liquidation Enable (Task 3)** - When tranches exhausted
4. **Term End (Task 1)** - Queue Lido withdrawals
5. **Settlement (Task 2)** - Process claims and distribute funds

**Sources:** [src/LVLidoVaultUtil.sol79-177]() [src/LVLidoVaultUtil.sol179-438]()

## Risk Parameters and Constants

The system uses several key constants that define risk thresholds and behaviors:

| Parameter | Value | Description |
| --- | --- | --- |
| `FACTOR_COLLATERAL_INCREASE` | `11e15` (1.1%) | Price drop threshold between tranches |
| `MAX_TRANCHES` | `3` | Maximum number of collateral tranches |
| `priceDifferencethreshold` | `-1%` | Initial liquidation threshold |
| `PRICE_FEED_DECIMALS` | `8` | Chainlink price feed decimal precision |
| `lidoClaimDelay` | `10 days` | Lido withdrawal claim waiting period |

### Threshold Calculation

Each tranche is triggered when the cumulative price drop reaches:

* Tranche 1: -1.0% (base threshold)
* Tranche 2: -2.1% (base + 1.1%)
* Tranche 3: -3.3% (base + 2.2%)
* Liquidation: > -3.3% (all tranches exhausted)

**Sources:** [src/LVLidoVaultUtil.sol28-34]() [src/LVLidoVaultUtil.sol97-98]() [src/LVLidoVaultUtil.sol115-116]()

## Emergency Mechanisms

### Manual Debt Repayment

The system includes a manual intervention mechanism through the `repayAjnaDebt()` function, allowing external parties to repay vault debt in emergency situations where automated processes fail.

### Liquidation Bypass

During critical market conditions, the system can bypass normal liquidation procedures if sufficient manual repayments are made to cover outstanding debt obligations.

**Sources:** [test/Main.t.sol148-154]() [src/LVLidoVaultUtil.sol301-312]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Risk Management]()
* [Risk Monitoring Architecture]()
* [Price Feed Integration]()
* [Collateral Lender Tranche System]()
* [Tranche Trigger Logic]()
* [Tranche Calculation Algorithm]()
* [Liquidation System]()
* [Liquidation Process Flow]()
* [Liquidation Proxy Integration]()
* [Automated Risk Mitigation Tasks]()
* [Task Classification]()
* [Task Execution Logic]()
* [Risk Parameters and Constants]()
* [Threshold Calculation]()
* [Emergency Mechanisms]()
* [Manual Debt Repayment]()
* [Liquidation Bypass]()