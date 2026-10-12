import { Flex, Button } from 'antd';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';

import { getCounters } from '../api/api';

function Officer() {
  const [counters, setCounters] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCounters = async () => {
      const data = await getCounters();
      setCounters(data || []);
    };
    fetchCounters();
  }, []);

  const handleClick = counterId => {
    navigate(`/counter/${counterId}`);
  }

  return (
    <Flex vertical justify="center" align="center" gap="small" wrap style={{ width: '100%', height: '80vh', textAlign: 'center' }}>
      <h2>Please select your counter:</h2>
      {counters?.map(counter => (
        <Button key={counter.counter_id} type="primary" onClick={() => handleClick(counter.counter_id)}>
          Counter {counter.counter_id}
        </Button>
      ))}
    </Flex>
  );
}

export default Officer;