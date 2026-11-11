# NetSage AI — System Architecture

Version: 0.1

## 1. Architecture Principles

- Modular services with clear responsibilities
- API-first communication
- Independent data collection and AI reasoning
- Deterministic diagnostics wherever possible
- Provider-independent LLM integration
- Auditable AI decisions and actions

## 2. System Layers

### Layer 1: Infrastructure
Routers, switches, Linux servers and applications.

### Layer 2: Collection
Python collectors, SNMP, SSH and syslog integrations.

### Layer 3: Processing
Normalization, event processing and metrics processing.

### Layer 4: Storage
- PostgreSQL: incidents, inventory and historical records
- FalkorDB: network topology and dependencies
- Redis: caching and event processing
- FAISS: initial vector search

### Layer 5: Intelligence
- Rule-based anomaly detection
- Embedding and retrieval pipeline
- RAG
- LangGraph investigation workflows
- LLM reasoning
- Evaluation and guardrails

### Layer 6: Application
- FastAPI backend
- React and TypeScript frontend
- Network topology visualization
- AI Copilot
- Incident management

### Layer 7: Controlled Automation
Authorized diagnostics and human-approved remediation.

## 3. Initial Data Flow

Network Infrastructure
    -> Collectors
    -> Normalization
    -> Storage and Event Processing
    -> Detection Engine
    -> Investigation Orchestrator
    -> Evidence Validation
    -> API
    -> Dashboard and Incident Center

## 4. Data Responsibilities

PostgreSQL:
- Device inventory
- Incident records
- User information
- Investigation history

FalkorDB:
- Devices
- Interfaces
- Network connections
- Application dependencies
- Impact relationships

FAISS:
- Networking documentation embeddings
- Knowledge retrieval

Redis:
- Temporary event processing
- Cache
- Background task coordination

## 5. AI Investigation Workflow

1. Receive an incident.
2. Retrieve relevant telemetry.
3. Identify affected devices.
4. Query network topology.
5. Retrieve related logs and documentation.
6. Generate possible root causes.
7. Validate hypotheses against evidence.
8. Generate a structured investigation report.
9. Request human review when appropriate.

## 6. AI Safety

- LLMs cannot invent telemetry.
- Every important diagnosis must reference evidence.
- Tool calls require input validation.
- Diagnostic permissions are restricted.
- Remediation requires explicit approval.
- Actions must be auditable.

## 7. Initial Technology Stack

Python 3.12
FastAPI
PostgreSQL
FalkorDB
Redis
FAISS
Sentence Transformers
LangGraph
LLM API
React
TypeScript
Tailwind CSS
React Flow
Docker Compose
Pytest

## 8. Architecture Evolution

The initial MVP uses a modular monolith where practical.
Collectors and background workers may run as separate
processes or containers.

Services will be separated further only when justified
by scalability, reliability or deployment requirements.
