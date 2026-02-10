# 📚 Documentation Index

**⚠️ Note:** This is an older index. For the most up-to-date navigation, see **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** in the root docs folder.

Welcome to the Market Mood Ring documentation. This directory contains comprehensive guides, technical documentation, and troubleshooting resources.

---

## 🚀 Essential Guides (Start Here!)

| Document | Description |
|----------|-------------|
| **[📖 Complete Documentation Index](DOCUMENTATION_INDEX.md)** | ⭐ **START HERE** - Navigate all 35+ docs |
| **[🚀 Getting Started](GETTING_STARTED.md)** | Complete beginner's setup guide |
| **[🔧 Troubleshooting](TROUBLESHOOTING.md)** | Master troubleshooting guide (35+ issues) |
| **[🐳 Docker vs Script Guide](DOCKER_VS_SCRIPT_GUIDE.md)** | When to use docker-compose vs startup script |
| **[🌊 Flink Job Guide](FLINK_JOB_GUIDE.md)** | Managing Flink sentiment jobs |

---

## 📁 Directory Structure

```
docs/
├── GETTING_STARTED.md         # ⭐ Complete setup guide
├── TROUBLESHOOTING.md         # ⭐ Master troubleshooting
├── DOCKER_VS_SCRIPT_GUIDE.md  # ⭐ Command reference
├── FLINK_JOB_GUIDE.md         # ⭐ Flink management
├── DOCUMENTATION_INDEX.md     # ⭐ Complete navigation
│
├── architecture/              # System architecture and design
├── phases/                    # Phase planning and migration guides
├── setup/                     # Installation and setup guides
├── technical/                 # Technical deep-dives and code explanations
├── troubleshooting/           # Common issues and solutions
└── summary/                   # Project summaries and change logs
```

---

## 🏗️ Architecture Documentation

- **[System Architecture](architecture/SYSTEM_ARCHITECTURE.md)** - Complete system overview
- **[Docker Architecture](technical/DOCKER_ARCHITECTURE.md)** - Docker images, containers, and configurations
- **[Docker Compose Architecture](technical/DOCKER_COMPOSE_ARCHITECTURE.md)** - Service orchestration and networking
- **[Python Files Architecture](technical/PYTHON_FILES_ARCHITECTURE.md)** - Python code structure and data flow
- **[Docker Compose Explained](architecture/DOCKER_COMPOSE_EXPLAINED.md)** - Docker Compose concepts
- **[Profiles Explained](architecture/PROFILES_EXPLAINED.md)** - Docker Compose profiles feature
- **[Producer Architecture](architecture/PRODUCER_ARCHITECTURE.md)** - Producer service design
- **[Technical Explanations](architecture/TECHNICAL_EXPLANATIONS.md)** - Core technical concepts

---

## 🚀 Setup Documentation

**Primary Guide:** [Getting Started](GETTING_STARTED.md) - Complete beginner's guide

**Additional Resources:**
- **[Environment Variables Guide](setup/ENV_FILE_GUIDE.md)** - Configure .env file
- **[LLM API Integration](setup/LLM_API_INTEGRATION.md)** - AI/Ollama setup
- **[Requirements by Phase](setup/REQUIREMENTS_BY_PHASE.md)** - Python package requirements
- **[Setup Workflow](setup/SETUP_WORKFLOW.md)** - Alternative setup process
- **[Phase 1 Quick Start](setup/PHASE1_QUICKSTART.md)** - Quick start guide (older, see Getting Started instead)
- **[Phase 1 Setup Complete](setup/PHASE1_SETUP_COMPLETE.md)** - Completion checklist
- **[Installation Explained](setup/INSTALLATION_EXPLAINED.md)** - Package installation details
- **[Environment Variables & Packages](setup/ENV_AND_PACKAGES.md)** - Configuration guide
- **[Path Explanation](setup/PATH_EXPLANATION.md)** - File path conventions
- **[UV Setup](setup/UV_SETUP.md)** - UV package manager setup

---

## 🔧 Technical Documentation

- **[NLTK Sentiment Analysis](technical/NLTK_SENTIMENT_ANALYSIS.md)** - How sentiment scoring works
- **[Python Files Architecture](technical/PYTHON_FILES_ARCHITECTURE.md)** - Python code structure
- **[Docker Architecture](technical/DOCKER_ARCHITECTURE.md)** - Docker images and containers
- **[Docker Compose Architecture](technical/DOCKER_COMPOSE_ARCHITECTURE.md)** - Service orchestration
- **[Ticker Optimization](technical/TICKER_OPTIMIZATION.md)** - Stock ticker selection
- **[Ticker Seed File](technical/TICKER_SEED_FILE.md)** - Ticker configuration
- **[Stock Configuration](technical/STOCK_CONFIGURATION.md)** - Stock data configuration

