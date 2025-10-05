* [core/services/pipeline/helpers\_test.go]()
* [core/services/pipeline/keypath.go]()
* [core/services/pipeline/keypath\_test.go]()
* [core/services/pipeline/models.go]()
* [core/services/pipeline/models\_test.go]()
* [core/services/pipeline/orm.go]()
* [core/services/pipeline/orm\_test.go]()
* [core/services/pipeline/runner.go]()
* [core/services/pipeline/runner\_test.go]()
* [core/services/pipeline/scheduler.go]()
* [core/services/pipeline/scheduler\_test.go]()
* [core/services/pipeline/task.base.go]()
* [core/services/pipeline/task.bridge.go]()
* [core/services/pipeline/task.bridge\_test.go]()
* [core/services/pipeline/task.http.go]()
* [core/services/pipeline/task.http\_test.go]()
* [core/services/pipeline/task.jsonparse.go]()
* [core/services/pipeline/task.jsonparse\_test.go]()
* [core/services/pipeline/task.median.go]()
* [core/services/pipeline/task.median\_test.go]()
* [core/services/pipeline/task.merge.go]()
* [core/services/pipeline/task.merge\_test.go]()
* [core/services/pipeline/task.multiply.go]()
* [core/services/pipeline/task.multiply\_test.go]()
* [core/services/pipeline/task\_params.go]()
* [core/services/pipeline/task\_params\_test.go]()
* [core/services/pipeline/variables.go]()
* [core/services/pipeline/variables\_test.go]()

The Pipeline System is a core component of Chainlink nodes that provides a flexible framework for defining, executing, and monitoring data processing workflows. It enables construction of directed acyclic graphs (DAGs) of tasks to fetch, transform, and deliver data on and off-chain.

This document explains the architecture and functionality of the Pipeline System. For information about specific job types that use pipelines, see [Job System](). For information about workflow implementation, see [Workflow System]().

## Architecture Overview

The Pipeline System allows node operators to define execution graphs composed of interconnected tasks. Each pipeline is represented as a directed acyclic graph (DAG) where nodes are tasks and edges represent data flow dependencies between them.

Sources: [core/services/pipeline/graph.go15-164]() [core/services/pipeline/runner.go33-48]() [core/services/pipeline/orm.go77-102]()

### Key Components

1. **Pipeline**: A directed acyclic graph of tasks that defines a workflow.
2. **Tasks**: Individual units of work that perform specific operations (HTTP requests, data parsing, mathematical operations, blockchain interactions, etc.)
3. **Runner**: Executes pipelines by orchestrating task execution based on their dependencies.
4. **Scheduler**: Manages the execution order of tasks within a pipeline run, tracking dependencies and collecting results.
5. **ORM**: Handles persistence of pipeline specifications, runs, and task results.

## Pipeline Definition

Pipelines are defined using a DOT-like syntax which specifies tasks and their connections.

Sources: [core/services/pipeline/graph.go211-286]()

### DOT Syntax Example

Here's an example of a pipeline definition:

```
// Fetch price data
ds1 [type=bridge name="coinmarketcap" requestData=<{"data":{"coin":"ETH","market":"USD"}}>]
ds1_parse [type=jsonparse path="data,result"]
ds1_multiply [type=multiply times=1000000000000000000]

// Fetch another price source
ds2 [type=http method=GET url="https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"]
ds2_parse [type=jsonparse path="ethereum,usd"]
ds2_multiply [type=multiply times=1000000000000000000]

// Connect the tasks
ds1 -> ds1_parse -> ds1_multiply -> median;
ds2 -> ds2_parse -> ds2_multiply -> median;

// Calculate median and prepare final answer
median [type=median index=0]
```

Sources: [core/services/pipeline/common.go23-46]() [core/services/pipeline/graph\_test.go15-118]()

### Implicit Dependencies

The pipeline parser automatically detects implicit dependencies between tasks by analyzing variable references and adds edges accordingly. For example, if a task references the output of another task with `$(task_name)`, an implicit dependency edge is added even if not explicitly defined.

Sources: [core/services/pipeline/graph.go54-97]()

## Pipeline Execution

The execution of a pipeline is managed by the `Runner` and `Scheduler` components. The Runner is responsible for initializing and executing the pipeline, while the Scheduler manages the execution of individual tasks based on their dependencies.

Sources: [core/services/pipeline/runner.go293-538]() [core/services/pipeline/scheduler.go15-173]()

### Run Lifecycle

1. **Initialization**: The pipeline is parsed and initialized with task-specific configurations.
2. **Execution**: Tasks are executed in dependency order, with results passed to dependent tasks.
3. **Result Collection**: Results from terminal tasks (tasks with no outputs) are collected as final outputs.
4. **Persistence**: The run and task results are stored in the database.

Sources: [core/services/pipeline/runner.go617-731]() [core/services/pipeline/orm.go439-513]()

### Asynchronous Tasks and Resumption

