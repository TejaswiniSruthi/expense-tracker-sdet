# Expense Tracker — SDET Portfolio Project

Full-stack expense tracker built as an end-to-end SDET showcase: REST API, database,
UI, and a complete test-automation stack around it — with CI/CD and cloud deployment
in progress.

## Stack

| Layer | Tech |
|---|---|
| Backend | Node.js 22, Express, Mongoose |
| Database | MongoDB 7 (Docker) |
| Frontend | HTML/CSS/vanilla JS |
| API tests | Python, pytest, requests, pydantic, jsonschema, pymongo |
| E2E tests | Playwright (pytest-playwright) |
| Performance | k6, JMeter |
| Reporting | Allure |
| Security | OWASP ZAP baseline *(Phase 4)* |
| CI/CD | Jenkins, Docker, Kubernetes *(Phase 4–5)* |
| Mobile | Appium — mobile web *(Phase 6)* |
| Tracking | Jira (EXP project) — every commit references a ticket |

## Run the app

````bash
docker compose up -d          # starts app + MongoDB
cd backend && node seed.js    # optional: load sample data
````

App: http://localhost:3000 · Health: http://localhost:3000/health

Dev mode without compose:

````bash
docker start expense-mongo
cd backend && npm install && npx nodemon server.js
````

## Run the tests

````bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r tests/requirements.txt
playwright install chromium
````

| Suite | Command |
|---|---|
| Everything | `pytest -v` |
| Smoke only | `pytest -m smoke` |
| API regression | `pytest -m regression` |
| E2E (browser) | `pytest -m e2e` |
| E2E watch mode | `pytest -m e2e --headed --slowmo 500` |
| Allure report | `allure serve reports/allure-results` |
| k6 load test | `k6 run tests/perf/expenses_load.js` |
| JMeter (headless) | `jmeter -n -t tests/perf/expense_load.jmx -l reports/jmeter_results.jtl -e -o reports/jmeter_html` |

The API suite covers functional CRUD, data-driven positive/negative cases (JSON
fixtures + parametrize), response-contract validation (pydantic + jsonschema),
cross-endpoint consistency, and direct MongoDB state assertions via pymongo.

## Performance testing — k6 vs JMeter

The same API is load-tested with both tools deliberately:

- **k6** — scripted JavaScript, thresholds-as-code (`p(95)<500`, error rate <1%),
  tiny footprint. Built for CI gates: the process exits non-zero when thresholds
  fail, so the pipeline fails with it.
- **JMeter** — GUI-built plan, CSV-driven test data without code, rich HTML
  dashboard out of the box. Stronger for complex enterprise scenarios and
  non-coders on the team.
- **Takeaway**: k6 lives in the pipeline; JMeter is the exploratory / reporting
  tool. Same API, same order of numbers — the tool doesn't change the truth.

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

````
expense-tracker-sdet/
├── backend/
│   ├── models/           Mongoose schemas (Expense)
│   ├── routes/           API routes (expenses)
│   ├── public/           Frontend UI (index.html)
│   ├── server.js         Express entry point
│   ├── seed.js           Sample data loader
│   └── Dockerfile
├── tests/
│   ├── api/              pytest + requests API tests (conftest fixtures)
│   ├── e2e/              Playwright browser tests
│   ├── mobile/           Appium mobile web tests (planned)
│   ├── fixtures/         Test data (JSON payloads)
│   ├── schemas/          Pydantic models + JSON schemas (contracts)
│   ├── perf/             k6 script + JMeter plan and CSV data
│   └── utils/            Shared helpers
├── ci-cd/                Jenkinsfile + Kubernetes manifests (planned)
├── pytest.ini
└── docker-compose.yml
````

## Roadmap

- [x] Phase 1–2: Environment, API, UI, dockerized stack
- [x] Phase 3: pytest API suite, contracts, DB assertions, Playwright E2E, k6 + JMeter, Allure
- [ ] Phase 4: Jenkins pipeline, OWASP ZAP, Kubernetes
- [ ] Phase 5: Cloud deploy (Render + Atlas)
- [ ] Phase 6: Appium mobile web testing
````
````
