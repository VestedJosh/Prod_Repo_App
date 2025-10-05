## Overview

The LVLidoVault system integrates with multiple Chainlink services to automate critical vault operations and provide external data feeds. The integration consists of three main components:

* **Chainlink Automation**: Executes automated tasks like collateral management, liquidation triggers, and epoch settlement
* **Chainlink Functions**: Fetches external rate data from sources like Space & Time database
* **Chainlink Price Feeds**: Provides real-time price data for stETH/ETH rates

**Chainlink Integration Architecture**

Sources: [script/deployUpkeepAdmin.s.sol10-12]() [script/postDeployment5.s.sol12-14]()

## UpkeepAdmin Deployment

The `UpkeepAdmin` contract serves as an intermediary for managing Chainlink Automation upkeeps. It provides administrative functions for upkeep management and handles LINK token operations.

### Deployment Process

The UpkeepAdmin deployment requires two key Ethereum mainnet addresses:

| Component | Address | Purpose |
| --- | --- | --- |
| Upkeep Registry | `0x6593c7De001fC8542bB1703532EE1E5aA0D458fD` | Chainlink Automation registry |
| LINK Token | `0x514910771AF9Ca656af840dff83E8264EcF986CA` | LINK token for upkeep funding |

**UpkeepAdmin Deployment and Activation Flow**

The deployment script creates the UpkeepAdmin with references to both the Chainlink Automation registry and LINK token contract.

Sources: [script/deployUpkeepAdmin.s.sol14-22]()

### Upkeep Activation

After deployment, the UpkeepAdmin must accept responsibility for managing specific upkeeps. The activation process uses a specific upkeep ID:

**Upkeep Activation Process**

The upkeep ID `36653741063921031869740428403356924300134765658190440492019233757663320393334` represents the specific automation job that the UpkeepAdmin will manage.

Sources: [script/postDeployment5.s.sol14]()

## Automation Tasks Configuration

The LVLidoVault system uses Chainlink Automation to execute multiple automated tasks identified by specific task IDs. These tasks are managed through the `LVLidoVaultUtil` contract's `checkUpkeep()` and `performUpkeep()` functions.

### Task Types

| Task ID | Task Name | Purpose |
| --- | --- | --- |
| 0 | Add Collateral | Respond to price drops by adding collateral lender funds |
| 1 | Queue Withdrawals | Begin Lido withdrawal process at term end |
| 2 | Settle Epoch | Complete final settlement and fund distribution |
| 3 | Allow Kick | Enable liquidation when collateral is exhausted |
| 221 | Get Rate | Fetch final interest rates via Chainlink Functions |

**Automation Task Routing System**

Sources: Based on system architecture diagrams and automation patterns

## Functions Setup

Chainlink Functions integration enables the vault to fetch external rate data, particularly from the Space & Time database for Aave lending rates. This data is used in the final settlement calculations.

### Rate Data Fetching

The Functions integration is triggered by Task 221 during the automation cycle. The function call retrieves current lending rates that are used to calculate final yields for the epoch settlement.

**Functions Rate Data Flow**

The Functions integration provides decentralized access to off-chain rate data needed for accurate yield calculations.

Sources: Based on system architecture diagrams

## Final Configuration and Ownership

The final step in Chainlink setup involves transferring ownership and renouncing administrative privileges to ensure the system operates in a decentralized manner.

### Ownership Renunciation

After all Chainlink integrations are configured and tested, the deployment process renounces ownership of the core contracts to prevent centralized control:

**Final Ownership Renunciation**

This step ensures that once the Chainlink automation is properly configured, no single entity retains administrative control over the core vault operations.

Sources: [script/postDeployment6.s.sol16-17]()

## Verification Steps

After completing the Chainlink setup, verify the following components are properly configured:

1. **UpkeepAdmin**: Confirm the contract is deployed and has accepted the upkeep responsibility
2. **Automation Tasks**: Verify that `checkUpkeep()` returns appropriate conditions for each task type
3. **Functions Integration**: Test that rate data requests are properly routed and responses are handled
4. **Price Feeds**: Confirm price feed integration for stETH/ETH rates
5. **Ownership**: Verify that core contracts have renounced ownership

The system should now be capable of autonomous operation through Chainlink's decentralized automation network.

Sources: [script/deployUpkeepAdmin.s.sol]() [script/postDeployment5.s.sol]() [script/postDeployment6.s.sol]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Chainlink Setup]()
* [Overview]()
* [UpkeepAdmin Deployment]()
* [Deployment Process]()
* [Upkeep Activation]()
* [Automation Tasks Configuration]()
* [Task Types]()
* [Functions Setup]()
* [Rate Data Fetching]()
* [Final Configuration and Ownership]()
* [Ownership Renunciation]()
* [Verification Steps]()