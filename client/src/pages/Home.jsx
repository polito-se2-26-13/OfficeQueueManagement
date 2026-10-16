// import React from 'react';
import { useNavigate } from 'react-router';
import { Button, Flex } from 'antd';

function Home() {
  const navigate = useNavigate();
  const handleClick = role => {
    navigate(`/${role}`);
  };
  return (
    <>
      <h1>Home</h1>
      <Flex vertical justify="middle" align="center" gap="large" style={{ marginTop: '100px' }}>
        <Button
          type="primary"
          size="large"
          onClick={() => {
            handleClick('customer');
          }}
        >
          Customer
        </Button>
        <Button
          type="primary"
          size="large"
          onClick={() => {
            handleClick('officer');
          }}
        >
          Officer
        </Button>
        <Button
          type="primary"
          size="large"
          onClick={() => {
            handleClick('admin');
          }}
        >
          Admin
        </Button>
      </Flex>
    </>
  );
}

export default Home;
