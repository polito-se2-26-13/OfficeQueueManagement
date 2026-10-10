const API_BASE_URL = 'http://localhost:8000';

async function getServices() {
  //   const response = await fetch(`${API_BASE_URL}/api/services`);
  //   const services = await response.json();
  const services = {
    services: [
      {
        id: 1,
        name: 'Service 1',
        description: 'Description of Service 1',
      },
      {
        id: 2,
        name: 'Service 2',
        description: 'Description of Service 2',
      },
    ],
  };
  return services;
}

async function getTicket() {
  // const response = await fetch(`${API_BASE_URL}/api/ticket`);
  // const ticket = await response.json();
  const ticket = {
    ticket_id: 1,
    ticket_cod: 'A1',
    service_name: 'Service 1',
    timeStamp: '2023-01-01T00:00:00Z',
  };
  return ticket;
}

export { getServices, getTicket };
