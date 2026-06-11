# AI-Driven Development & Automation Tools (`my-tools`)

Welcome to the **AI-Driven Development & Automation Tools** repository. This project serves as a centralized toolkit for automated agentic software engineering, specifically tailored for building, testing, and managing high-performance full-stack applications with C#/.NET Clean Architecture and Angular frontends, integrated directly with GitHub Projects v2 boards.

---

## 📁 Repository Directory Structure

```text
my-tools/
├── .gemini/
│   ├── rules/       # Architectural and formatting standards for code generation
│   ├── skills/      # Execution playbooks for AI coding tasks
│   └── templates/   # Standardized prompt templates for development scaffolding
├── agents/
│   ├── dotnet-clean-architect/    # Scaffolds new solutions dynamically
│   ├── github-backlog-reader/     # Reads tasks and orchestrates board status lifecycle
│   └── senior-fullstack-engineer/  # Implements features across all architectural layers
├── scripts/
│   ├── create_pr.py               # Automates creation of GitHub Pull Requests
│   ├── fetch_backlog.py           # Retrieves tasks and status mappings from GitHub Projects v2
│   └── update_project_item.py     # Updates status options of items on GitHub Project boards
└── plugin.json                     # Plugin definition for Custom Agents
```

---

## 🤖 Custom Agents

This repository defines three specialized autonomous subagents under the `agents` folder, registered via [plugin.json](plugin.json):

1. **[dotnet-clean-architect](./agents/dotnet-clean-architect/agent.json)**:
   * **Purpose**: Instantiates fully structured, clean, and building .NET Web API solutions following the Clean Architecture pattern.
   * **Key Tasks**: Prompts the user for project names, database providers (PostgreSQL, SQL Server, MySQL, SQLite, Oracle), connection strings, and directory paths for rules/skills before scaffolding the projects and linking them to a `.sln` or `.slnx` file.

2. **[github-backlog-reader](./agents/github-backlog-reader/agent.json)**:
   * **Purpose**: Connects to a GitHub Project v2 board, reads issues in the backlog/todo column, and coordinates feature branches, code implementation, test execution, PR creation, and branch cleanup.
   * **Execution Lifecycle**: Follows a strict 12-step automated pipeline from branch checkout to final merge branch cleanup.

3. **[senior-fullstack-engineer](./agents/senior-fullstack-engineer/agent.json)**:
   * **Purpose**: A top-tier developer subagent capable of implementing, refactoring, and optimizing backend code (.NET) and frontend code (Angular) while enforcing strict SOLID, DDD, and Clean Architecture patterns.

---

## 🐍 Helper Automation Scripts

The `scripts` directory contains Python automation scripts for GitHub API integration. They use Application Default Credentials (ADC) or token authentication from the target project `.env` file:

* **[scripts/fetch_backlog.py](./scripts/fetch_backlog.py)**:
  Fetches project board status configurations, option IDs, and next recommended tasks under the 'Backlog' or 'Todo' status via GitHub's GraphQL API.
  ```bash
  python3 scripts/fetch_backlog.py <github_owner> <project_number> <base_code_path>
  ```

* **[scripts/update_project_item.py](./scripts/update_project_item.py)**:
  Updates single-select fields (like the Status of an issue card) on a GitHub Project v2 board.
  ```bash
  python3 scripts/update_project_item.py <projectId> <itemId> <fieldId> <optionId> <base_code_path>
  ```

  * **[scripts/create_pr.py](./scripts/create_pr.py)**:
  Automates the generation of a pull request from a feature branch to the target base branch on GitHub.
  ```bash
  python3 scripts/create_pr.py <owner> <repo> <title> <head_branch> <base_code_path> [base_branch] [body]
  ```

---

## 📑 Gemini Configurations (`.gemini/`)

