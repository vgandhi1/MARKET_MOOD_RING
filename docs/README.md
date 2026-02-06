# 📚 Documentation Index

Welcome to the Market Mood Ring documentation. This directory contains comprehensive guides, technical documentation, and troubleshooting resources.

## 📁 Directory Structure

```
docs/
├── architecture/          # System architecture and design
├── phases/               # Phase planning and migration guides
├── setup/                # Installation and setup guides
├── technical/            # Technical deep-dives and code explanations
├── troubleshooting/      # Common issues and solutions
└── summary/             # Project summaries and change logs
```

---

## 🏗️ Architecture Documentation

- **[Docker Architecture](technical/DOCKER_ARCHITECTURE.md)** - Docker images, containers, and configurations
- **[Docker Compose Architecture](technical/DOCKER_COMPOSE_ARCHITECTURE.md)** - Service orchestration and networking
- **[Python Files Architecture](technical/PYTHON_FILES_ARCHITECTURE.md)** - Python code structure and data flow
- **[Docker Compose Explained](architecture/DOCKER_COMPOSE_EXPLAINED.md)** - Docker Compose concepts
- **[Profiles Explained](architecture/PROFILES_EXPLAINED.md)** - Docker Compose profiles feature
- **[Producer Architecture](architecture/PRODUCER_ARCHITECTURE.md)** - Producer service design
- **[Technical Explanations](architecture/TECHNICAL_EXPLANATIONS.md)** - Core technical concepts

---

## 📋 Phase Documentation

- **[Phase Planning](phases/PHASE_PLANNING.md)** - 3-phase development approach
  - Phase 1: ETL Pipeline (No LLM/Ollama)
  - Phase 2: LLM Integration
  - Phase 3: Ollama Integration

---

## 🚀 Setup Documentation

- **[Setup Workflow](setup/SETUP_WORKFLOW.md)** - Complete setup process
- **[Requirements by Phase](setup/REQUIREMENTS_BY_PHASE.md)** - 📦 **NEW** Python package requirements for each phase
- **[LLM API Integration](setup/LLM_API_INTEGRATION.md)** - 🤖 **NEW** Guide for integrating LLM APIs (OpenAI, Anthropic, etc.)
- **[UV Setup](setup/UV_SETUP.md)** - UV package manager setup
- **[Installation Explained](setup/INSTALLATION_EXPLAINED.md)** - Package installation details
- **[Environment Variables & Packages](setup/ENV_AND_PACKAGES.md)** - Configuration guide
- **[Path Explanation](setup/PATH_EXPLANATION.md)** - File path conventions
- **[Phase 1 Quick Start](setup/PHASE1_QUICKSTART.md)** - Quick start guide for Phase 1
- **[Phase 1 Setup Complete](setup/PHASE1_SETUP_COMPLETE.md)** - Phase 1 completion checklist

---

## 🔧 Technical Documentation

- **[Python Files Architecture](technical/PYTHON_FILES_ARCHITECTURE.md)** - Python code structure
- **[Docker Architecture](technical/DOCKER_ARCHITECTURE.md)** - Docker images and containers
- **[Docker Compose Architecture](technical/DOCKER_COMPOSE_ARCHITECTURE.md)** - Service orchestration
- **[NLTK Sentiment Analysis](technical/NLTK_SENTIMENT_ANALYSIS.md)** - 📊 **NEW** NLTK Vader overview and usage
- **[Ticker Optimization](technical/TICKER_OPTIMIZATION.md)** - Stock ticker selection
- **[Ticker Seed File](technical/TICKER_SEED_FILE.md)** - Ticker configuration
- **[Stock Configuration](technical/STOCK_CONFIGURATION.md)** - Stock data configuration

---

## 🐛 Troubleshooting

