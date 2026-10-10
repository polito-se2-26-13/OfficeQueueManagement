import { useState } from 'react';
import { Button, Flex } from 'antd';
import { useParams } from 'react-router';

import { nextCustomer } from '../api/api';

function Counter() {
  const { id } = useParams();
  const [nextInfo, setNextInfo] = useState(null);
  const [hasCalled, setHasCalled] = useState(false);
  const handleClick = async () => {
    try {
      const nextInfo = await nextCustomer(id);
      setNextInfo(nextInfo);
      setHasCalled(true);
    } catch (error) {
      console.error('Error fetching next customer:', error);
    }
  };

  return (
    <Flex
      vertical
      align="center"
      justify="center"
      style={{ width: '100%', height: '80vh', textAlign: 'center' }}
    >
      <Button type="primary" onClick={handleClick}>
        Next Customer
      </Button>

      <div style={{ visibility: hasCalled ? 'visible' : 'hidden', marginTop: '20px' }}>
        {nextInfo ? (
          <div>
            <p>Customer Ticket: {nextInfo?.ticket_cod}</p>
            <p>Service: {nextInfo?.service?.service_name}</p>
          </div>
        ) : (
          <p>No more customers in the queue.</p>
        )}
      </div>
    </Flex>
  );
}

export default Counter;
