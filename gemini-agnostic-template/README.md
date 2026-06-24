# Project-Agnostic Gemini Template

This directory contains a complete, reusable, and project-agnostic template of coding rules, playbooks, and prompt templates designed to guide AI coding assistants (like Antigravity or custom developer subagents).

It isolates general Clean Architecture rules, hand-rolled CQRS guidelines, Angular best practices, and EF migrations from any specific naming, database provider, or styling colors.

---

## Directory Structure

```
gemini-agnostic-template/
├── README.md                   # This documentation file
├── bootstrap.py                # Bootstrapping Python script
├── bootstrap.sh                # Executable wrapper shell script
├── rules/                      # Coding rules and style guides
│   ├── 01-formatting-syntax.md
│   ├── 02-clean-architecture.md
│   ├── 03-result-error-handling.md
│   ├── 04-rich-domain.md
│   ├── 05-custom-cqrs.md
│   ├── 06-relational-database.md
│   ├── 07-database-mapping.md
│   ├── 08-api-controllers-error-handling.md
│   ├── 09-dependency-injection.md
│   ├── 10-testing.md
│   ├── 11-tailwind-styling.md
│   ├── 12-background-jobs.md
│   └── 13-open-knowledge-format.md
├── skills/                     # Actionable developer playbooks (skills)
│   ├── 00-scaffold-feature-playbook/SKILL.md
│   ├── 01-create-domain-entity/SKILL.md
│   ├── 02-create-use-case/SKILL.md
│   ├── 03-add-relational-database/SKILL.md
│   ├── 04-create-infrastructure-mapping/SKILL.md
│   ├── 05-configure-dependency-injection/SKILL.md
│   ├── 06-create-api-controller/SKILL.md
│   ├── 07-create-unit-test/SKILL.md
│   ├── 08-setup-identity-and-auth/SKILL.md
│   ├── 09-frontend-framework-definitions/SKILL.md
│   ├── 10-frontend-feature-scaffolding/SKILL.md
│   ├── 11-database-migrations/SKILL.md
│   └── 12-manage-okf-documentation/SKILL.md
└── templates/                  # Prompt templates
    ├── boilerplate-prompt-template.md
    └── scafold-feature-prompt-template.md
```

---

## How to Use the Bootstrapper

The template includes an automation script (`bootstrap.sh`) to copy the templates and instantly generate concrete, project-specific rules in your target project directory by replacing the `{ProjectName}` placeholders.

### Running the Bootstrapper

Open your terminal, navigate to this directory, and execute:

```bash
./bootstrap.sh <NewProjectName> [DestinationDirectory]
```

#### Example 1: Generate files in the current folder (creates a `.gemini/` subfolder):
```bash
./bootstrap.sh StoreBackend
```

#### Example 2: Generate files directly into a new project workspace directory:
```bash
./bootstrap.sh StoreBackend /home/user/Development/StoreBackend
```

---

## Guidelines for Customization

After generating the concrete rules for a new project, it is highly recommended to customize the local `.gemini/` files to match the unique decisions of that project:

1. **Relational Database (`rules/06`, `skills/03`, `skills/11`)**: Lock in the chosen database provider (e.g. PostgreSQL, SQLite, MySQL) and remove details of unused engines.
2. **Tailwind Themes (`rules/11`, `skills/09`)**: Replace placeholders like `{AccentColor}` and `{PrimaryBgColor}` with your actual brand colors and themes defined in the code's main stylesheet.
3. **Background Processing (`rules/12`)**: Align details with whichever library you integrate (e.g., Hangfire, Quartz, or simple hosted services).
