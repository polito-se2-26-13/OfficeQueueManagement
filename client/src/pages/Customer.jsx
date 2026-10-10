import { useNavigate } from 'react-router';
import { useState, useEffect } from 'react';
import { Collapse, Button, Flex } from 'antd';

import { getServices, getTicket } from '../api/api';

function Customer() {
  const navigate = useNavigate();
  const handleClick = id => {
    //send request to server to create a ticket with the selected service id
    getTicket(id).then(ticket => { 
      navigate(`/ticket/${ticket.ticket_cod}`);
    })
  };

  const [services, setServices] = useState([]);

  useEffect(() => {
    const fetchServices = async () => {
      const data = await getServices();
      setServices(data.services);
    };
    fetchServices();
    console.log(services);
  }, []);

  return (
    <>
      <h1>Please select your services:</h1>
      <Flex justify="center" align="center" style={{ width: '100%', marginTop: '100px' }}>
        <Collapse
          accordion
          style={{ width: '80%' }}
          items={services.map(service => ({
            key: service.id,
            label: (
              <Flex justify="space-between" align="center" style={{ paddingInline: '20px' }}>
                <div>{service.name}</div>
                <Button type="primary" size="large" onClick={() => handleClick(service.id)}>
                  select
                </Button>
              </Flex>
            ),
            children: service.description,
          }))}
        ></Collapse>
      </Flex>
    </>
  );
}

export default Customer;
