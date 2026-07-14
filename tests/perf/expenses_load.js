import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '15s', target: 10 },  // ramp up to 10 virtual users
    { duration: '30s', target: 10 },  // hold
    { duration: '15s', target: 0 },   // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests under 500ms
    http_req_failed: ['rate<0.01'],    // <1% errors
  },
};

const BASE = 'http://localhost:3000';

export default function () {
  const list = http.get(`${BASE}/api/expenses`);
  check(list, { 'list returns 200': (r) => r.status === 200 });

  const payload = JSON.stringify({
    amount: 99,
    category: 'Other',
    description: 'k6 load test',
  });
  const created = http.post(`${BASE}/api/expenses`, payload, {
    headers: { 'Content-Type': 'application/json' },
  });
  check(created, { 'create returns 201': (r) => r.status === 201 });

  sleep(1);
}