
## Configuration Overview

After deploying the core contracts, several configuration steps must be executed to establish proper contract relationships and security settings. The post-deployment configuration involves four distinct scripts that must be run in sequence to ensure contracts can communicate and operate correctly.

The configuration process establishes critical relationships between contracts, sets up automation addresses, and transfers ownership to the appropriate controlling contracts for security.

## Configuration Scripts

The system includes four post-deployment configuration scripts located in the `script/` directory. Each script handles a specific aspect of the system configuration:

| Script | Purpose | Target Contract | Configuration Action |
| --- | --- | --- | --- |
| `postDeployment1.s.sol` | Set automation address | LVLidoVault | Links vault to automation utility |
| `postDeployment2.s.sol` | Configure liquidation proxy | LiquidationProxy | Links proxy to main vault |
| `postDeployment3.s.sol` | Set forwarder address | LVLidoVaultUtil | Configures Chainlink forwarder |
| `postDeployment4.s.sol` | Transfer ownership | LVToken, LiquidationProxy | Secures contracts under vault control |

### Script 1: Automation Address Configuration

The first configuration script establishes the connection between the main vault and its automation utility contract.

**Configuration Details:**

* Contract: `LVLidoVault`
* Function: `setLVLidoVaultUtilAddress()`
* Purpose: Links the main vault to its automation utility for epoch management

Sources: [script/postDeployment1.s.sol1-21]()

### Script 2: Liquidation Proxy Configuration

The second script configures the liquidation proxy to reference the main vault contract.

**Configuration Details:**

* Contract: `LiquidationProxy`
* Function: `setLVLidoVault()`
* Purpose: Links the liquidation proxy to the main vault for liquidation operations

Sources: [script/postDeployment2.s.sol1-21]()

### Script 3: Forwarder Address Configuration

The third script sets up the Chainlink forwarder address in the automation utility contract.

**Configuration Details:**

* Contract: `LVLidoVaultUtil`
* Function: `setForwarderAddress()`
* Purpose: Configures the Chainlink forwarder for automation services

Sources: [script/postDeployment3.s.sol1-21]()

### Script 4: Ownership Transfer

The final script transfers ownership of critical contracts to the main vault for security and proper access control.

**Ownership Transfers:**

* Both LVToken contracts (LVWETH and LVWSTETH) → LVLidoVault
* LiquidationProxy → LVLidoVault

Sources: [script/postDeployment4.s.sol1-32]()

## Configuration Sequence

The post-deployment configuration must be executed in the correct sequence to ensure proper system initialization:

### Execution Commands

Each script should be executed using Forge with the appropriate network configuration:

## Address Updates Required

Before running the configuration scripts, the contract addresses must be updated in each script file to match your deployed instances:

| Script | Address Variables to Update |
| --- | --- |
| `postDeployment1.s.sol` | `lvlidoAddress`, `LVLidoVaultUtil` address |
| `postDeployment2.s.sol` | `proxyAddress`, `LVLidoVault` address |
| `postDeployment3.s.sol` | `proxyAddress`, `forwarderAddress` |
| `postDeployment4.s.sol` | `lvlidoAddress`, `lvtokenAddress`, `lvtokenAddress2`, `liquidationProxyAddress` |

## Configuration Relationships

The post-deployment configuration establishes the following contract relationships:

These relationships enable:

* Automated epoch management through `LVLidoVaultUtil`
* Liquidation operations through `LiquidationProxy`
* Chainlink automation integration via forwarder
* Vault ownership of token contracts for minting/burning operations

Sources: [script/postDeployment1.s.sol1-21]() [script/postDeployment2.s.sol1-21]() [script/postDeployment3.s.sol1-21]() [script/postDeployment4.s.sol1-32]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Post-Deployment Configuration]()
* [Configuration Overview]()
* [Configuration Scripts]()
* [Script 1: Automation Address Configuration]()
* [Script 2: Liquidation Proxy Configuration]()
* [Script 3: Forwarder Address Configuration]()
* [Script 4: Ownership Transfer]()
* [Configuration Sequence]()
* [Execution Commands]()
* [Address Updates Required]()
* [Configuration Relationships]()