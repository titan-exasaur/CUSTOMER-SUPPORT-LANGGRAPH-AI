# Customer Support Triage Agentic AI

> An AWS serverless pipeline that automatically classifies, drafts responses for, and escalates customer support tickets — end-to-end, without human-in-the-loop.

---

## What Problem This Solves

Support teams are overwhelmed triaging tickets manually — deciding urgency, crafting responses, and flagging escalations one by one.
This system automates the full triage pipeline: a complaint comes in, agents classify it, draft a reply, and decide if it needs human escalation — all in one shot.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser)                         │
│              S3 Static Website  ·  HTML + CSS + JS              │
└───────────────────────┬─────────────────────────────────────────┘
                        │  POST /tickets
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway (HTTP API)                     │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│               API Lambda  ·  FastAPI + Mangum                   │
│    • Validates request  • Stores ticket → MongoDB Atlas         │
│    • Pushes { ticket_id } → SQS                                 │
│    • Returns ticket_id to UI                                    │
└──────────┬────────────────────────────┬─────────────────────────┘
           │ GET /tickets/{id}          │ enqueue
           │ (UI polls)                 ▼
           │              ┌────────────────────────┐
           │              │      Amazon SQS        │
           │              │  msg: { ticket_id }    │
           │              └────────────┬───────────┘
           │                           │ trigger
           │                           ▼
           │              ┌────────────────────────────────────────┐
           │              │         Worker Lambda (container)      │
           │              │                                        │
           │              │   ┌────────────────────────────────┐   │
           │              │   │    LangGraph Agent Workflow    │   │
           │              │   │                                │   │
           │              │   │  [Classifier] → [Responder]    │   │
           │              │   │       → [Escalation] → END     │   │
           │              │   └────────────────────────────────┘   │
           │              └───────────────────┬────────────────────┘
           │                                  │ write results
           │                                  ▼
           │              ┌────────────────────────────────────────┐
           └─────────────▶│           MongoDB Atlas                │
                          │  tickets collection  ·  full state     │
                          └────────────────────────────────────────┘

  ┌─────────────────────┐     ┌──────────────────────────────────┐
  │    Amazon ECR       │     │          CloudWatch Logs         │
  │  support-triage-api │────▶│  API Lambda logs                 │
  │support-triage-worker│     │  Worker Lambda logs              │
  └─────────────────────┘     └──────────────────────────────────┘
         │ provides images to both Lambdas
```

**Flow summary:**
1. User submits complaint via S3-hosted UI
2. API Gateway → API Lambda validates, stores ticket, enqueues `ticket_id` to SQS
3. SQS triggers Worker Lambda → LangGraph runs 3 agents sequentially
4. Final ticket state (category, draft response, escalation flag) written to MongoDB
5. UI polls `GET /tickets/{ticket_id}` until status = `completed`

---

## The 3 Agents

### 1. 🔍 Classifier Agent
Reads the raw ticket text and assigns a **category** (e.g. billing, technical, shipping) and an **urgency level** (low / medium / high).
Stores `ticket_category` and `urgency_level` to MongoDB before passing control downstream.

### 2. ✍️ Responder Agent
Takes the classified ticket and drafts a **context-aware reply** tailored to the category and urgency.
Stores the `draft_response` in MongoDB — ready for an agent or human to send.

### 3. 🚨 Escalation Agent
Evaluates the ticket against escalation rules (e.g. high urgency, legal mentions, repeat complaints).
Sets `needs_escalation: true/false` and updates `status` to `completed` in MongoDB.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML + CSS + JS, hosted on **Amazon S3** (static website) |
| Public API | **Amazon API Gateway** — HTTP API |
| API Compute | **AWS Lambda** (container) · **FastAPI** + **Mangum** |
| Queue | **Amazon SQS** — decouples API from processing |
| Worker Compute | **AWS Lambda** (container) — SQS-triggered |
| Agent Framework | **LangGraph** — sequential agent workflow |
| LLM | OpenAI / Anthropic (via LangChain) |
| Persistence | **MongoDB Atlas** — `tickets` collection |
| Container Registry | **Amazon ECR** — `support-triage-api`, `support-triage-worker` |
| Observability | **Amazon CloudWatch** — Lambda logs |
| Infrastructure | AWS Console / manual deploy |

---

## How to Run It

### Prerequisites
- AWS account with ECR, Lambda, API Gateway, SQS configured
- MongoDB Atlas cluster (with IP allowlist set)
- Docker installed locally
- Python 3.11+

### 1. Clone the repo
```bash
git clone https://github.com/your-username/customer-support-triage.git
cd customer-support-triage
```

### 2. Set environment variables
```bash
# .env (never commit this)
MONGODB_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/support
OPENAI_API_KEY=sk-...
AWS_REGION=us-east-1
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/<account>/support-triage
```

### 3. Build and push Docker images to ECR
```bash
# API image
docker build -t support-triage-api ./api
docker tag support-triage-api:latest <account>.dkr.ecr.<region>.amazonaws.com/support-triage-api:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/support-triage-api:latest

# Worker image
docker build -t support-triage-worker ./worker
docker tag support-triage-worker:latest <account>.dkr.ecr.<region>.amazonaws.com/support-triage-worker:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/support-triage-worker:latest
```

### 4. Deploy Lambdas
Update each Lambda in the AWS Console to use the new ECR image URI, or use the AWS CLI:
```bash
aws lambda update-function-code \
  --function-name support-triage-api \
  --image-uri <account>.dkr.ecr.<region>.amazonaws.com/support-triage-api:latest
```

### 5. Enable SQS trigger
In the AWS Console, attach the SQS queue as a trigger to the Worker Lambda (disable when not in use to avoid costs).

### 6. Open the frontend
Upload `frontend/index.html` to the S3 bucket and visit the S3 static website URL.

> **Note:** MongoDB Atlas `0.0.0.0/0` network access should be re-enabled (or Lambda IPs allowlisted) before testing.

---

## YouTube Walkthrough

🎬 **Coming soon** — full end-to-end demo including deployment, agent traces, and MongoDB output.

> Link will be added here once recorded.

---

## License

MIT