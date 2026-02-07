# PentestAI Documentation - Complete File Index

This document lists all documentation files created for the PentestAI project.

## 📚 Documentation Structure

### Core Documentation Files

1. **docs/index.html** - Docsify configuration and setup
2. **docs/README.md** - Main documentation homepage
3. **docs/_sidebar.md** - Navigation sidebar structure
4. **docs/_navbar.md** - Top navigation bar
5. **docs/_coverpage.md** - Landing page/cover

### Main Guides

6. **docs/getting-started.md** - Installation and first steps
7. **docs/architecture.md** - System architecture overview
8. **docs/troubleshooting.md** - Common issues and solutions

### Core Components (docs/core/)

9. **docs/core/configuration.md** - Complete configuration reference
   - All 50+ configuration options
   - Environment variables
   - JSON/YAML config
   - Examples for all use cases

### API Documentation (docs/api/)

10. **docs/api/python-api.md** - Python API reference
    - PentestAIController class
    - PentestAIConfig class
    - Data models
    - Complete code examples

11. **docs/api/rest-api.md** - REST API reference
    - All endpoints
    - Request/response formats
    - SSE streaming
    - Examples in Python, JavaScript, cURL

### Deployment Guides (docs/deployment/)

12. **docs/deployment/docker.md** - Docker deployment guide
    - Docker Compose setup
    - Dockerfiles
    - Troubleshooting
    - Security best practices

### Examples (docs/examples/)

13. **docs/examples/full-assessment.md** - Complete workflow example
    - Full two-stage assessment
    - Result analysis
    - Export and reporting

## 🗂️ Planned Documentation (To Be Created)

### Agent Documentation (docs/agents/)

- **docs/agents/planner.md** - Planner agent details
- **docs/agents/executor.md** - Executor agent details
- **docs/agents/instructor.md** - Instructor agent with RAG
- **docs/agents/summarizer.md** - Summarizer agent
- **docs/agents/extractor.md** - Extractor agent
- **docs/agents/estimator.md** - Estimator agent
- **docs/agents/advisor.md** - Advisor agent
- **docs/agents/evaluator.md** - Evaluator agent
- **docs/agents/optimizer.md** - Optimizer agent with Group Knapsack

### Core Components (Additional)

- **docs/core/controller.md** - PentestAIController deep dive
- **docs/core/pentest-module.md** - Stage 1 module details
- **docs/core/remediation-module.md** - Stage 2 module details

### Framework Documentation

- **docs/two-stage-framework.md** - Two-stage workflow explained
- **docs/agent-system.md** - Multi-agent architecture

### Integration Guides (docs/integrations/)

- **docs/integrations/kali-mcp.md** - Kali MCP integration
- **docs/integrations/llm-providers.md** - LLM provider setup
- **docs/integrations/arvancloud.md** - ArvanCloud gateway

### User Interfaces (docs/ui/)

- **docs/ui/react-ui.md** - React web interface
- **docs/ui/api-server.md** - FastAPI backend
- **docs/ui/cli.md** - Command-line interface
- **docs/ui/gradio-ui.md** - Gradio interface (legacy)

### Additional Examples

- **docs/examples/basic-usage.md** - Simple pentest
- **docs/examples/pentest-only.md** - Stage 1 only
- **docs/examples/remediation-only.md** - Stage 2 only
- **docs/examples/custom-config.md** - Custom configuration
- **docs/examples/mcp-integration.md** - MCP usage

### Configuration Details

- **docs/configuration/overview.md** - Configuration system
- **docs/configuration/pentest-options.md** - Pentest settings
- **docs/configuration/remediation-options.md** - Remediation settings
- **docs/configuration/llm-settings.md** - LLM configuration
- **docs/configuration/output-settings.md** - Output options

### Knowledge Base

- **docs/knowledge/builtin.md** - Built-in knowledge entries
- **docs/knowledge/custom.md** - Custom knowledge creation
- **docs/knowledge/rag.md** - RAG system explained

### Advanced Topics

