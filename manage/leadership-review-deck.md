# Market Mood Ring
## Leadership Review Deck

Prepared for: Engineering and Product Leadership  
Date: 2026-05-03  
Repo: `MARKET_MOOD_RING`

**Live slides:** [https://vgandhi1.github.io/MARKET_MOOD_RING/](https://vgandhi1.github.io/MARKET_MOOD_RING/) · Source: [`manage/presentation.html`](presentation.html)

---

## 1) Executive Summary

- Market Mood Ring is an operational real-time market intelligence platform built on Kafka, Flink, PostgreSQL (pgvector), and Streamlit.
- The platform is currently in a functional "production-ready for portfolio/demo" state with end-to-end ingestion, sentiment scoring, and AI-assisted explanations.
- Current architecture emphasizes fast iteration and local deployability (Docker + host Ollama), with clear paths to harden for enterprise usage.
- Priority for next quarter: improve reliability/SLOs, testing depth, and security/compliance readiness.

---

## 2) Repository and Delivery Status

- Remote sync status: local `main` is aligned with `origin/main` (no branch drift detected during review).
- Recent release themes:
  - Flink sentiment processing improvements
  - Documentation and setup hardening
  - 72-hour dashboard data window
  - Llama 3 AI analyst integration
- Documentation maturity is high, with extensive setup, architecture, and troubleshooting guides.

---

## 3) Product Vision and Use Cases

### Vision
Convert noisy, high-velocity market signals into clear, actionable narrative for non-quant users.

### Primary Use Cases
- Explain "why a stock is moving" based on real-time headline sentiment.
- Provide live monitoring of price movement and sentiment drift.
- Enable conversational analysis via AI analyst grounded in recent ingested news.

---

## 4) System Architecture (Leadership View)

### Ingestion
- `news_producer.py`: fetches headlines from Finnhub.
- `price_producer.py`: fetches market prices from Finnhub.
- `price_consumer.py`: writes price stream to PostgreSQL.
- `rag_ingest.py`: embeds text for semantic retrieval.

### Processing
- `flink_sentiment.py` consumes news and computes VADER sentiment scores in stream.

### Storage
- PostgreSQL database `market_mood` with:
  - `price_log`
  - `sentiment_log`
  - `financial_knowledge` (vector embeddings)

### Experience
- Streamlit dashboard for live charts and sentiment table.
- AI Analyst uses vector retrieval + Ollama Llama 3 generation.

---

## 5) Current Capabilities Delivered

- Real-time message transport through Kafka (KRaft mode, no Zookeeper dependency).
- Streaming sentiment analytics with Flink and Python UDF logic.
- 72-hour charting and recent sentiment surfacing in dashboard.
- RAG-backed AI chat to contextualize market events.
- Scripted bootstrap (`start_data_pipeline.sh`) to reduce setup friction across WSL2 + Docker + host LLM.

---

## 6) Business Value Delivered to Date

- Demonstrates full-stack data + AI system integration, useful for stakeholder demos and technical hiring signals.
- Provides near-real-time market mood abstraction for rapid decision support.
- Reduces interpretation latency: transforms raw headlines into concise sentiment and narrative.
- Creates foundation for premium features (alerts, watchlists, risk signals, explainability trails).

---

## 7) Engineering Quality Assessment

### Strengths
- Clear modular boundaries (producer, stream processing, dashboard, docs).
- Good observability entry points (Flink UI, docker logs, troubleshooting docs).
- Strong onboarding docs and architecture explanations.

### Gaps
- Limited visible automated test coverage in repository.
- Single-node infrastructure defaults (Kafka/Flink/Postgres) constrain resilience.
- Credential management is local/dev-oriented; not yet enterprise secret-store integrated.

---

## 8) Key Risks and Mitigations

### Operational Risk
- **Risk:** Pipeline interruptions due to local environment/network dependencies.
- **Mitigation:** Add health probes, auto-restart policies, and synthetic data backfill mode.

### Data Quality Risk
- **Risk:** Sentiment false positives/negatives from headline-only context.
- **Mitigation:** Add confidence banding, source quality weights, and outcome feedback loop.

### AI Reliability Risk
- **Risk:** LLM response inconsistency and possible hallucination.
- **Mitigation:** Strict prompt constraints, response templates, and citation of retrieved context snippets.

### Security/Compliance Risk
- **Risk:** Local key handling and open service boundaries.
- **Mitigation:** Move to secret manager, scoped service accounts, and network policy hardening.

---

## 9) Performance and Scalability Outlook

- Current design supports lightweight real-time workloads and demonstration traffic effectively.
- Scale blockers for production:
  - single broker and single DB instance
  - absence of partitioning and retention governance by workload tier
  - limited load and soak testing evidence
- Recommended scaling path:
  1. Introduce staging environment and baseline SLOs.
  2. Add horizontal scaling and partition strategies.
  3. Introduce managed services or Kubernetes orchestration for sustained throughput.

---

## 10) Security and Compliance Readiness

Current maturity: early-to-mid (developer production readiness, not regulated production).

Priority controls to add:
- Secrets in managed vault (remove local plaintext dependencies in runtime).
- Audit logging for user prompts and model responses.
- PII/data classification policy, retention windows, and deletion workflow.
- Dependency and image vulnerability scanning in CI.

---

## 11) Roadmap (Next 90 Days)

### Month 1 - Reliability Foundation
- CI pipeline with lint/test/build gates.
- Container health checks + restart strategy.
- Structured logging and baseline metrics dashboard.

### Month 2 - Product and Model Quality
- Sentiment calibration with validation dataset.
- Alerting feature (threshold-based watchlist notifications).
- Better AI answer grounding and citation UX.

### Month 3 - Production Hardening
- Staging deployment and runbook completion.
- Security controls (secrets, RBAC, scanning).
- Leadership review of readiness for pilot users.

---

## 12) Decisions Requested from Leadership

1. Approve a 90-day hardening sprint before external pilot.
2. Prioritize reliability + security over net-new feature breadth.
3. Confirm target audience for pilot (internal analytics users vs external beta users).
4. Approve cloud budget for managed messaging/DB if uptime goals exceed local-stack limits.

---

## Appendix A: Project Components at a Glance

- `producer/`: market data ingestion and DB writer components.
- `flink_jobs/`: stream sentiment logic.
- `dashboard/`: Streamlit UI and AI analyst interaction.
- `docs/`: setup, architecture, and troubleshooting corpus.
- `docker-compose.yaml`: local orchestration of core services.
- `init.sql`: schema and vector index initialization.

---

## Appendix B: Presentation assets

| Asset | Path | Use |
|-------|------|-----|
| Interactive slides | `manage/presentation.html` | Keyboard navigation (←/→), dot nav, 10+ slides |
| GitHub Pages | `https://vgandhi1.github.io/MARKET_MOOD_RING/` | Public demo after workflow deploys `gh-pages` |
| This document | `manage/leadership-review-deck.md` | Speaker notes and appendix |

## Appendix C: Suggested Presentation Flow (15 minutes)

- 2 min: business problem and executive summary
- 4 min: architecture and current capabilities demo snapshot
- 3 min: value delivered and adoption potential
- 3 min: risks and mitigation plan
- 3 min: roadmap and leadership decisions
