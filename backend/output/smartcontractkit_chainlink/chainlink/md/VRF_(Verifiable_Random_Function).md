* [core/utils/http/http.go]()
* [core/utils/http/http\_allowed\_ips.go]()
* [core/utils/http/http\_allowed\_ips\_test.go]()

This document provides technical information about Chainlink's Verifiable Random Function (VRF) implementation. VRF provides cryptographically secure random numbers for smart contracts, with on-chain verification of randomness. For information about general blockchain integration, see [Blockchain Integration]().

## Overview

Chainlink VRF is a provably-fair and verifiable source of randomness designed for smart contracts. The VRF system consists of on-chain contracts (VRF Coordinator) and off-chain Chainlink node services that work together to fulfill randomness requests.

The core functionality allows:

* Smart contracts to request random values
* Chainlink nodes to generate random values with cryptographic proofs
* On-chain verification of the random values

The Chainlink node maintains a VRF service that monitors the blockchain for randomness requests, generates provably-random values using cryptographic keys, and submits them back to the blockchain.

Sources:
[core/services/vrf/delegate.go35-62]()

## Architecture

The VRF system integrates with Chainlink's job management system through the `vrf.Delegate` which implements the `job.Delegate` interface.

### VRF Delegate Service Creation

### Components

The VRF implementation consists of the following key components:

1. **vrf.Delegate**: Implements `job.Delegate` interface and serves as a factory for VRF services based on pipeline task detection
2. **Service Selection Logic**: Determines which VRF service to create based on pipeline tasks:
   * `pipeline.VRFTaskV2Plus` → V2Plus service with `CoordinatorV2_5`
   * `pipeline.VRFTaskV2` → V2 service with `CoordinatorV2`
   * `pipeline.VRFTask` → V1 listener with basic coordinator
3. **Validation Functions**: `CheckFromAddressesExist()` and `CheckFromAddressMaxGasPrices()` ensure proper key and gas configuration
4. **Feed Integration**: V2/V2Plus services integrate with price feed aggregators for LINK/ETH or LINK/NATIVE exchange rates

Sources:
[core/services/vrf/delegate.go73-279]()
[core/services/vrf/delegate.go281-322]()

## VRF Versions

The `vrf.Delegate` creates different services based on pipeline task detection in the job specification.

### VRF V1 (`pipeline.VRFTask`)

Created when the pipeline contains a `pipeline.VRFTask`. Returns a `v1.Listener` service.

* Uses `solidity_vrf_coordinator_interface.VRFCoordinator` wrapper
* Basic request-response pattern through pipeline execution
* Integrates with mailbox system for request queuing

### VRF V2 (`pipeline.VRFTaskV2`)

Created when the pipeline contains a `pipeline.VRFTaskV2`. Returns a `v2.New()` service.

* Uses `vrf_coordinator_v2.VRFCoordinatorV2` wrapper
* Retrieves `LINKETHFEED` address from coordinator for price feeds
* Creates `aggregator_v3_interface.AggregatorV3Interface` for ETH/LINK price data
* Supports `batch_vrf_coordinator_v2.BatchVRFCoordinatorV2` for batch processing
* Optional `vrf_owner.VRFOwner` integration for advanced management

### VRF V2 Plus (`pipeline.VRFTaskV2Plus`)

Created when the pipeline contains a `pipeline.VRFTaskV2Plus`. Returns a `v2.New()` service.

* Uses `vrf_coordinator_v2_5.VRFCoordinatorV25` wrapper
* Retrieves `LINKNATIVEFEED` address from coordinator for native token pricing
* Creates `aggregator_v3_interface.AggregatorV3Interface` for LINK/NATIVE price data
* **Restrictions**: VRF Owner not supported, Custom Reverts Pipeline not supported
* Enhanced with native token payment capabilities

### Service Creation Flow

Sources:
[core/services/vrf/delegate.go141-279]()
[core/services/vrf/delegate.go165-177]()
[core/services/vrf/delegate.go218-228]()

## Request-Response Flow

The VRF system follows this flow when processing randomness requests:

1. **Request Detection**:

   * VRF service monitors the blockchain via LogBroadcaster
   * On new randomness request logs, the appropriate handler is triggered
2. **Request Validation**:

   * Checks if the request is already fulfilled
   * Validates request parameters (e.g., payment amount)
   * Prevents duplicate processing with LogDeduper
3. **Randomness Generation**:

   * Generates a random value using cryptographic VRF keys
   * Creates a proof that can be verified on-chain
4. **Fulfillment Submission**:

   * Builds transaction with proof
   * Uses TransmitChecker to confirm fulfillment is needed
   * Submits fulfillment transaction via TxManager
5. **Confirmation Monitoring**:

   * Tracks confirmation status of fulfillment transactions
   * Handles resubmissions if necessary

Sources:
[core/services/vrf/delegate\_test.go194-242]()
[core/services/vrf/v1/listener.go]()

## Address and Gas Price Validation

The VRF delegate includes validation functions to ensure proper configuration before service creation.

### Address Validation

