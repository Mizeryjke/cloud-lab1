import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 60 },
    { duration: '5m', target: 60 },
    { duration: '2m', target: 0 },
  ],
};

const BASE_URL = __ENV.TARGET_URL || 'http://ВАШ_ALB_DNS.eu-north-1.elb.amazonaws.com';

export default function () {
  const payload = JSON.stringify({
    name: `Item-${Math.floor(Math.random() * 100000)}`,
    description: 'k6 load test entry'
  });

  const headers = { 'Content-Type': 'application/json' };
  const resPost = http.post(`${BASE_URL}/items`, payload, { headers });
  
  check(resPost, {
    'POST /items status 201': (r) => r.status === 201,
  });

  sleep(0.5);

  for (let i = 0; i < 9; i++) {
    const resGet = http.get(`${BASE_URL}/items`);
    check(resGet, {
      'GET /items status 200': (r) => r.status === 200,
    });
    sleep(0.2);
  }
}