- **[Dashboard No Data](troubleshooting/DASHBOARD_NO_DATA_TROUBLESHOOTING.md)** - Dashboard empty data issues
- **[Flink Python Fix](troubleshooting/FLINK_PYTHON_FIX.md)** - Python command not found
- **[Flink Kafka Connector Fix](troubleshooting/FLINK_KAFKA_CONNECTOR_FIX.md)** - Kafka connector missing
- **[Flink Kafka Group ID Fix](troubleshooting/FLINK_KAFKA_GROUP_ID_FIX.md)** - Group ID required error
- **[PostgreSQL Credentials Fix](troubleshooting/FIX_POSTGRES_CREDENTIALS.md)** - Database authentication
- **[Quick Fix PostgreSQL](troubleshooting/QUICK_FIX_POSTGRES.md)** - Quick database fix
- **[Port Conflict Fix](troubleshooting/PORT_CONFLICT_FIX.md)** - Port 8501 conflict resolution

---

## 📖 Quick Links

### Getting Started
1. Read [Phase Planning](phases/PHASE_PLANNING.md) to understand the 3-phase approach
2. Follow [Setup Workflow](setup/SETUP_WORKFLOW.md) for initial setup
3. Use [Phase 1 Quick Start](setup/PHASE1_QUICKSTART.md) for Phase 1 deployment

### Understanding the System
1. Review [Python Files Architecture](technical/PYTHON_FILES_ARCHITECTURE.md) for code structure
2. Study [Docker Architecture](technical/DOCKER_ARCHITECTURE.md) for container setup
3. Explore [Docker Compose Architecture](technical/DOCKER_COMPOSE_ARCHITECTURE.md) for orchestration

### Troubleshooting
1. Check [Dashboard No Data](troubleshooting/DASHBOARD_NO_DATA_TROUBLESHOOTING.md) if dashboard is empty
2. Review [Flink Python Fix](troubleshooting/FLINK_PYTHON_FIX.md) for Flink job issues
3. See [PostgreSQL Credentials Fix](troubleshooting/FIX_POSTGRES_CREDENTIALS.md) for database issues

---

## 🎯 Documentation by Role

### For Developers
- [Python Files Architecture](technical/PYTHON_FILES_ARCHITECTURE.md)
- [Docker Architecture](technical/DOCKER_ARCHITECTURE.md)
- [Docker Compose Architecture](technical/DOCKER_COMPOSE_ARCHITECTURE.md)

### For DevOps Engineers
- [Docker Compose Architecture](technical/DOCKER_COMPOSE_ARCHITECTURE.md)
- [Docker Architecture](technical/DOCKER_ARCHITECTURE.md)
- [Profiles Explained](architecture/PROFILES_EXPLAINED.md)

### For Data Engineers
- [Python Files Architecture](technical/PYTHON_FILES_ARCHITECTURE.md)
- [Producer Architecture](architecture/PRODUCER_ARCHITECTURE.md)
- [Phase Planning](phases/PHASE_PLANNING.md)

### For Users
- [Phase 1 Quick Start](setup/PHASE1_QUICKSTART.md)
- [Setup Workflow](setup/SETUP_WORKFLOW.md)
- [Troubleshooting Guides](troubleshooting/)

---

## 📝 Contributing

When adding new documentation:
1. Place files in appropriate subdirectories
2. Update this README with links
3. Follow existing documentation style
4. Include code examples and diagrams where helpful

---

## 📋 Summary Documentation

- **[Changes Summary](summary/CHANGES_SUMMARY.md)** - Project change log
- **[Complete Changes Summary](summary/COMPLETE_CHANGES_SUMMARY.md)** - Detailed change history
- **[Deployment Summary](summary/DEPLOYMENT_SUMMARY.md)** - Deployment guide
- **[Review Summary](summary/REVIEW_SUMMARY.md)** - Project review notes

---

## 🔗 External Resources

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Apache Flink Documentation](https://flink.apache.org/docs/)
- [PostgreSQL pgvector](https://github.com/pgvector/pgvector)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Finnhub API](https://finnhub.io/docs/api)
- [NLTK Documentation](https://www.nltk.org/)
- [Vader Sentiment](https://github.com/cjhutto/vaderSentiment)