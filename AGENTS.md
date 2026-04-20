# Agents Configuration for Mistral Vibe

## Available Agents

### Kent - TDD Implementation Expert
- **Role**: Test-Driven Development implementation
- **Usage**: `/agent kent` or `@kent`
- **Specialty**: Red-Green-Refactor cycle, Tidy First principles
- **Rules**: `.opencode/agents/kent.md`

### Alexia - Autonomous Analyst
- **Role**: Autonomous problem analysis and decision making
- **Usage**: `/agent alexia`
- **Specialty**: End-to-end problem solving without human intervention
- **Rules**: `.opencode/agents/alexia.md`

### Claire - Coordination Specialist
- **Role**: Workflow coordination and process management
- **Usage**: `/agent claire`
- **Specialty**: Multi-agent coordination and task orchestration

### Iris - Quality Assurance
- **Role**: Code review and quality control
- **Usage**: `/agent iris`
- **Specialty**: Functional and technical reviews

### Martin - Documentation Expert
- **Role**: Documentation generation and knowledge management
- **Usage**: `/agent martin`
- **Specialty**: Technical writing and documentation standards

## Modern Workflow (Rules-Based)

### 1. Issue Analysis
```bash
/agent alexia
# Analyze the issue and create initial plan
/aidd:03:plan [issue_number]
/aidd:03:challenge
```

### 2. Implementation (TDD)
```bash
/agent kent
/aidd:04:implement
# Follow Kent's TDD cycle:
# 1. Write failing test
# 2. Implement minimal code
# 3. Refactor (Tidy First)
```

### 3. Quality Assurance
```bash
/agent iris
/aidd:05:review_functional
/aidd:05:review_code
```

### 4. Security & Audit
```bash
/aidd:09:audit
/aidd:09:security_refactor
```

### 5. Project Status & Validation
```bash
/custom:07:project_status
# Includes test validation and quality metrics
```

### 6. Issue Closing
```bash
/custom:08:close_issue
# Mandatory: Never close issues manually
```

### 7. Finalization
```bash
/aidd:08:commit
/custom:08:end_plan
/custom:08:changelog
```

## Rules System

### Key Rules Locations
- **Audit**: `.opencode/rules/00-architecture/`
- **Standards**: `.opencode/rules/01-standards/`
- **Security**: `.opencode/rules/custom/08-issue-closing.md`
- **Quality**: `.opencode/rules/05-testing/`

### Rule Application
- Rules are automatically enforced during workflow execution
- Agents apply relevant rules based on context
- Custom rules override default behavior

## Memory & Artifacts
- **Task Memory**: `aidd_docs/memory/internal/`
- **Audit Reports**: `aidd_docs/tasks/audits/`
- **Status Reports**: `aidd_docs/tasks/status/`
- **Templates**: `aidd_docs/templates/`

## Configuration Files
- **Main Config**: `opencode.json`
- **Mistral Vibe**: `mistral_vibe_config.json`
- **Agent Definitions**: `.opencode/agents/*.md`

## Usage Examples

### Starting a new feature
```bash
/agent alexia
# Describe the feature requirements
/agent kent
# Implement using TDD approach
```

### Running audits
```bash
/aidd:09:audit full_codebase
/aidd:09:security_refactor
```

### Weekly maintenance
```bash
/custom:07:project_status
# Review generated report in aidd_docs/tasks/status/
```