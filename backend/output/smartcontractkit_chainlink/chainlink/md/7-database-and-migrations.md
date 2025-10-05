The database architecture consists of several key components that provide abstraction and type safety for database operations.

Sources: [core/web/external\_initiators\_controller.go1-119]() [core/web/bridge\_types\_controller.go1-234]()

ORM Pattern and Data Access
---------------------------

The Chainlink codebase implements an Object-Relational Mapping (ORM) pattern to provide a clean abstraction layer between the application logic and database operations.

**ORM Interface Pattern**

The system uses interface-based ORM design where controllers depend on `bridges.ORM` interface rather than concrete implementations. This provides testability and separation of concerns.

| ORM Method | Purpose | Controller Usage |
| --- | --- | --- |
| `CreateBridgeType(ctx, bt)` | Create new bridge type | [core/web/bridge\_types\_controller.go84]() |
| `FindBridge(ctx, taskType)` | Find bridge by name | [core/web/bridge\_types\_controller.go136]() |
| `UpdateBridgeType(ctx, bt, btr)` | Update existing bridge | [core/web/bridge\_types\_controller.go180]() |
| `DeleteBridgeType(ctx, bt)` | Delete bridge type | [core/web/bridge\_types\_controller.go225]() |
| `CreateExternalInitiator(ctx, ei)` | Create external initiator | [core/web/external\_initiators\_controller.go87]() |
| `FindExternalInitiatorByName(ctx, name)` | Find external initiator | [core/web/external\_initiators\_controller.go106]() |
| `DeleteExternalInitiator(ctx, name)` | Delete external initiator | [core/web/external\_initiators\_controller.go111]() |

Sources: [core/web/bridge\_types\_controller.go79-87]() [core/web/external\_initiators\_controller.go52-58]()

Database Error Handling
-----------------------

The system implements comprehensive error handling for database operations, including SQL-specific error detection and user-friendly error reporting.

**Error Handling Patterns**

The controllers implement specific error handling patterns for different database error conditions:

* **Record Not Found**: `sql.ErrNoRows` is detected and converted to HTTP 404
* **Constraint Violations**: PostgreSQL constraint errors are converted to HTTP 409 Conflict
* **Validation Errors**: Input validation failures result in HTTP 400 Bad Request
* **Generic SQL Errors**: Unexpected database errors return HTTP 500 Internal Server Error

**Example Error Handling Implementation**:

Sources: [core/web/bridge\_types\_controller.go137-144]() [core/web/external\_initiators\_controller.go107-110]() [core/web/bridge\_types\_controller.go88-98]()

Data Validation and Business Logic
----------------------------------

The system implements comprehensive data validation before database operations to ensure data integrity and provide meaningful error messages.

**Bridge Type Validation**

| Validation Rule | Implementation | Error Message |
| --- | --- | --- |
| Name Required | `len(bt.Name.String()) < 1` | "No name specified" |
| Name Format | `bridges.ParseBridgeName()` | Task type validation error |
| URL Required | `len(strings.TrimSpace(u)) == 0` | "URL must be present" |
| Payment Positive | `bt.MinimumContractPayment.Cmp(assets.NewLinkFromJuels(0)) < 0` | "MinimumContractPayment must be positive" |
| Unique Name | `orm.FindBridge(ctx, bt.Name)` | "Bridge Type X already exists" |

**External Initiator Validation**

| Validation Rule | Implementation | Error Message |
| --- | --- | --- |
| Name Required | `len([]rune(exi.Name)) == 0` | "No name specified" |
| Name Format | `externalInitiatorNameRegexp.MatchString()` | "Name must be alphanumeric and may contain '\_' or '-'" |
| Unique Name | `orm.FindExternalInitiatorByName()` | "Name X already exists" |

Sources: [core/web/bridge\_types\_controller.go37-54]() [core/web/external\_initiators\_controller.go27-43]()

Testing Infrastructure
----------------------

The Chainlink testing infrastructure provides comprehensive database testing capabilities with dedicated test database management.

**Test Database Management**

The testing infrastructure uses `pgtest.NewSqlxDB(t)` to create isolated test database instances for each test, ensuring test independence and preventing data contamination between tests.

**Testing Patterns**:

* **Parallel Test Execution**: Tests use `t.Parallel()` for concurrent execution
* **Context Management**: Tests use `testutils.Context(t)` for proper context handling
* **Resource Cleanup**: Automatic cleanup with `t.Cleanup(cleanup)` functions
* **Assertion Helpers**: Custom assertion helpers like `cltest.AssertServerResponse()`

Sources: [core/web/external\_initiators\_controller\_test.go27-28]() [core/web/bridge\_types\_controller\_test.go117-119]() [core/web/external\_initiators\_controller\_test.go67-74]()

Database Transaction Flow
-------------------------

The following diagram illustrates the typical flow of database operations from HTTP request to database persistence:

**Transaction Characteristics**:

* **Context Propagation**: All database operations receive `context.Context` for cancellation and timeout handling
* **Error Handling**: Comprehensive error detection and appropriate HTTP status code mapping
* **Audit Logging**: Successful operations are logged to audit trail for security and compliance
* **JSON API Responses**: Standardized JSON API format for all responses

Sources: [core/web/bridge\_types\_controller.go62-110]() [core/web/external\_initiators\_controller.go62-100]()