# AI-Driven Development & Automation Tools (`my-tools`)

Welcome to the **AI-Driven Development & Automation Tools** repository. This project serves as a centralized toolkit for automated agentic software engineering, specifically tailored for building, testing, and managing high-performance full-stack applications with C#/.NET Clean Architecture and Angular frontends, integrated directly with GitHub Projects v2 boards.

---

## 📁 Repository Directory Structure

```text
my-tools/
├── agents/
│   ├── documentation-architect/    # Scans codebase and generates UML & C4 diagrams
│   ├── dotnet-clean-architect/     # Scaffolds new solutions dynamically
│   ├── github-backlog-reader/      # Reads tasks and orchestrates board status lifecycle
│   └── senior-fullstack-engineer/   # Implements features across all architectural layers
├── gemini-agnostic-template/       # Project-agnostic template for rules and skills with bootstrapping
│   ├── rules/
│   ├── skills/
│   └── templates/
├── scripts/
│   ├── create_pr.py                # Automates creation of GitHub Pull Requests
│   ├── fetch_backlog.py            # Retrieves tasks and status mappings from GitHub Projects v2
│   └── update_project_item.py      # Updates status options of items on GitHub Project boards
├── skills/
│   └── architecture-documentation/  # Skill playbook for diagramming and architecture documentation
├── plugin.json                     # Plugin definition for Custom Agents
└── README.md                       # Repository documentation
```

---

## 🤖 Custom Agents

This repository defines four specialized autonomous subagents under the `agents` folder, registered via [plugin.json](plugin.json):

1. **[documentation-architect](./agents/documentation-architect/agent.json)**:
   * **Purpose**: Scans the codebase to generate structured architecture documentation, UML diagrams, and C4 Model diagrams using Mermaid.js with structured descriptions.
   * **Execution**: Suggests a root-level `docs/` folder with organized subfolders for structural, behavioral, and architectural diagrams.

2. **[dotnet-clean-architect](./agents/dotnet-clean-architect/agent.json)**:
   * **Purpose**: Instantiates fully structured, clean, and building .NET Web API solutions following the Clean Architecture pattern.
   * **Key Tasks**: Scaffolds projects and links them to `.sln` or `.slnx` files after collecting configuration inputs (name, database provider, paths for rules/skills).

3. **[github-backlog-reader](./agents/github-backlog-reader/agent.json)**:
   * **Purpose**: Connects to a GitHub Project v2 board, reads backlog/todo tasks, and automates a 12-step pipeline from branch creation to final PR merge.

4. **[senior-fullstack-engineer](./agents/senior-fullstack-engineer/agent.json)**:
   * **Purpose**: Enforces strict SOLID, DDD, and Clean Architecture patterns while implementing, refactoring, and optimizing backend (.NET) and frontend (Angular) features.

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
 
## 🌀 Project-Agnostic Gemini Template (`gemini-agnostic-template/`)
 
The [gemini-agnostic-template](./gemini-agnostic-template/) directory contains a complete, reusable, and project-agnostic configuration of coding rules, execution playbooks (skills), and prompt templates. It isolates general architectural rules (Clean Architecture, CQRS, Angular best practices) from any project-specific names or database engines.
 
### 📘 Architecture Rules (`rules/`)
Contains 12 guidelines that outline design principles for high-quality .NET and Angular development:
* **[01-formatting-syntax.md](./gemini-agnostic-template/rules/01-formatting-syntax.md)**: Formatting, naming conventions, and syntax rules.
* **[02-clean-architecture.md](./gemini-agnostic-template/rules/02-clean-architecture.md)**: Layer dependency flows and structure (Domain, Application, Infrastructure, Presentation, Shared).
* **[03-result-error-handling.md](./gemini-agnostic-template/rules/03-result-error-handling.md)**: Standardizing flow control with `Result` types instead of throwing exceptions.
* **[04-rich-domain.md](./gemini-agnostic-template/rules/04-rich-domain.md)**: Encapsulated domain entities utilizing private constructors, static factory methods, and UUID v7.
* **[05-custom-cqrs.md](./gemini-agnostic-template/rules/05-custom-cqrs.md)**: Explicit command and query separations without heavy middleware dependencies.
* **[06-relational-database.md](./gemini-agnostic-template/rules/06-relational-database.md)**: Database configurations, abstractions, and transaction boundaries.
* **[07-database-mapping.md](./gemini-agnostic-template/rules/07-database-mapping.md)**: Entity Framework Core mappings (avoiding data annotations, utilizing Fluent API).
* **[08-api-controllers-error-handling.md](./gemini-agnostic-template/rules/08-api-controllers-error-handling.md)**: Exposing REST endpoints and centralizing API exception filters.
* **[09-dependency-injection.md](./gemini-agnostic-template/rules/09-dependency-injection.md)**: Correct registration configurations for services and interfaces.
* **[10-testing.md](./gemini-agnostic-template/rules/10-testing.md)**: Guidelines for writing unit tests with `xUnit` and `Moq`.
* **[11-tailwind-styling.md](./gemini-agnostic-template/rules/11-tailwind-styling.md)**: Styling guidelines and rules when using TailwindCSS.
* **[12-background-jobs.md](./gemini-agnostic-template/rules/12-background-jobs.md)**: Instructions and architectural patterns for implementing background processing.
 
