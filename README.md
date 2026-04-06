# Event-Driven Workflow Engine with Netflix Conductor

An event-driven workflow orchestration system built with **Netflix Conductor (Orkes Community Edition)**, **Redis**, and **Python**. This project demonstrates how to design and run distributed, fault-tolerant service workflows using the Saga pattern — where individual service workers communicate through Conductor, and failures in one service automatically trigger compensation actions across dependent services.

---

## Architecture Overview

```
                        ┌─────────────────────────────────────┐
                        │         conductor-net (Docker)       │
                        │                                      │
  HTTP Request          │   ┌─────────┐    ┌──────────────┐   │
 ──────────────────────►│   │   API   │───►│   Conductor  │   │
  POST /workflow/start  │   │ :8000   │    │  Server      │   │
                        │   └─────────┘    │  :8080       │   │
                        │                  └──────┬───────┘   │
                        │                         │           │
                        │            ┌────────────┼────────┐  │
                        │            ▼            ▼        ▼  │
                        │   ┌──────────────┐ ┌─────────┐ ┌──────────┐ │
                        │   │ login-worker │ │backend  │ │db-worker │ │
                        │   │ (Python)     │ │-worker  │ │(Python)  │ │
                        │   └──────────────┘ │(Python) │ └──────────┘ │
                        │                    └─────────┘              │
                        │   ┌─────────┐                               │
                        │   │  Redis  │◄──── State & Queue Broker     │
                        │   │  :6379  │                               │
                        │   └─────────┘                               │
                        └─────────────────────────────────────────────┘
```

The system consists of:

- **Conductor Server** — Orchestrates task execution, manages workflow state, and exposes the UI and REST API
- **Redis** — Acts as the backing store for Conductor's in-memory task queues and state management
- **Workers** — Independently containerized Python services (login, backend, db) that poll Conductor for tasks, execute business logic, and report results
- **API** — A FastAPI/Python HTTP gateway that triggers workflow executions programmatically
- **Saga Pattern** — If any worker fails, dependent services detect the failure and trigger compensation actions to maintain overall system consistency

---

## Project Structure

```
conductor-workflow/
├── api/
│   └── Dockerfile              # API service container definition
├── workers/
│   ├── login_worker/
│   │   └── Dockerfile          # Login service worker container
│   ├── backend_worker/
│   │   └── Dockerfile          # Backend service worker container
│   └── db_worker/
│       └── Dockerfile          # Database service worker container
├── workflows/
│   ├── tasks.json              # Task definitions registered with Conductor
│   └── service_workflow.json   # Workflow definition (task sequence & routing)
├── docker-compose.yml          # Full stack orchestration
└── register_definitions.sh     # Script to register tasks & workflows with Conductor API
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Workflow Orchestrator | Netflix Conductor (Orkes Community Standalone) |
| Message Broker / State | Redis 7 |
| Worker Language | Python |
| Containerization | Docker + Docker Compose |
| Workflow Definitions | JSON |
| Registration Script | Bash + cURL |

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/) installed
- Ports `8080`, `5000`, `6379`, and `8000` available on your machine

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/sathwikreddy12/conductor-workflow.git
cd conductor-workflow
```

### 2. Start the Full Stack

```bash
docker-compose up --build
```

This command will:
- Start Redis and wait for it to be healthy
- Start the Conductor Server and wait for it to be ready
- Build and start all three workers (login, backend, db) and the API service

> The health checks ensure services start in the correct dependency order automatically.

### 3. Register Workflow & Task Definitions

Once the Conductor server is running, register the task and workflow definitions:

```bash
chmod +x register_definitions.sh
./register_definitions.sh
```

This script POSTs `workflows/tasks.json` and `workflows/service_workflow.json` to the Conductor metadata API at `http://localhost:8080/api`.

### 4. Access the Conductor UI

Open your browser and navigate to:

```
http://localhost:8080
```

From here you can monitor workflow executions, inspect task states, and view execution history.

### 5. Trigger a Workflow

Use the API service running at `http://localhost:8000` to trigger workflow executions, or use the Conductor UI directly.

---

## How It Works

1. A client sends a request to the **API service**, which calls the Conductor Server to start a workflow instance.
2. Conductor evaluates the **workflow definition** and schedules the first task.
3. The appropriate **worker** polls Conductor, picks up its task, executes the business logic, and reports success or failure.
4. Conductor proceeds to the next task based on the result.
5. If a worker **fails**, the **Saga pattern** kicks in — Conductor routes to compensation tasks, triggering rollback or cleanup logic in dependent services to maintain system consistency.

---

## Services & Ports

| Service | Port | Description |
|---------|------|-------------|
| Conductor Server | `8080` | Main orchestration server + UI |
| Conductor gRPC | `5000` | gRPC endpoint |
| Redis | `6379` | Task queue and state store |
| API | `8000` | HTTP gateway for triggering workflows |

---

## Stopping the Stack

```bash
docker-compose down
```

To also remove volumes:

```bash
docker-compose down -v
```

---

## Key Concepts Demonstrated

- **Workflow Orchestration** — Centralized coordination of distributed service tasks using Conductor
- **Saga Pattern** — Distributed transaction management with automatic compensation on failure
- **Worker Isolation** — Each service is independently containerized and polls for its own task type
- **Health-Check Chaining** — Docker Compose health checks ensure strict startup ordering
- **IaC for Workflows** — Workflow and task definitions are version-controlled as JSON
- **Bash Automation** — Shell scripting to automate API registration on startup

---

## Author

**Ketha Sathwiik Reddy**  
[GitHub](https://github.com/sathwikreddy12) · [LinkedIn](https://linkedin.com/in/ketha-sathwik-reddy)
