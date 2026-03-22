[ ] - In Yolo Detector file, it has ExportFormats enum, put it in the correct place. 

## GP Tracking Dashboard — Task Plan (End-to-End, Multi-Worker)

Goal: product-grade realtime incident detection (person/fire/smoke) from live camera streams, with a dashboard that visualizes state + alerts, running safely on multiple workers.

### Guiding constraints

- Multi-worker friendly (no reliance on in-process `app.state` for shared state)
- Low-latency realtime (bounded buffering, backpressure, "latest-frame wins")
- Observable (metrics + structured logs + traces/profiles)
- Reproducible (dependency manifests match imports; clear run commands)
- Testable (pytest tests for API + websocket flows)

---

## Phase 0 — Repo hygiene + reproducibility (quick wins)

- Add `TASKS.md` (this file)
- Ensure Python deps are reproducible:
  - Sync `requirements.txt` with actual backend imports (fastapi/uvicorn/prometheus_client/structlog/pydantic-settings/pyyaml/opencv-python/numpy/etc.)
  - Decide: use `requirements.txt` as source of truth, and keep `env.yml` optional (or generate it from pip)
- Add `.env.example` (no secrets), document required env vars
- Ensure runtime artifacts are gitignored:
  - `app/logs/`, `app/*profile*.html`, `app/*.json` profiler outputs, etc.
  Deliverable: `pip install -r requirements.txt` boots backend.

---

## Phase 1 — Backend architecture for multi-worker

### 1A) Replace in-memory shared state (`app.state`)

Current: `camera_stream` writes to `app.state.camera_metadata` and `dashboard_stream` reads it.
Problem: breaks with multiple workers.
Plan:

- Introduce Redis as the shared state store (single source of truth)
  - Key schema example:
    - `camera:{camera_id}:metadata` -> JSON blob (latest snapshot)
    - `camera:{camera_id}:last_seen` -> timestamp
    - `cameras:active` -> set of active camera_ids
- Choose update model:
  - Option A: dashboard websocket polls Redis at interval (simple, acceptable)
  - Option B: Pub/Sub per camera or global "updates" channel (lower latency, more complex)
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

### 2A) Define contracts (backend <-> dashboard)

- Define a single camera snapshot schema (Pydantic model), including:
  - `camera_id`, `timestamp`, `is_danger`, `danger_labels` (person/fire/smoke)
  - `detections`: list of bboxes with class/conf/coords
  - optional: `depth_points` / occupancy / heatmap summary
- Ensure safe defaults (no mutable list defaults)
Deliverable: versioned JSON schema that dashboard consumes.

### 2B) YOLO inference integration

- Enable YOLO detection in camera websocket handler
- Add thresholds per class (config-driven)
- Implement "danger" rule:
  - danger if any of {person, fire, smoke} above threshold
  - optional: debounce (e.g. require K of last M frames to reduce flicker)
  Deliverable: live detections + `is_danger` updates stored in Redis.

### 2C) Optimization plan (pragmatic)

- Profile baseline end-to-end latency (frame recv -> inference -> stored -> dashboard)
- GPU optimizations:
  - resize strategy (fixed short side)
  - half precision (fp16) if supported
  - optional batching (small batch 2–5) ONLY if it reduces latency at target load
- CPU optimizations:
  - faster JPEG decode path (measure)
  - avoid repeated allocations where possible
  Deliverable: measured latency/FPS targets documented.

---

## Phase 3 — Dashboard: realtime viewer (not just editor)

Current: dashboard is a floorplan editor stored in localStorage.
Plan:

- Add a networking layer:
  - connect to backend websocket `/dashboard/stream`
  - render camera states (danger coloring, badges)
- Map backend camera_ids to floorplan camera nodes:
  - add `camera_id` field to camera nodes in the editor data model
  - UI for assigning/selecting camera_id per placed camera icon
- UX:
  - alert panel + timeline (last N incidents)
  - per-camera details drawer (detections list, last update time)
  Deliverable: dashboard shows realtime danger status on the floorplan.

---

## Phase 4 — Observability & operations

- Metrics:
  - per-camera FPS in/out, inference time, queue drops
  - dashboard connected count, active cameras, Redis latency
- Logging:
  - structured events with `camera_id`, correlation ids
- Health:
  - `/health/ready` checks Redis connectivity + model loaded
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

## Definition of Done (for MVP)

- Multiple workers enabled; state consistent via Redis
- Cameras stream frames, backend detects person/fire/smoke, writes snapshots
- Dashboard websocket receives snapshots and renders danger status
- Metrics + logs + health endpoints are meaningful
- Reproducible install/run documented