The Pipeline System supports asynchronous tasks, which can suspend execution and resume later when results become available. This is particularly useful for tasks that may take a long time to complete or require external callbacks.

Sources: [core/services/pipeline/runner.go733-756]() [core/services/pipeline/task.bridge.go256-267]()

## Task Types

The Pipeline System includes a wide variety of built-in task types to handle different operations:

| Task Type | Description | Example Use Case |
| --- | --- | --- |
| HTTP | Makes HTTP requests to external APIs | Fetching price data from a public API |
| Bridge | Calls external adapters via bridges | Interacting with a custom data source |
| JSONParse | Parses JSON data using path expressions | Extracting specific fields from API responses |
| Median | Calculates median of inputs | Aggregating price data from multiple sources |
| Multiply | Multiplies numeric values | Converting price units (e.g., USD to Wei) |
| ETHTx | Sends Ethereum transactions | Submitting price updates on-chain |
| ETHCall | Makes read-only calls to Ethereum contracts | Reading contract state |
| CBOR | Parses CBOR-encoded data | Working with CBOR data from smart contracts |
| Conditional | Evaluates boolean conditions | Implementing branching logic |

Sources: [core/services/pipeline/common.go302-343]() [core/services/pipeline/task.http.go15-131]() [core/services/pipeline/task.bridge.go55-293]() [core/services/pipeline/task.jsonparse.go15-177]()

### Task Execution Model

Each task implements the `Task` interface, which defines methods for execution and dependency management:

Sources: [core/services/pipeline/common.go50-65]() [core/services/pipeline/task.base.go12-29]()

## Data Flow and Variable Resolution

Data flows through the pipeline via task inputs and outputs. The system supports variable referencing, allowing tasks to access outputs from other tasks or external variables.

### Variable Resolution

Tasks can reference:

1. **Task outputs**: Using the syntax `$(task_dot_id)` or `$(task_dot_id.path)` for nested values
2. **External variables**: Passed to the pipeline at execution time

Sources: [core/services/pipeline/common.go102-125]() [core/services/pipeline/runner.go380-536]()

## Error Handling and Retries

The Pipeline System provides robust error handling capabilities, including:

1. **Task-level error handling**: Tasks can be configured to fail early or continue execution despite errors.
2. **Automatic retries**: Tasks can be configured with retry parameters (attempts, backoff).
3. **Comprehensive error reporting**: All errors are collected and reported in the final results.

Sources: [core/services/pipeline/scheduler.go174-270]() [core/services/pipeline/task.base.go44-151]()

## Persistence

The Pipeline System persists pipeline specifications, runs, and task results in the database via the ORM.

Sources: [core/services/pipeline/orm.go187-222]() [core/services/pipeline/orm.go317-364]() [core/services/pipeline/orm.go439-459]()

### Run Cleanup and Pruning

The Pipeline System includes a run reaper that periodically cleans up old runs to prevent database growth. The pruning behavior can be configured via the `MaxSuccessfulRuns` parameter.

Sources: [core/services/pipeline/orm.go516-556]() [core/services/pipeline/orm.go690-770]()

## Integration with External Adapters

One of the most powerful features of the Pipeline System is its ability to integrate with external adapters via Bridge tasks.

Sources: [core/services/pipeline/task.bridge.go98-293]()

### Bridge Task Caching

Bridge tasks support caching of responses, allowing for fallback to cached values when external adapters are unavailable. This enhances system reliability and reduces unnecessary external requests.

Sources: [core/services/pipeline/task.bridge.go233-254]() [core/services/pipeline/task.bridge.go270-275]()

## Performance Monitoring

The Pipeline System includes built-in metrics for monitoring performance:

1. **Task execution time**: Tracks the execution time of each task.
2. **Run completion time**: Measures the total time to complete a pipeline run.
3. **Error counts**: Counts errors by pipeline and task type.
4. **Bridge metrics**: Special metrics for bridge task performance.

Sources: [core/services/pipeline/runner.go82-108]() [core/services/pipeline/task.bridge.go28-52]()

## Conclusion

The Pipeline System is a flexible and powerful framework for defining and executing data processing workflows in Chainlink nodes. It provides a rich set of built-in task types, robust error handling, and integration capabilities with external systems. By composing tasks into directed acyclic graphs, complex data processing pipelines can be created to fetch, transform, and deliver data on and off-chain.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Pipeline System]()
* [Architecture Overview]()
* [Key Components]()
* [Pipeline Definition]()
* [DOT Syntax Example]()
* [Implicit Dependencies]()
* [Pipeline Execution]()
* [Run Lifecycle]()
* [Asynchronous Tasks and Resumption]()
* [Task Types]()
* [Task Execution Model]()
* [Data Flow and Variable Resolution]()
* [Variable Resolution]()
* [Error Handling and Retries]()
* [Persistence]()
* [Run Cleanup and Pruning]()
* [Integration with External Adapters]()
* [Bridge Task Caching]()
* [Performance Monitoring]()
* [Conclusion]()