The `CheckFromAddressesExist()` function validates that all addresses in `jb.VRFSpec.FromAddresses` exist in the keystore:

* Iterates through `jb.VRFSpec.FromAddresses`
* Calls `gethks.Get(ctx, a.Hex())` for each address
* Returns aggregated errors using `multierr.Append()`

### Gas Price Validation

Two validation functions ensure consistent gas price configuration:

#### `CheckFromAddressMaxGasPrices()`

Validates that key-specific max gas prices match the job's `gasLanePrice`:

* Only validates if `jb.VRFSpec.GasLanePrice != nil`
* Compares `keySpecificMaxGas(address)` with `jb.VRFSpec.GasLanePrice`
* Returns error for mismatched addresses

#### `FromAddressMaxGasPricesAllEqual()`

Ensures all from addresses have the same key-specific max gas price:

* Compares each address's max gas price with the first address
* Required for V2/V2Plus services before creation

### Validation in Service Creation

Both V2 and V2Plus service creation include these validation steps:

1. `CheckFromAddressesExist(ctx, jb, d.ks.Eth())`
2. `FromAddressMaxGasPricesAllEqual(jb, chain.Config().EVM().GasEstimator().PriceMaxKey)`
3. `CheckFromAddressMaxGasPrices(jb, chain.Config().EVM().GasEstimator().PriceMaxKey)`

Sources:
[core/services/vrf/delegate.go281-322]()
[core/services/vrf/delegate\_test.go478-630]()

## Feed Price Integration

VRF V2 and V2Plus services integrate with Chainlink price feeds to determine gas costs and payments.

### Feed Address Retrieval

Both V2 services retrieve feed addresses from their respective coordinators:

**V2 Service (`LINKETHFEED`)**:

**V2Plus Service (`LINKNATIVEFEED`)**:

### Aggregator Interface Creation

Both services create `aggregator_v3_interface.AggregatorV3Interface` instances:

The aggregator is passed to the `v2.New()` service constructor for price calculations during VRF fulfillment.

### Retry Logic

Feed address retrieval includes retry logic with:

* 10 attempts maximum
* 500ms delay between attempts
* Handles temporary RPC endpoint failures

This ensures the VRF service can switch to alternative RPC endpoints if needed during initialization.

Sources:
[core/services/vrf/delegate.go164-176]()
[core/services/vrf/delegate.go217-228]()

## VRF Job Configuration

VRF jobs are configured with specialized parameters and include validation during service creation.

### Configuration Parameters

### VRF V2Plus Restrictions

The delegate enforces specific restrictions for V2Plus jobs:

### Batch Coordinator Support

Optional batch processing through `BatchCoordinatorAddress`:

### Configuration Validation

The delegate validates configuration before service creation:

* All `fromAddresses` must exist in the keystore
* All `fromAddresses` must have equal key-specific max gas prices
* `gasLanePrice` must match key-specific max gas prices (if specified)
* VRF Owner not allowed for V2Plus configurations

Sources:
[core/services/vrf/delegate.go154-159]()
[core/services/vrf/delegate.go114-120]()
[core/services/vrf/delegate\_test.go689-721]()

## Common Patterns and Best Practices

1. **Confirmation Settings**:

   * Set appropriate `minIncomingConfirmations` for your security needs
   * Higher values increase security but delay fulfillment
2. **Gas Management**:

   * Configure `gasLanePrice` according to network conditions
   * Ensure ETH keys have sufficient funds for gas payments
3. **Request Tracking**:

   * VRF services automatically track and deduplicate requests
   * Uses the `LogDeduper` to prevent duplicate fulfillments
4. **Batch Processing**:

   * V2 supports batch fulfillment for better gas efficiency
   * Configured via `BatchCoordinatorAddress` in job spec
5. **Reorg Protection**:

   * VRF system includes protection against blockchain reorganizations
   * Prevents double-fulfillment of requests

Sources:
[core/services/vrf/delegate\_test.go196-242]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [VRF (Verifiable Random Function)]()
* [Overview]()
* [Architecture]()
* [VRF Delegate Service Creation]()
* [Components]()
* [VRF Versions]()
* [VRF V1 (`pipeline.VRFTask`)]()
* [VRF V2 (`pipeline.VRFTaskV2`)]()
* [VRF V2 Plus (`pipeline.VRFTaskV2Plus`)]()
* [Service Creation Flow]()
* [Request-Response Flow]()
* [Address and Gas Price Validation]()
* [Address Validation]()
* [Gas Price Validation]()
* [`CheckFromAddressMaxGasPrices()`]()
* [`FromAddressMaxGasPricesAllEqual()`]()
* [Validation in Service Creation]()
* [Feed Price Integration]()
* [Feed Address Retrieval]()
* [Aggregator Interface Creation]()
* [Retry Logic]()
* [VRF Job Configuration]()
* [Configuration Parameters]()
* [VRF V2Plus Restrictions]()
* [Batch Coordinator Support]()
* [Configuration Validation]()
* [Common Patterns and Best Practices]()