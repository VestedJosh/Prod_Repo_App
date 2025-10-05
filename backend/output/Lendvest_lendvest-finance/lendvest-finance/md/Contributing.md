## Development Setup

The LVLidoVault project uses Foundry as its primary development framework. Before contributing, ensure you have completed the development environment setup as described in [Development Environment]().

The project structure follows Foundry conventions with smart contracts in `src/`, tests in `test/`, and deployment scripts in `script/`. The `.gitignore` file excludes standard Foundry build artifacts including `cache/`, `out/`, and broadcast logs for development networks.

**Sources:** [.gitignore1-16]()

## Code Standards and Formatting

All Solidity code must be formatted using `forge fmt` before submission. The CI pipeline enforces this requirement and will fail builds that contain improperly formatted code.

### Formatting Requirements

| Tool | Command | Purpose |
| --- | --- | --- |
| `forge fmt` | Format Solidity code | Ensures consistent code style |
| `forge fmt --check` | Validate formatting | Used in CI to reject improperly formatted code |

The formatting check is performed as part of the automated CI pipeline and must pass before any pull request can be merged.

**Sources:** [.github/workflows/test.yml32-35]()

## Testing Requirements

All contributions must include appropriate tests and pass the existing test suite. The project uses Foundry's testing framework with verbose output enabled in CI.

For detailed information about the test suite structure and how to run tests locally, see [Testing](). At minimum, your contribution must:

* Pass all existing tests: `forge test -vvv`
* Include tests for any new functionality
* Maintain or improve test coverage

**Sources:** [.github/workflows/test.yml42-45]()

## Contribution Workflow

The following diagram illustrates the standard development workflow for contributing to the LVLidoVault project:

### Development Contribution Process

### Key Development Commands

| Stage | Command | Purpose |
| --- | --- | --- |
| Format | `forge fmt` | Apply consistent code formatting |
| Build | `forge build --sizes` | Compile contracts and show size information |
| Test | `forge test -vvv` | Run test suite with verbose output |
| Version Check | `forge --version` | Verify Foundry installation |

**Sources:** [.github/workflows/test.yml28-45]()

## Continuous Integration Pipeline

The project uses GitHub Actions for automated testing and validation. Every pull request triggers the CI pipeline which must pass before merging.

### CI Pipeline Architecture

### CI Environment Configuration

The CI pipeline uses specific environment variables and configurations:

| Configuration | Value | Purpose |
| --- | --- | --- |
| `FOUNDRY_PROFILE` | `ci` | Uses CI-specific Foundry settings |
| Foundry Version | `nightly` | Uses latest nightly build for newest features |
| Checkout | `submodules: recursive` | Ensures all dependencies are fetched |

The pipeline runs on every push and pull request, as well as manual workflow dispatch.

**Sources:** [.github/workflows/test.yml1-46]()

## Licensing Considerations

The LVLidoVault project is licensed under the Business Source License 1.1 (BSL 1.1). Contributors must understand the licensing implications:

### License Terms Summary

| Aspect | Requirement |
| --- | --- |
| **Permitted Use** | Copy, modify, create derivative works, redistribute, non-production use |
| **Production Restrictions** | Commercial production use requires license purchase |
| **Change Date** | License converts to open source on specified Change Date |
| **Attribution** | License must be conspicuously displayed on all copies |
| **Copyright** | Copyright (C) 2025 Lendvest |

### Key Licensing Requirements

* All contributions become subject to the BSL 1.1 license
* The license text must be preserved in all copies and derivative works
* Commercial production use is restricted until the Change Date
* The license will convert to GPL 2.0 or compatible license on the Change Date

By contributing to this project, you agree that your contributions will be licensed under the same BSL 1.1 terms.

**Sources:** [LICENSE1-39]()

## Review Process

All contributions undergo code review before merging. The review process focuses on:

### Technical Review Criteria

| Category | Requirements |
| --- | --- |
| **Code Quality** | Follows Solidity best practices and project conventions |
| **Testing** | Comprehensive test coverage for new functionality |
| **Documentation** | Code is properly documented and self-explanatory |
| **Security** | No obvious security vulnerabilities or attack vectors |
| **Integration** | Changes integrate properly with existing system architecture |

### Automated Checks

Before human review, all contributions must pass:

1. **Formatting Check**: `forge fmt --check` must pass
2. **Compilation**: `forge build --sizes` must succeed
3. **Test Suite**: `forge test -vvv` must pass all tests
4. **Submodule Integrity**: All git submodules must be properly referenced

Pull requests failing any automated check will be automatically rejected and require fixes before review.

**Sources:** [.github/workflows/test.yml12-46]()

## Submission Guidelines

### Pull Request Requirements

* **Title**: Clear, descriptive title explaining the change
* **Description**: Detailed explanation of what was changed and why
* **Testing**: Description of how the change was tested
* **Breaking Changes**: Clear documentation if the change breaks compatibility

### Branch Naming Conventions

Use descriptive branch names that indicate the type and scope of changes:

* `feature/description` - New functionality
* `fix/description` - Bug fixes
* `docs/description` - Documentation updates
* `refactor/description` - Code refactoring without functional changes

### Commit Message Standards

Write clear, concise commit messages that explain the purpose of each change. Follow conventional commit format where appropriate.

**Sources:** [.gitignore1-16]() [.github/workflows/test.yml1-46]()

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

* [Contributing]()
* [Development Setup]()
* [Code Standards and Formatting]()
* [Formatting Requirements]()
* [Testing Requirements]()
* [Contribution Workflow]()
* [Development Contribution Process]()
* [Key Development Commands]()
* [Continuous Integration Pipeline]()
* [CI Pipeline Architecture]()
* [CI Environment Configuration]()
* [Licensing Considerations]()
* [License Terms Summary]()
* [Key Licensing Requirements]()
* [Review Process]()
* [Technical Review Criteria]()
* [Automated Checks]()
* [Submission Guidelines]()
* [Pull Request Requirements]()
* [Branch Naming Conventions]()
* [Commit Message Standards]()