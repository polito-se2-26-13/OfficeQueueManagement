import { test, expect } from '@playwright/test';

// needs the backend on :8000 and the frontend on :5173, with the first counter serving at least one service

test('an officer calls the next customer', async ({ page, request }) => {
  const response = await request.get('/api/services');
  const services = await response.json();
  // one ticket per service, so the first counter has someone to call whatever services it serves
  for (const service of services) {
    await request.post('/api/tickets', { data: { service_id: service.service_id } });
  }

  await page.goto('/officer');
  await page.getByRole('button', { name: 'Counter' }).first().click();
  await page.getByRole('button', { name: 'Next Customer' }).click();

  await expect(page.getByText('Customer Ticket:')).toBeVisible();
});

test('an unknown counter shows an error to the officer', async ({ page }) => {
  await page.goto('/counter/99');
  await page.getByRole('button', { name: 'Next Customer' }).click();

  await expect(page.getByText('Could not call the next customer')).toBeVisible();
});