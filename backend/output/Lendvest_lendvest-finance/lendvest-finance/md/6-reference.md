|  | `epochStarted()` | Whether current epoch has begun |
|  | `rate()` | Current interest rate |
| **Order Processing** | `lenderOrdersPush()` | Submit lender orders |
|  | `borrowerOrdersPush()` | Submit borrower orders |
|  | `getEpochMatches()` | Retrieve matched orders for epoch |
| **Collateral Management** | `avoidLiquidation()` | Add collateral to prevent liquidation |
|  | `collateralLenderTraunche()` | Current collateral lender tranche level |
| **Token Operations** | `wethToWsteth()` | Convert WETH to wstETH |
|  | `requestWithdrawalsWstETH()` | Queue Lido withdrawals |
| **Liquidation** | `setAllowKick()` | Enable/disable liquidation kicks |
|  | `repayDebtForProxy()` | Repay debt via proxy contract |

**Sources:** [src/interfaces/ILVLidoVault.sol1-71]()

### Interface Integration Patterns

The following diagram shows how the main interface connects with external protocols and internal contract components:

**Sources:** [src/interfaces/ILVLidoVault.sol6-8]()

Configuration Reference
-----------------------

The system uses Foundry for compilation and testing, with specific configuration requirements for the complex contract architecture.

### Foundry Configuration

The `foundry.toml` file defines the build configuration for the entire project:

**Configuration Parameters:**

| Parameter | Value | Purpose |
| --- | --- | --- |
| `viaIR` | `true` | Enables IR-based code generation for complex contracts |
| `optimizer` | `true` | Enables Solidity optimizer |
| `optimizer_runs` | `200` | Optimizes for moderate deployment/runtime cost balance |
| `incremental` | `true` | Enables incremental compilation for faster builds |

The `viaIR` setting is particularly important for this project because the vault contracts are complex and may exceed standard compilation limits without intermediate representation compilation.

**Sources:** [foundry.toml1-10]()

### Deployment Configuration Requirements

**Sources:** [foundry.toml5-7]()

Legal and Licensing
-------------------

The LVLidoVault system is distributed under the Business Source License 1.1, which provides specific terms for usage, modification, and distribution.

### License Overview

The system uses a Business Source License (BSL) 1.1, which allows:

* Non-production use
* Copying and modification
* Creation of derivative works
* Redistribution

**Key License Terms:**

| Aspect | Requirement |
| --- | --- |
| **Non-production Use** | Permitted without restriction |
| **Production Use** | Requires commercial license until Change Date |
| **Modification** | Permitted with license preservation |
| **Distribution** | Must include BSL license notice |
| **Change Date** | To be specified - converts to open source |
| **Change License** | GPL Version 2.0 or compatible |

### License Compliance Requirements

**Copyright Information:**

* **Copyright Holder:** Lendvest (2025)
* **License URL:** [www.mariadb.com/bsl11]()
* **License File:** [LICENSE1-39]()

**Warranty Disclaimer:**
The software is provided "AS IS" without warranties of any kind, including merchantability, fitness for purpose, non-infringement, and title.

**Sources:** [LICENSE1-39]()

### Commercial Licensing

For production use before the Change Date, users must either:

1. Purchase a commercial license from Lendvest or authorized resellers
2. Ensure their use complies with current BSL requirements
3. Wait for the Change Date when the code becomes open source under GPL

The license automatically terminates for any use that violates the BSL terms, affecting both current and future versions of the Licensed Work.

**Sources:** [LICENSE5-15]()