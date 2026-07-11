# Expense Tracker 

Full-stack expense tracker built as an end-to-end SDET showcase: REST API, database,
UI, and (in progress) a complete test-automation and CI/CD pipeline around it.

## Stack

| Layer | Tech |
|---|---|
| Backend | Node.js 22, Express, Mongoose |
| Database | MongoDB 7 (Docker) |
| Frontend | HTML/CSS/vanilla JS |
| API tests | Python, pytest, requests, pydantic, jsonschema, pymongo *(Phase 3)* |
| E2E tests | Playwright *(Phase 3)*, Appium — mobile web *(Phase 6)* |
| Performance | k6, JMeter *(Phase 3)* |
| Security | OWASP ZAP baseline *(Phase 4)* |
| CI/CD | Jenkins, Docker, Kubernetes *(Phase 4–5)* |
| Tracking | Jira (EXP project) — every commit references a ticket |

## Run it

```bash
docker compose up -d          # starts app + MongoDB
cd backend && node seed.js    # optional: load sample data
```

App: http://localhost:3000 · Health: http://localhost:3000/health

Dev mode without compose:

```bash
docker start expense-mongo    # or any local Mongo on 27017
cd backend && npm install && npx nodemon server.js
```

## API

| Method | Endpoint | Description |
|---|---|---|
| GET | /health | Service + DB status |
| POST | /api/expenses | Create expense (validated) |
| GET | /api/expenses | List, filters: `?category=` `&from=` `&to=` |
| GET | /api/expenses/summary | Totals by category (aggregation) |
| GET | /api/expenses/:id | Single expense (404/400 handling) |
| PUT | /api/expenses/:id | Update (schema-validated) |
| DELETE | /api/expenses/:id | Delete (204) |

## Project structure

```
expense-tracker-sdet/
├── backend/
│   ├── models/           Mongoose schemas (Expense)
│   ├── routes/           API routes (expenses)
│   ├── public/           Frontend UI (index.html)
│   ├── server.js         Express entry point
│   ├── seed.js           Sample data loader
│   └── Dockerfile
├── tests/
│   ├── api/              pytest + requests API tests
│   ├── e2e/              Playwright browser tests
│   ├── mobile/           Appium mobile web tests
│   ├── fixtures/         Test data (JSON payloads)
│   ├── schemas/          Pydantic response models
│   ├── perf/             k6 + JMeter scripts
│   └── utils/            Shared helpers
├── ci-cd/                Jenkinsfile + Kubernetes manifests
└── docker-compose.yml
```

## Roadmap

- [x] Phase 1–2: Environment, API, UI, dockerized stack
- [ ] Phase 3: pytest API suite, Playwright E2E, k6/JMeter, Allure
- [ ] Phase 4: Jenkins pipeline, OWASP ZAP, Kubernetes
- [ ] Phase 5: Cloud deploy (Render + Atlas)
- [ ] Phase 6: Appium mobile web testing