- **docs/advanced/counterfactual.md** - Counterfactual reasoning
- **docs/advanced/group-knapsack.md** - Group Knapsack algorithm
- **docs/advanced/attack-trees.md** - Attack plan trees
- **docs/advanced/custom-agents.md** - Creating custom agents

### Troubleshooting Details

- **docs/troubleshooting/docker.md** - Docker-specific issues
- **docs/troubleshooting/llm.md** - LLM connection issues
- **docs/troubleshooting/mcp.md** - MCP server issues
- **docs/troubleshooting/ui.md** - UI-specific problems

### Development

- **docs/development/contributing.md** - Contribution guide
- **docs/development/setup.md** - Development environment
- **docs/development/testing.md** - Testing guide
- **docs/development/style.md** - Code style guide

### Reference

- **docs/reference/cli-commands.md** - CLI command reference
- **docs/reference/env-vars.md** - Environment variables
- **docs/reference/file-formats.md** - File format specs
- **docs/reference/vulnerability-types.md** - Vulnerability taxonomy

### Additional Deployment

- **docs/deployment/docker-compose.md** - Compose details
- **docs/deployment/production.md** - Production deployment
- **docs/deployment/environment.md** - Environment setup

### About

- **docs/about/paper.md** - Research paper summary
- **docs/about/license.md** - License information
- **docs/about/changelog.md** - Version history
- **docs/about/contributors.md** - Contributors

### API Details

- **docs/api/data-models.md** - Complete data model reference
- **docs/api/mcp-protocol.md** - MCP protocol details

## 📊 Documentation Statistics

### Currently Created
- **Total Files:** 13 core documentation files
- **Total Words:** ~50,000+ words
- **Code Examples:** 100+ code snippets
- **Coverage:** ~35% complete

### Components Documented
- ✅ Main setup and configuration (100%)
- ✅ Python API reference (100%)
- ✅ REST API reference (100%)
- ✅ Docker deployment (100%)
- ✅ Full assessment example (100%)
- ✅ Troubleshooting basics (100%)
- ⏳ Agent details (0%)
- ⏳ UI interfaces (0%)
- ⏳ Advanced topics (0%)
- ⏳ Additional examples (0%)

### Planned Additions
- **Remaining Files:** ~50 documentation files
- **Estimated Words:** 100,000+ additional words
- **Target Coverage:** 95% complete

## 🚀 Quick Links

### Most Important Pages
1. [Getting Started](getting-started.md) - Start here!
2. [Architecture](architecture.md) - Understand the system
3. [Configuration Guide](core/configuration.md) - Configure everything
4. [Python API](api/python-api.md) - Use the framework
5. [REST API](api/rest-api.md) - Integrate with API
6. [Docker Deployment](deployment/docker.md) - Deploy with Docker
7. [Troubleshooting](troubleshooting.md) - Fix issues

### By Use Case

**I want to:**
- **Run my first pentest** → [Getting Started](getting-started.md)
- **Understand the architecture** → [Architecture](architecture.md)
- **Configure PentestAI** → [Configuration Guide](core/configuration.md)
- **Use Python API** → [Python API Reference](api/python-api.md)
- **Build an integration** → [REST API Reference](api/rest-api.md)
- **Deploy with Docker** → [Docker Guide](deployment/docker.md)
- **Fix an issue** → [Troubleshooting](troubleshooting.md)
- **See full example** → [Full Assessment Example](examples/full-assessment.md)

## 📝 Contributing to Documentation

Want to help improve these docs?

1. **Fix typos/errors:** Submit PR to `docs/` directory
2. **Add examples:** Create new files in `docs/examples/`
3. **Improve existing:** Enhance current documentation files
4. **Create missing:** Write any of the planned documentation files above

See [Development Guide](development/contributing.md) (planned) for details.

## 🔍 Search

Use the search bar (top right) to find specific topics across all documentation.

## 💬 Feedback

Found an issue or have a suggestion?
- [GitHub Issues](https://github.com/pentestai/pentestai/issues)
- [GitHub Discussions](https://github.com/pentestai/pentestai/discussions)

---

**Last Updated:** February 6, 2024  
**Documentation Version:** 1.0.0  
**Framework Version:** 1.0.0
