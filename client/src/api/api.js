const API_BASE_URL = 'http://localhost:8000';

async function getServices() {
  const response = await fetch(`${API_BASE_URL}/api/services`);
  const services = await response.json();
  return services;
}

async function getTicket(id) {
    const response = await fetch(`${API_BASE_URL}/api/tickets`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ service_id: Number(id) }),
  });
  const ticket = await response.json();
  return ticket;
}

async function getCounters() {
  const response = await fetch(`${API_BASE_URL}/api/counters`);
  const counters = await response.json();
  return counters;
}

async function nextCustomer(counterId) {
  const response = await fetch(`${API_BASE_URL}/api/counters/${counterId}/next-customer`, {
    method: 'POST',
  });

  if (response.status === 204) {
    return null;
  }

  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }

  const nextInfo = await response.json();
  return nextInfo;
}

export { getServices, getTicket, getCounters, nextCustomer };
