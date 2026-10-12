import { test, expect } from '@playwright/test';

// needs the backend on :8000 and the frontend on :5173, with at least one service in the database

test('the totem shows the services of the backend', async ({ page, request }) => {
  const response = await request.get('/api/services');
  const services = await response.json();
  expect(services.length).toBeGreaterThan(0);

  await page.goto('/');
  await page.getByRole('button', { name: 'Customer' }).click();

  for (const service of services) {
    await expect(page.getByText(service.service_name, { exact: true })).toBeVisible();
  }
});

test('a customer gets a ticket for the chosen service', async ({ page, request }) => {
  const response = await request.get('/api/services');
  const services = await response.json();
  const service = services[0];

  await page.goto('/customer');
  const row = page.getByRole('tab', { name: service.service_name });
  await row.getByRole('button', { name: 'select' }).click();

  await expect(page).toHaveURL(/\/ticket\/[A-Z]\d{3,}$/);
  expect(page.url()).toContain('/ticket/' + service.service_name[0]);
  await expect(page.getByText('Your Ticket Code is')).toBeVisible();
});
