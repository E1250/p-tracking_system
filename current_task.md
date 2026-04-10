# 🚀 Project Roadmap: The Path to Production

This document outlines the critical "missing pieces" to elevate the **Tracking Dashboard** from a prototype to a senior-level production system.

## 🏗️ 1. Clean Architecture & Refactoring
**Status:** 🟠 In Progress
**Why?** Decoupling logic allows you to upgrade AI models or change your DB without breaking everything.

- [ ] **Implement `ProcessingPipeline`**: Move the logic from `camera_stream.py` to `backend/services/pipeline.py`.
- [ ] **Dependency Injection**: Pass model instances into the pipeline instead of reaching into `app.state`.
- [ ] **Error Boundaries**: Create custom exceptions (e.g., `InferenceError`, `DecodingError`) to handle failures gracefully.

## 🧪 2. Robust Testing (Priority)
**Status:** 🔴 Missing
**Why?** You can't scale what you can't verify.

- [ ] **Unit Tests**: Test the `calculate_detection_box_center` and other utility functions.
- [ ] **Mocked Model Tests**:
  ```python
  def test_pipeline_with_mock_ai():
      mock_detector = MagicMock()
      mock_detector.detect.return_value = FakeDetections()
      # ... verify the pipeline still works without a real GPU
  ```
- [ ] **Integration Test**: Full flow from WebSocket input to Redis output.
- [ ] **Load Testing**: Use **Locust** to benchmark the system's capacity.

## 🔒 3. Security & Resilience
**Status:** 🔴 Missing
**Why?** Prevents unauthorized access and system crashes.

- [ ] **Auth Middleware**: Protect `/detectors/stream` with an API Key.
- [ ] **Circuit Breakers**: If Redis is down, the system should log the error but not crash the entire app.
- [ ] **Client Heartbeats**: Implement "ping/pong" to clean up dead connections faster.

## 📊 4. Observability
**Status:** 🟠 Partially Implemented
**Why?** "If you can't measure it, you can't improve it."

- [ ] **Grafana Dashboard**: Create a dashboard visualization for your current Prometheus metrics.
- [ ] **Alerting Service**: A simple service that triggers a Slack/Discord webhook when `is_danger` is True for > 5 seconds.
- [ ] **Structured Trace Log**: Link frame IDs across the system to see exactly where a specific frame was delayed.

## 🐳 5. DevOps & CI/CD
**Status:** 🔴 Missing
**Why?** Automates the boring stuff so you can focus on code.

- [ ] **GitHub Actions**: Add a workflow to run `ruff` and `pytest` on every PR.
- [ ] **Docker Optimization**: Use multi-stage builds to reduce the Docker image size.

## 📖 6. Documentation
**Status:** 🟠 Basic
**Why?** Essential for your portfolio. Recruiters look for how you explain complex systems.

- [ ] **Mermaid Diagrams**: Add a "Data Flow Diagram" to your README.
- [ ] **API Documentation**: Polish the FastAPI Swagger descriptions with clear examples.







- For tasks.md, it is kinda alternate to `Trello` and agile for project management, I plan to keep using Github Issues and ``todo` file. 
- I would prefer using `env.yml` rather than req.txt in my case.
- fb16 has been added, it takes lower memory and get the same accuracy.

## GP Tracking Dashboard — Task Plan (End-to-End, Multi-Worker)

Goal: product-grade realtime incident detection (person/fire/smoke) from live camera streams, with a dashboard that visualizes state + alerts, running safely on multiple workers.

### Guiding constraints

- Low-latency realtime (bounded buffering, backpressure, "latest-frame wins")
- Observable (metrics + structured logs + traces/profiles)
- Reproducible (dependency manifests match imports; clear run commands)
- Testable (pytest tests for API + websocket flows)

---

---

## Phase 1 — Backend architecture for multi-worker

### ✅ 1A) Replace in-memory shared state (`app.state`)

Current: `camera_stream` writes to `app.state.camera_metadata` and `dashboard_stream` reads it.
Problem: breaks with multiple workers.
Plan:

- ✅ Introduce Redis as the shared state store (single source of truth)
  - Key schema example:
    - `camera:{camera_id}:metadata` -> JSON blob (latest snapshot)
    - `camera:{camera_id}:last_seen` -> timestamp
    - `cameras:active` -> set of active camera_ids
- ✅ Choose update model:
  - Option A: dashboard websocket polls Redis at interval (simple, acceptable)
  - ✅ Option B: Pub/Sub per camera or global "updates" channel (lower latency, more complex) *(Great job implementing Pub/Sub in `dashboard_stream`! It's much better for latency.)*
- Decide retention/TTL:
  - `metadata` TTL (e.g. 10s) so dead cameras disappear automatically
  - active cameras set cleanup strategy
  Deliverable: backend works with `--workers N` consistently.

### 1B) Add backpressure & compute model

- Implement per-camera processing policy:
  - "latest-frame wins": keep only the newest frame (drop backlog)
  - bounded queue size=1 (or 2) per camera
- Protect event-loop:
  - all CPU heavy ops in executor
  - GPU inference serialized per device or batched (see Phase 2)
  Deliverable: stable under high FPS camera input.

---

## Phase 2 — Realtime inference pipeline (person/fire/smoke)

### 2C) Optimization plan (pragmatic)

- Profile baseline end-to-end latency (frame recv -> inference -> stored -> dashboard)
- GPU optimizations:
  - resize strategy (fixed short side)
  - ✅ half precision (fp16) if supported *(Awesome! Reduced memory usage while preserving accuracy is a massive win.)*
  - optional batching (small batch 2–5) ONLY if it reduces latency at target load
- CPU optimizations:
  - faster JPEG decode path (measure)
  - avoid repeated allocations where possible
  Deliverable: measured latency/FPS targets documented.

---

## Phase 4 — Observability & operations

- ✅ Metrics:
  - ✅ per-camera FPS in/out, inference time, queue drops *(Awesome use of MLFlow logging metrics and Prometheus!)*
  - ✅ dashboard connected count, active cameras, Redis latency
- ✅ Logging:
  - ✅ structured events with `camera_id`, correlation ids *(StructLogger looks great! structured logging makes debugging much faster.)*
- ✅ Health:
  - ✅ `/health/ready` checks Redis connectivity + model loaded *(I see you have the health router attached already!)*
- Deployment:
  - docker-compose: backend + redis (+ optional prometheus/grafana)
  - production server command (gunicorn/uvicorn workers) documented
  Deliverable: you can run locally as a “mini production” stack.

---

## Phase 5 — Tests

- Convert websocket scripts into pytest:
  - 2 cameras + 1 dashboard integration test
  - assert Redis contains expected keys and dashboard receives updates
- Add load test (optional):
  - simulate camera FPS streams, ensure bounded memory and acceptable latency
  Deliverable: CI-friendly tests validating the critical path.

---

---

---

---

---

---

Good — your mindset is correct. Now I’ll give you **focused, actionable guidance** (no fluff).

---

# 🎯 Your Goal

> Turn this into a **real production-grade AI system**, not just a project.

---

# 🧠 1. The rule you MUST follow

👉 **Depth > Features**

If you keep adding features → you stay mid  
If you go deep → you move toward senior

---

# 🏗️ 2. Lock the Architecture (non-negotiable)

Refactor into **strict layers**:

```
/domain        → pure logic (tracking, depth, detection)
/application   → use cases (track_object, process_frame)
/infrastructure→ models, DB, external APIs
/interfaces    → FastAPI routes, UI

