# Documentation index

**Start here** — navigates the consolidated Market Mood Ring docs (~25 active guides; legacy paths redirect here).

---

## Essential (read first)

| Document | Purpose |
|----------|---------|
| [Main README](../README.md) | Overview, quick start, architecture summary |
| [Getting Started](GETTING_STARTED.md) | Full setup walkthrough |
| [Troubleshooting](TROUBLESHOOTING.md) | Master runbook (startup, DB, dashboard, producers) |
| [Environment guide](setup/ENV_FILE_GUIDE.md) | `.env`, packages, container paths |
| [Docker vs script](DOCKER_VS_SCRIPT_GUIDE.md) | `./start_data_pipeline.sh` vs `docker-compose` |
| [Flink job guide](FLINK_JOB_GUIDE.md) | Submit, monitor, cancel sentiment job |
| [Flink fixes](troubleshooting/FLINK_FIXES.md) | Connector JARs, Python symlink, Kafka group.id |

---

## Architecture

| Document | Purpose |
|----------|---------|
| [System architecture](architecture/SYSTEM_ARCHITECTURE.md) | End-to-end pipeline design |
| [Docker & Compose](architecture/DOCKER.md) | Services, KRaft Kafka, images, profiles |
| [Producer architecture](architecture/PRODUCER_ARCHITECTURE.md) | Ingestion and RAG |
| [Profiles explained](architecture/PROFILES_EXPLAINED.md) | `producers` profile behavior |
| [Technical explanations](architecture/TECHNICAL_EXPLANATIONS.md) | pgvector, docker exec vs compose run |
| [Why Docker installs packages](architecture/WHY_DOCKER_INSTALLS_PACKAGES.md) | Build-time dependencies |

---

## Setup & configuration

| Document | Purpose |
|----------|---------|
| [LLM integration](setup/LLM_API_INTEGRATION.md) | Ollama (host) and cloud LLMs |
| [Requirements by phase](setup/REQUIREMENTS_BY_PHASE.md) | Python dependency matrix |
| [Installation explained](setup/INSTALLATION_EXPLAINED.md) | Where packages install in images |
| [UV setup](setup/UV_SETUP.md) | Optional local package manager |

*Deprecated setup paths (`PHASE1_QUICKSTART`, `SETUP_WORKFLOW`, etc.) redirect to Getting Started.*

---

## Technical reference

| Document | Purpose |
|----------|---------|
| [Python files](technical/PYTHON_FILES_ARCHITECTURE.md) | Code layout and data flow |
| [NLTK sentiment](technical/NLTK_SENTIMENT_ANALYSIS.md) | VADER scoring in Flink |
| [Stock & tickers](technical/STOCK_CONFIGURATION.md) | Symbols, `tickers.json`, rate limits |

---

## Troubleshooting (specific)

| Document | Purpose |
|----------|---------|
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | **Primary** — most issues |
| [FLINK_FIXES.md](troubleshooting/FLINK_FIXES.md) | Flink build/runtime |
| [Port conflicts](troubleshooting/PORT_CONFLICT_FIX.md) | Port already in use |

*Older fix docs (`FIX_POSTGRES_*`, `DASHBOARD_NO_DATA_*`, `FLINK_KAFKA_*`) redirect to the guides above.*

---

## Summaries & status

| Document | Purpose |
|----------|---------|
| [Deployment summary](summary/DEPLOYMENT_SUMMARY.md) | Ops cheat sheet |
| [FINAL_DOCUMENTATION_STATUS](../FINAL_DOCUMENTATION_STATUS.md) | Doc completion / naming reference |

---

## By role

| Role | Path |
|------|------|
| **Beginner** | README → Getting Started → ENV_FILE_GUIDE → Troubleshooting |
| **Developer** | System Architecture → Producer Architecture → Python Files → NLTK |
| **DevOps** | Docker → Docker vs Script → Troubleshooting |
| **ML / AI** | LLM Integration → NLTK → `dashboard/app.py`, `rag_ingest.py` |

---

## Live presentation

Leadership slides: [manage/presentation.html](../manage/presentation.html) · [GitHub Pages](https://vgandhi1.github.io/MARKET_MOOD_RING/)

---

*Last updated: May 2026 — docs consolidated to reduce duplicate setup and troubleshooting files.*