---

## 🐛 Troubleshooting

**Primary Guide:** [Master Troubleshooting Guide](TROUBLESHOOTING.md) - 35+ issues with solutions

**Specific Issues:**
- **[Dashboard No Data](troubleshooting/DASHBOARD_NO_DATA_TROUBLESHOOTING.md)** - Dashboard empty data issues
- **[Flink Python Fix](troubleshooting/FLINK_PYTHON_FIX.md)** - Python command not found
- **[Flink Kafka Connector Fix](troubleshooting/FLINK_KAFKA_CONNECTOR_FIX.md)** - Kafka connector missing
- **[Flink Kafka Group ID Fix](troubleshooting/FLINK_KAFKA_GROUP_ID_FIX.md)** - Group ID required error
- **[PostgreSQL Credentials Fix](troubleshooting/FIX_POSTGRES_CREDENTIALS.md)** - Database authentication
- **[Quick Fix PostgreSQL](troubleshooting/QUICK_FIX_POSTGRES.md)** - Quick database fix
- **[Port Conflict Fix](troubleshooting/PORT_CONFLICT_FIX.md)** - Port conflict resolution

---

## 📖 Quick Links

### Getting Started (Beginners)
1. **[Getting Started Guide](GETTING_STARTED.md)** - Complete step-by-step setup
2. **[Environment Setup](setup/ENV_FILE_GUIDE.md)** - Configure API keys
3. Run: `./start_data_pipeline.sh`
4. If issues: **[Troubleshooting Guide](TROUBLESHOOTING.md)**

### Understanding the System (Developers)
1. **[System Architecture](architecture/SYSTEM_ARCHITECTURE.md)** - High-level overview
2. **[Producer Architecture](architecture/PRODUCER_ARCHITECTURE.md)** - Data ingestion
3. **[Python Files Architecture](technical/PYTHON_FILES_ARCHITECTURE.md)** - Code structure
4. **[Docker Compose Explained](architecture/DOCKER_COMPOSE_EXPLAINED.md)** - Services

### Operations (DevOps)
1. **[Docker vs Script Guide](DOCKER_VS_SCRIPT_GUIDE.md)** - Command comparison
2. **[Flink Job Guide](FLINK_JOB_GUIDE.md)** - Flink management
3. **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Operations guide
4. **[Docker Compose Architecture](technical/DOCKER_COMPOSE_ARCHITECTURE.md)** - Orchestration

---

## 🎯 Documentation by Role

### For Beginners
**Start here:** [Getting Started Guide](GETTING_STARTED.md)

### For Developers
- [System Architecture](architecture/SYSTEM_ARCHITECTURE.md)
- [Python Files Architecture](technical/PYTHON_FILES_ARCHITECTURE.md)
- [Producer Architecture](architecture/PRODUCER_ARCHITECTURE.md)
- [Docker Architecture](technical/DOCKER_ARCHITECTURE.md)

### For DevOps Engineers
- [Docker vs Script Guide](DOCKER_VS_SCRIPT_GUIDE.md)
- [Docker Compose Architecture](technical/DOCKER_COMPOSE_ARCHITECTURE.md)
- [Profiles Explained](architecture/PROFILES_EXPLAINED.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

### For Data Engineers
- [System Architecture](architecture/SYSTEM_ARCHITECTURE.md)
- [Producer Architecture](architecture/PRODUCER_ARCHITECTURE.md)
- [NLTK Sentiment Analysis](technical/NLTK_SENTIMENT_ANALYSIS.md)
- [Python Files Architecture](technical/PYTHON_FILES_ARCHITECTURE.md)

---

## 📋 Summary Documentation

- **[Final Documentation Verification](summary/FINAL_DOCUMENTATION_VERIFICATION.md)** - Latest status
- **[Deployment Summary](summary/DEPLOYMENT_SUMMARY.md)** - Deployment guide
- **[Review Summary](summary/REVIEW_SUMMARY.md)** - Project review notes

---

## 📝 Contributing

When adding new documentation:
1. Place files in appropriate subdirectories
2. Update [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) with links
3. Follow existing documentation style
4. Include code examples and diagrams where helpful

---

## 🔗 External Resources

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Apache Flink Documentation](https://flink.apache.org/docs/)
- [PostgreSQL pgvector](https://github.com/pgvector/pgvector)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Finnhub API](https://finnhub.io/docs/api)
- [NLTK Documentation](https://www.nltk.org/)
- [Vader Sentiment](https://github.com/cjhutto/vaderSentiment)

---

*Last Updated: February 2026*  
*For complete navigation, see [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)*