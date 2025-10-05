| --- | --- | --- | --- |
| Lenders | WETH | Provide liquidity for borrowing | `VaultLib.LenderOrder` |
| Borrowers | wstETH | Deposit collateral to borrow WETH | `VaultLib.BorrowerOrder` |
| Collateral Lenders | wstETH | Additional collateral for liquidation protection | `VaultLib.CollateralLenderOrder` |

**Order Management System**

Sources: [src/LVLidoVault.sol60-64]() [src/LVLidoVault.sol872-941]() [src/LVLidoVault.sol222-432]()

Epoch Lifecycle and Automation
------------------------------

The system operates through discrete epochs, each containing a fixed-term lending period followed by settlement. Chainlink Automation manages the lifecycle transitions and risk mitigation.

**Epoch State Management**

Sources: [src/LVLidoVault.sol440-490]() [src/LVLidoVault.sol48-58]() [README.md53-63]()

External Protocol Integrations
------------------------------

The vault integrates with multiple DeFi protocols to enable leveraged lending and yield generation:

**Integration Architecture**

Sources: [src/LVLidoVault.sol25-31]() [src/LVLidoVault.sol132-154]() [src/LVLidoVault.sol169-213]() [src/LVLidoVault.sol596-614]()

Chainlink Automation Tasks
--------------------------

The `LVLidoVaultUtil` contract implements five distinct automation tasks that manage the vault lifecycle and risk mitigation:

| Task ID | Function | Trigger Condition | Purpose |
| --- | --- | --- | --- |
| 0 | Add Collateral | Price drop detection | `avoidLiquidation()` - Add CL collateral |
| 1 | Queue Withdrawals | Term end reached | `requestWithdrawalsWstETH()` - Start Lido exit |
| 2 | Settle Epoch | Withdrawal delay passed | `claimWithdrawal()` + settlement |
| 3 | Enable Liquidation | Collateral exhausted | `setAllowKick(true)` - Allow auctions |
| 221 | Fetch Rate | Term completion | Chainlink Functions rate query |

**Automation Flow**

Sources: [README.md38-51]() [src/LVLidoVault.sol596-614]() [src/LVLidoVault.sol665-682]()

Token Flow and Flash Loan Mechanics
-----------------------------------

The system uses flash loans from Balancer to provide leverage for borrowers while maintaining proper collateralization ratios:

**Flash Loan Execution Flow**

Sources: [src/LVLidoVault.sol169-213]() [src/LVLidoVault.sol132-154]() [src/LVLidoVault.sol422-431]()

Risk Management and Liquidation
-------------------------------

The system implements a multi-tiered risk management approach using collateral lender tranches and automated liquidation mechanisms:

**Collateral Lender Tranche System**

Sources: [src/LVLidoVault.sol55]() [src/LVLidoVault.sol665-682]() [src/LVLidoVault.sol1076-1095]() [README.md41-43]()