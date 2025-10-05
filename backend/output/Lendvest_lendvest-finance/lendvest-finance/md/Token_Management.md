## Token Architecture Overview

The LVLidoVault system manages four primary token types that serve different roles in the lending and borrowing ecosystem:

| Token Type | Symbol | Purpose | Contract Type |
| --- | --- | --- | --- |
| External Quote Token | WETH | Primary lending currency | Standard ERC20 |
| External Collateral Token | wstETH | Collateral for borrowing | Lido staking token |
| Internal Quote Token | LVWETH | Vault shares for WETH lenders | LVToken |
| Internal Collateral Token | LVWSTETH | Vault shares for wstETH depositors | LVToken |

### Token Relationship Diagram

Sources: [test/Main.t.sol30-35]() [script/deployERC20s.s.sol11-12]()

## LVToken Contract Architecture

The `LVToken` contract serves as the foundation for internal vault tokens, providing ERC20 functionality with additional access control for minting and burning operations.

### LVToken Deployment and Configuration

Sources: [test/Main.t.sol52-53]() [test/Main.t.sol74-75]() [script/deployERC20s.s.sol22-27]() [script/postDeployment4.s.sol18-23]()

## Token Lifecycle Management

The token lifecycle within the LVLidoVault system follows a structured flow from user deposits through epoch processing to final withdrawals.

### Token Flow During Epoch Lifecycle

Sources: [test/Main.t.sol100-170]()

## Token Ownership and Access Control

The LVLidoVault system implements a centralized ownership model where the main vault contract controls all internal token operations.

### Ownership Transfer Process

The ownership transfer occurs in the post-deployment phase to ensure proper access control:

| Step | Action | Contract | Target |
| --- | --- | --- | --- |
| 1 | Deploy tokens | `LVToken` | Independent contracts |
| 2 | Deploy vault | `LVLidoVault` | Main controller |
| 3 | Transfer LVWETH ownership | `transferOwnership()` | LVLidoVault |
| 4 | Transfer LVWSTETH ownership | `transferOwnership()` | LVLidoVault |
| 5 | Transfer LiquidationProxy ownership | `transferOwnership()` | LVLidoVault |

### Access Control Architecture

Sources: [script/postDeployment4.s.sol14-27]() [test/Main.t.sol74-76]()

## Token Integration with External Protocols

The vault tokens serve as intermediary representations while the underlying assets are deployed to external DeFi protocols for yield generation.

### External Protocol Token Flow

Sources: [test/Main.t.sol68-71]() [test/Main.t.sol225-232]()

## Token State Management

The LVLidoVault contract maintains several state variables to track token balances and utilization across different user types and external protocols.

### Key State Variables

| Variable | Purpose | Token Type |
| --- | --- | --- |
| `totalLenderDeposits` | Total WETH from lenders | WETH |
| `totalBorrowerDeposits` | Total wstETH from borrowers | wstETH |
| `totalCLDepositsUtilized` | Active collateral lender wstETH | wstETH |
| `totalCLDepositsUnutilized` | Reserve collateral lender wstETH | wstETH |

### Token Balance Reconciliation

The system maintains precise tracking of token balances across internal accounting and external protocol deployments to ensure user withdrawals can be properly calculated and executed.

Sources: [test/Main.t.sol464-467]() [test/Main.t.sol519-522]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Token Management]()
* [Token Architecture Overview]()
* [Token Relationship Diagram]()
* [LVToken Contract Architecture]()
* [LVToken Deployment and Configuration]()
* [Token Lifecycle Management]()
* [Token Flow During Epoch Lifecycle]()
* [Token Ownership and Access Control]()
* [Ownership Transfer Process]()
* [Access Control Architecture]()
* [Token Integration with External Protocols]()
* [External Protocol Token Flow]()
* [Token State Management]()
* [Key State Variables]()
* [Token Balance Reconciliation]()