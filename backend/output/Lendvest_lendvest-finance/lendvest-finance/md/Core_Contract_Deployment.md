For information about development environment setup and prerequisites, see [Prerequisites and Setup](). For post-deployment configuration and contract wiring, see [Post-Deployment Configuration]().

## Deployment Overview

The LVLidoVault system requires deploying multiple interconnected contracts in a specific sequence due to constructor dependencies. The deployment process involves five main steps executed through separate Foundry scripts.

### Deployment Sequence Diagram

Sources: [script/deployERC20s.s.sol1-32]() [script/deployPool.s.sol1-25]() [script/deployProxy.s.sol1-18]() [script/deployLVLidoVault.s.sol1-23]() [script/deployLVLidoVaultUtil.s.sol1-22]()

## Contract Deployment Steps

### Step 1: Deploy Vault Tokens

The first step deploys the `LVToken` contracts that represent shares in the vault for both WETH lenders and wstETH depositors.

The `DeployERC20s` contract creates two `LVToken` instances without any constructor parameters, as they inherit standard ERC20 functionality.

Sources: [script/deployERC20s.s.sol17-30]()

### Step 2: Deploy Ajna Pool

The Ajna pool serves as the core lending pool where leveraged positions are managed. It requires the previously deployed vault tokens as collateral and quote tokens.

| Parameter | Value | Description |
| --- | --- | --- |
| `collateralToken` | LVWSTETH address | wstETH-backed vault token |
| `quoteToken` | LVWETH address | WETH-backed vault token |
| `interestRate` | `1e16` (1%) | Initial pool interest rate |

The deployment uses the `IERC20PoolFactory.deployPool()` function to create the pool instance.

Sources: [script/deployPool.s.sol15-24]()

### Step 3: Deploy Liquidation Proxy

The `LiquidationProxy` contract handles liquidation operations and requires the Ajna pool address for initialization.

Sources: [script/deployProxy.s.sol9-16]()

### Step 4: Deploy Main Vault

The `LVLidoVault` contract is the core system component and requires both the Ajna pool and liquidation proxy addresses.

| Constructor Parameter | Purpose |
| --- | --- |
| `ajnaPoolAddress` | References the lending pool for leveraged operations |
| `liquidationProxyAddress` | Enables liquidation functionality |

Sources: [script/deployLVLidoVault.s.sol15-21]()

### Step 5: Deploy Utility Contract

The final deployment creates the `LVLidoVaultUtil` contract, which provides automation and utility functions for the main vault.

The utility contract constructor takes the main vault address to establish the connection for automated operations.

Sources: [script/deployLVLidoVaultUtil.s.sol14-20]()

## Contract Dependencies

The deployment order is critical due to constructor dependencies between contracts:

Sources: [script/deployPool.s.sol11-12]() [script/deployProxy.s.sol11]() [script/deployLVLidoVault.s.sol12-13]() [script/deployLVLidoVaultUtil.s.sol12]()

## Deployment Script Configuration

Each deployment script contains hardcoded addresses that reference either mainnet protocol addresses or previously deployed contract addresses:

### External Protocol Addresses

* **WETH**: `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2`
* **wstETH**: `0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0`
* **Ajna Pool Factory**: `0x6146DD43C5622bB6D12A5240ab9CF4de14eDC625`

### Contract Address References

The scripts contain specific deployed contract addresses that must be updated based on the actual deployment results:

| Script | Referenced Address | Purpose |
| --- | --- | --- |
| `deployPool.s.sol` | LVWETH, LVWSTETH addresses | Pool token parameters |
| `deployProxy.s.sol` | Ajna pool address | Proxy initialization |
| `deployLVLidoVault.s.sol` | Ajna pool, LiquidationProxy addresses | Vault initialization |
| `deployLVLidoVaultUtil.s.sol` | LVLidoVault address | Utility contract initialization |

Sources: [script/deployERC20s.s.sol10-12]() [script/deployPool.s.sol10-12]() [script/deployProxy.s.sol11]() [script/deployLVLidoVault.s.sol12-13]() [script/deployLVLidoVaultUtil.s.sol12]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Core Contract Deployment]()
* [Deployment Overview]()
* [Deployment Sequence Diagram]()
* [Contract Deployment Steps]()
* [Step 1: Deploy Vault Tokens]()
* [Step 2: Deploy Ajna Pool]()
* [Step 3: Deploy Liquidation Proxy]()
* [Step 4: Deploy Main Vault]()
* [Step 5: Deploy Utility Contract]()
* [Contract Dependencies]()
* [Deployment Script Configuration]()
* [External Protocol Addresses]()
* [Contract Address References]()