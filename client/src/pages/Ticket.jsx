import { useParams } from 'react-router';
import { Flex } from 'antd';

function Ticket() {
  const { code } = useParams();
  return (
    <Flex
      vertical
      justify="center"
      align="center"
      style={{ width: '100%', height: '80vh', textAlign: 'center' }}
    >
      <h2>Your Ticket Code is</h2>
      <h1>{code}</h1>
    </Flex>
  );
}

export default Ticket;
