import { useParams, useNavigate } from 'react-router';
import { Flex, Button } from 'antd';
import { LeftOutlined } from '@ant-design/icons';

function Ticket() {
  const { code } = useParams();
  const navigate = useNavigate();

  return (
    <div style={{ position: 'relative', width: '100%', height: '100vh' }}>
      <Button
        type="text"
        size="large"
        icon={<LeftOutlined />}
        onClick={() => navigate(-1)}
        style={{
          position: 'absolute',
          top: 20,
          left: 20,
          zIndex: 10,
        }}
      >
        Back
      </Button>
      <Flex
        vertical
        justify="center"
        align="center"
        style={{ width: '100%', height: '80vh', textAlign: 'center' }}
      >
        <h2>Your Ticket Code is</h2>
        <h1>{code}</h1>
      </Flex>
    </div>
  );
}

export default Ticket;
