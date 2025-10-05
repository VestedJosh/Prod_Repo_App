| Solidity Optimizer | Enabled (200 runs) | Gas optimization |
| Via IR | Enabled | Advanced compilation |
| Incremental Compilation | Enabled | Faster builds |

### External Dependencies

The system integrates with multiple external libraries and protocols through git submodules:

**Sources:** [.gitmodules1-16]() [foundry.toml1-10]()

### Environment Variables

The deployment process requires the following environment variables:

| Variable | Purpose |
| --- | --- |
| `RPC_URL` | Ethereum RPC endpoint |
| `HACKATHON_PK` | Private key for deployment |
| `ETHERSCAN_API_KEY` | Contract verification |

Core Contract Deployment Sequence
---------------------------------

The deployment follows a specific sequence to ensure proper contract dependencies and initialization.

### Deployment Flow

**Sources:** [DEPLOYMENT.md1-25]()

### Step 1: Deploy ERC20 Tokens

Deploy the vault's internal tokens that represent user positions:

Expected deployments:

* `LVWETH` token for lender positions
* `LVWSTETH` token for borrower positions

### Step 2: Deploy Ajna Pool

Deploy the lending pool that facilitates WSTETH/WETH lending:

### Step 3: Deploy LiquidationProxy

Deploy the proxy contract that handles liquidation mechanics:

### Step 4: Deploy Core Vault Contracts

Deploy the main vault and utility contracts:

### Step 5: Deploy UpkeepAdmin

Deploy the Chainlink upkeep administration contract:

**Sources:** [DEPLOYMENT.md1-24]()

Post-Deployment Configuration
-----------------------------

After deploying all contracts, a series of configuration scripts establish the proper relationships and permissions between contracts.

### Configuration Sequence

**Sources:** [DEPLOYMENT.md32-38]()

### Step 1: Set Automation Address

Configure the `LVLidoVaultUtil` with the automation forwarder address:

### Step 2: Configure Liquidation Proxy

Set the vault address in the `LiquidationProxy` contract:

### Step 3: Set Forwarder Address

Configure the Chainlink forwarder address in `LVLidoVaultUtil`:

### Step 4: Initial Ownership Transfers

Transfer ownership of tokens and proxy to the main vault:

### Step 5: Upkeep Admin Transfer

Configure the upkeep admin ownership:

### Step 6: Final Ownership Transfers

Complete the ownership transfer process by renouncing deployer ownership:

**Sources:** [DEPLOYMENT.md32-41]()

Chainlink Services Setup
------------------------

The system requires two Chainlink services: Functions for external data fetching and Automation for periodic task execution.

### Chainlink Functions Configuration

Create a new Chainlink Functions subscription and configure it for Aave rate fetching:

1. **Create Functions Subscription**: Set up a new subscription on the Chainlink platform
2. **Configure Functions**: Deploy rate fetching functions using external repository for Aave rate data
3. **Add Consumer**: Register `LVLidoVaultUtil` as a Functions consumer

### Chainlink Automation Configuration

Set up Chainlink Automation for periodic vault maintenance tasks:

1. **Create Automation Subscription**: Initialize a new upkeep subscription
2. **Configure Upkeeps**: Register the `LVLidoVaultUtil` contract with appropriate task parameters
3. **Transfer Admin Rights**: Transfer subscription administration to the `UpkeepAdmin` contract

### Integration Architecture

**Sources:** [DEPLOYMENT.md26-42]()

Deployment Verification
-----------------------

After completing all deployment and configuration steps, verify the system is properly configured:

### Contract Address Verification

Ensure all contracts are deployed at expected addresses and verify contract source code on Etherscan.

### Permission Verification

Confirm ownership transfers completed successfully:

* ERC20 tokens owned by `LVLidoVault`
* `LiquidationProxy` owned by `LVLidoVault`
* `LVLidoVault` and `LVLidoVaultUtil` ownership renounced
* Chainlink subscription administered by `UpkeepAdmin`

### Integration Testing

Test key integrations to ensure proper functionality:

* Chainlink Functions can fetch external rate data
* Chainlink Automation can execute upkeep tasks
* Contract inter-dependencies function correctly

**Sources:** [DEPLOYMENT.md1-43]()