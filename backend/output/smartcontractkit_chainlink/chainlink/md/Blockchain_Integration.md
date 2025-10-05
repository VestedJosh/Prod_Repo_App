* [core/services/job/orm.go]()
* [core/services/job/runner\_integration\_test.go]()
* [core/services/job/spawner\_test.go]()
* [core/services/ocr2/delegate.go]()
* [core/services/pipeline/mocks/config.go]()
* [core/services/pipeline/mocks/orm.go]()
* [core/services/pipeline/mocks/pipeline\_param\_unmarshaler.go]()
* [core/services/pipeline/mocks/runner.go]()
* [core/services/relay/evm/evm.go]()
* [core/testdata/testspecs/v2\_specs.go]()
* [core/web/jobs\_controller.go]()
* [core/web/jobs\_controller\_test.go]()
* [core/web/pipeline\_runs\_controller.go]()
* [core/web/pipeline\_runs\_controller\_test.go]()
* [core/web/presenters/job.go]()
* [core/web/presenters/job\_test.go]()
* [core/web/resolver/spec.go]()
* [core/web/resolver/spec\_test.go]()
* [core/web/schema/type/spec.graphql]()

This document covers Chainlink's blockchain integration capabilities, including multi-chain support, relayer architecture, job-based blockchain interactions, and smart contract integration. The system provides a unified interface for interacting with multiple blockchain networks through an abstraction layer that handles chain-specific details.

For information about job management and execution, see [Job System](). For details about configuration of specific chains, see [Chain and Plugin Configuration]().

## Multi-Chain Architecture

Chainlink supports multiple blockchain networks through a relayer-based architecture that abstracts chain-specific implementations behind common interfaces. The system distinguishes between EVM-compatible chains and non-EVM chains, with specialized handling for each category.

### Core Relayer System

The `RelayerFactory` creates chain-specific relayers based on configuration. Each relayer implements the `loop.Relayer` interface, providing a consistent API across different blockchain networks.

**Sources:** [core/services/chainlink/application.go300-356]() [core/services/chainlink/application.go329-351]()

### EVM Chain Support

EVM chains receive specialized treatment due to their widespread adoption and shared architecture. The system supports multiple EVM networks including Ethereum mainnet, Layer 2 solutions, and sidechains.

**Sources:** [core/services/chainlink/application.go311-327]() [core/services/relay/evm/evm.go199-228]()

## Job-Based Blockchain Integration

Chainlink's blockchain interactions are primarily orchestrated through a job system where different job types handle specific blockchain operations. Each job type has specialized logic for interacting with smart contracts and processing blockchain events.

### Job Type Mapping

Most job types that interact with smart contracts require an `EVMChainID` to be specified, linking the job to a specific blockchain network.

**Sources:** [core/services/job/orm.go186-508]() [core/services/job/models.go78-138]()

### Job Delegate System

Each job type has a corresponding delegate that implements the `job.Delegate` interface. These delegates are responsible for creating and managing the services needed to execute jobs on specific blockchain networks.

**Sources:** [core/services/chainlink/application.go499-677]() [core/services/ocr2/delegate.go237-261]()

## EVM Relayer Architecture

The EVM relayer provides the primary integration point for Ethereum and EVM-compatible chains. It implements providers for different use cases and manages blockchain-specific operations.

### EVM Relayer Components

**Sources:** [core/services/relay/evm/evm.go141-228]() [core/services/relay/evm/evm.go369-402]()

### Contract Interaction Patterns

**Sources:** [core/services/relay/evm/evm.go369-402]() [core/services/ocr2/delegate.go417-539]()

## Smart Contract Integration

The system provides comprehensive smart contract integration through generated Go wrappers, ABI handling, and event processing capabilities.

### Contract Wrapper Generation

The codebase includes extensive generated Go contract wrappers that provide type-safe interfaces to smart contracts. These wrappers handle ABI encoding/decoding and provide structured access to contract methods and events.

**Sources:** [core/services/relay/evm/evm.go66-86]() [core/services/relay/evm/evm.go72-85]()

### Transaction Lifecycle

**Sources:** [core/services/ocr2/delegate.go540-586]() [core/services/job/orm.go644-695]()

## Key Configuration Requirements

Blockchain integration requires proper configuration of chain-specific parameters and key management:

| Configuration Aspect | EVM Chains | Non-EVM Chains | Required Fields |
| --- | --- | --- | --- |
| **Chain Identification** | `EVMChainID` | `RelayID` | Chain-specific ID |
| **Key Management** | `TransmitterAddress` | `TransmitterID` | Signing key reference |
| **Network Configuration** | RPC endpoints, confirmations | Chain-specific params | Network connectivity |
| **Gas Configuration** | Gas price, gas limit | Fee configuration | Transaction cost management |
| **Contract Addresses** | Contract addresses | Program IDs/addresses | Target contract specification |

**Sources:** [core/services/job/orm.go186-508]() [core/services/job/models.go275-365]()

The blockchain integration system provides a comprehensive framework for multi-chain operations while maintaining type safety and proper abstraction between different blockchain networks. Job-specific delegates handle the coordination between the core Chainlink functionality and blockchain-specific requirements.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Blockchain Integration]()
* [Multi-Chain Architecture]()
* [Core Relayer System]()
* [EVM Chain Support]()
* [Job-Based Blockchain Integration]()
* [Job Type Mapping]()
* [Job Delegate System]()
* [EVM Relayer Architecture]()
* [EVM Relayer Components]()
* [Contract Interaction Patterns]()
* [Smart Contract Integration]()
* [Contract Wrapper Generation]()
* [Transaction Lifecycle]()
* [Key Configuration Requirements]()