### 🛠️ Execution Skills (`skills/`)
Playbooks defining exact step-by-step instructions for coding operations:
* **[00-scaffold-feature-playbook](./gemini-agnostic-template/skills/00-scaffold-feature-playbook/SKILL.md)**: Outlines high-level workflow orchestration for scaffolding any full-stack feature.
* **[01-create-domain-entity](./gemini-agnostic-template/skills/01-create-domain-entity/SKILL.md)**: Detailed steps to write rich domain entities.
* **[02-create-use-case](./gemini-agnostic-template/skills/02-create-use-case/SKILL.md)**: How to write command/query handlers and validators.
* **[03-add-relational-database](./gemini-agnostic-template/skills/03-add-relational-database/SKILL.md)**: Setting up entity DB configurations and executing migrations.
* **[04-create-infrastructure-mapping](./gemini-agnostic-template/skills/04-create-infrastructure-mapping/SKILL.md)**: Creating custom EF Core entity type configurations.
* **[05-configure-dependency-injection](./gemini-agnostic-template/skills/05-configure-dependency-injection/SKILL.md)**: Registering application handlers and services.
* **[06-create-api-controller](./gemini-agnostic-template/skills/06-create-api-controller/SKILL.md)**: Developing REST API endpoints that return standard HTTP responses.
* **[07-create-unit-test](./gemini-agnostic-template/skills/07-create-unit-test/SKILL.md)**: Constructing testing setups.
* **[08-setup-identity-and-auth](./gemini-agnostic-template/skills/08-setup-identity-and-auth/SKILL.md)**: Adding JWT-based token authorization security.
* **[09-frontend-framework-definitions](./gemini-agnostic-template/skills/09-frontend-framework-definitions/SKILL.md)**: Enforcing layout, routing, components, and Angular modules standards.
* **[10-frontend-feature-scaffolding](./gemini-agnostic-template/skills/10-frontend-feature-scaffolding/SKILL.md)**: Playbook for scaffolding frontend services and components.
* **[11-database-migrations](./gemini-agnostic-template/skills/11-database-migrations/SKILL.md)**: Safe database migration creation and execution workflows.
 
### 📝 Prompt Templates (`templates/`)
* **[boilerplate-prompt-template.md](./gemini-agnostic-template/templates/boilerplate-prompt-template.md)**: Prompt layout used to direct the `dotnet-clean-architect` agent.
* **[scafold-feature-prompt-template.md](./gemini-agnostic-template/templates/scafold-feature-prompt-template.md)**: Template for initiating full-stack feature implementations.
 
### 🚀 Bootstrapping New Projects
 
The template includes a bootstrapping script to copy the templates and instantly generate concrete, project-specific rules in your target project directory by replacing the `{ProjectName}` placeholders.
 
To bootstrap a new project:
1. Navigate to the template directory:
   ```bash
   cd gemini-agnostic-template
   ```
2. Run the bootstrap script:
   ```bash
   ./bootstrap.sh <NewProjectName> [DestinationDirectory]
   ```
   * *Example 1 (Generate in the current directory as a `.gemini/` subfolder)*:
     ```bash
     ./bootstrap.sh StoreBackend
     ```
   * *Example 2 (Generate directly into a new workspace)*:
     ```bash
     ./bootstrap.sh StoreBackend /path/to/StoreBackend
     ```
 
For more details on custom configurations and guidelines for customization, see the [gemini-agnostic-template/README.md](./gemini-agnostic-template/README.md).
 
---
 
## 🛠️ Exposed Repository Skills
 
This repository exposes custom execution skills defined under the [skills](./skills/) folder:
* **[architecture-documentation](./skills/architecture-documentation/SKILL.md)**: Guided playbook for scanning codebases and generating structured UML and C4 diagrams in Mermaid.js.
 
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