```

Rules:

- domain knows NOTHING about FastAPI, DB, or models
- everything injected (dependency injection mindset)

👉 This is where seniors stand out.

---

# 🤖 3. Turn AI into a real pipeline

Right now it's likely “functions”.

Make it:

```
Input → Preprocess → Model → Postprocess → Output

```

Add:

- config-based model selection
- ability to swap models (YOLO, custom, etc.)
- batching support

👉 Think like you're building a mini ML platform.

---

# ⚙️ 4. Backend like a real system

Add:

### Validation

- Pydantic schemas everywhere

### Logging

- structured logs (not print)

### Errors

- custom exceptions
- proper HTTP responses

### API design

- `/v1/track`
- `/v1/detect`

👉 Clean API = senior signal.

---

# 🔄 5. Async + Background processing

Very important:

- heavy tasks (AI inference) → background workers
- use:
  - queue (Redis + Celery or RQ)
  - or FastAPI background tasks (start simple)

👉 This separates juniors from real backend engineers.

---

# 📡 6. Real-time capability (optional but powerful)

If you add:

- WebSocket streaming
- live tracking feed

👉 This becomes a **serious system**

---

# 🧪 7. Testing (DON’T SKIP)

Minimum:

- unit tests for domain
- 1–2 API tests

You’ll learn:

- design quality
- edge cases
- stability

---

# 🐳 8. Production mindset

You already used Docker — good.

Now improve:

- docker-compose (backend + frontend + redis)
- environment configs
- `.env` handling

---

# 📊 9. Observability (very senior move)

Add:

- logging
- simple metrics (time per inference)

Optional:

- Prometheus / Grafana later

---

# 🧩 10. One advanced feature ONLY

Pick ONE:

- model serving system
- real-time tracking
- multi-camera support
- pipeline orchestration

👉 Don’t do all. Depth.

---

# 🛑 When to STOP?

This is critical.

👉 Stop when:

### ✅ You have:

- clean architecture (strict layers)
- working API (well designed)
- AI pipeline (modular)
- async/background processing
- basic tests
- dockerized system

AND:

### ✅ You can explain:

- every design decision
- trade-offs
- how to scale it

👉 If you can **defend your system like an engineer**, you’re ready.

---

# 🚨 When NOT to stop

If:

- code is messy
- logic mixed everywhere
- no tests
- no structure

👉 then you're not done

---

# 🧠 Final truth

Senior ≠ knowing more tools  
Senior = **how you think and structure systems**

---

# 🔥 If you follow this seriously

You won’t just have a project

👉 You’ll have:

- a **portfolio-level system**
- something you can talk about in interviews deeply
- real engineering experience

---

If you want next:  
I can **redesign your current repo structure step-by-step** into a clean architecture version.

---

---

---

---

# 🏗️ The 3-project strategy (this is ideal for you)

## 🥇 1. Core System (YOU ARE BUILDING THIS)

👉 tracking_system

Make it:

- full pipeline (AI + backend + frontend)
- real-time capable
- modular AI system

This becomes:  
👉 your **main flagship project**

---

## 🥈 2. Deep Learning / Research project

Not engineering — research style.

Examples:

- implement a paper (object tracking, SLAM, depth)
- improve a model
- experiment + metrics + evaluation

👉 Shows:

- you understand **math + DL deeply**

---

## 🥉 3. Robotics / Physical AI project

Even simple:

Examples:

- simulation (ROS, Gazebo)
- drone/car control logic
- sensor fusion (camera + something)

👉 Shows:

- you connect **AI with physics/world**