### 📘 Architecture Rules (`.gemini/rules/`)
Contains 10 guidelines that outline design principles for high-quality .NET and Angular development:
* **[01-formatting-syntax.md](./.gemini/rules/01-formatting-syntax.md)**: Formatting, naming conventions, and syntax rules.
* **[02-clean-architecture.md](./.gemini/rules/02-clean-architecture.md)**: Layer dependency flows and structure (Domain, Application, Infrastructure, Presentation, Shared).
* **[03-result-error-handling.md](./.gemini/rules/03-result-error-handling.md)**: Standardizing flow control with `Result` types instead of throwing exceptions.
* **[04-rich-domain.md](./.gemini/rules/04-rich-domain.md)**: Encapsulated domain entities utilizing private constructors, static factory methods, and UUID v7.
* **[05-custom-cqrs.md](./.gemini/rules/05-custom-cqrs.md)**: Explicit command and query separations without heavy middleware dependencies.
* **[06-relational-database.md](./.gemini/rules/06-relational-database.md)**: Database configurations, abstractions, and transaction boundaries.
* **[07-database-mapping.md](./.gemini/rules/07-database-mapping.md)**: Entity Framework Core mappings (avoiding data annotations, utilizing Fluent API).
* **[08-api-controllers-error-handling.md](./.gemini/rules/08-api-controllers-error-handling.md)**: Exposing REST endpoints and centralizing API exception filters.
* **[09-dependency-injection.md](./.gemini/rules/09-dependency-injection.md)**: Correct registration configurations for services and interfaces.
* **[10-testing.md](./.gemini/rules/10-testing.md)**: Guidelines for writing unit tests with `xUnit` and `Moq`.

### 🛠️ Execution Skills (`.gemini/skills/`)
Playbooks defining exact step-by-step instructions for coding operations:
* **[00-scaffold-feature-playbook](./.gemini/skills/00-scaffold-feature-playbook.md)**: Outlines high-level workflow orchestration for scaffolding any full-stack feature.
* **[01-create-domain-entity](./.gemini/skills/01-create-domain-entity.md)**: Detailed steps to write rich domain entities.
* **[02-create-use-case](./.gemini/skills/02-create-use-case.md)**: How to write command/query handlers and validators.
* **[03-add-relational-database](./.gemini/skills/03-add-relational-database.md)**: Setting up entity DB configurations and executing migrations.
* **[04-create-infrastructure-mapping](./.gemini/skills/04-create-infrastructure-mapping.md)**: Creating custom EF Core entity type configurations.
* **[05-configure-dependency-injection](./.gemini/skills/05-configure-dependency-injection.md)**: Registering application handlers and services.
* **[06-create-api-controller](./.gemini/skills/06-create-api-controller.md)**: Developing REST API endpoints that return standard HTTP responses.
* **[07-create-unit-test](./.gemini/skills/07-create-unit-test.md)**: Constructing testing setups.
* **[08-setup-identity-and-auth](./.gemini/skills/08-setup-identity-and-auth.md)**: Adding JWT-based token authorization security.
* **[09-angular-frontend-framework-definitions](./.gemini/skills/09-angular-frontend-framework-definitions.md)**: Structuring TypeScript services, guards, and styling rules.

### 📝 Prompt Templates (`.gemini/templates/`)
* **[boilerplate-prompt-template.md](./.gemini/templates/boilerplate-prompt-template.md)**: Prompt layout used to direct the `dotnet-clean-architect` agent.
* **[scafold-feature-prompt-template.md](./.gemini/templates/scafold-feature-prompt-template.md)**: Template for initiating full-stack feature implementations.

---

## 🚀 Getting Started

### 1. Environment Configurations
The Python scripts require a valid GitHub Personal Access Token (PAT) with read/write access to project boards and pull requests.
Save it in a `.env` file at the root of the project directory:
```env
GITHUB_TOKEN=your_personal_access_token_here
```

### 2. Loading Custom Agents
Ensure the parent folder containing `plugin.json` is registered in your IDE or CLI agent configurations to unlock the subagents (`dotnet-clean-architect`, `github-backlog-reader`, `senior-fullstack-engineer`) during your coding assistant interactions.
