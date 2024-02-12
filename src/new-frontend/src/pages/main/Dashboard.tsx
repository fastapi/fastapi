import React from 'react';

import { Box, Text } from '@chakra-ui/react';

import { useUserStore } from '../../store/user-store';


const Dashboard: React.FC = () => {
    const { user } = useUserStore();

    return (
        <>
            {user ? (
                <Box width="100%" p={8}>
                    <Text fontSize="24px">Hi, {user.full_name || user.email} 👋🏼</Text>
                    <Text>Welcome back, nice to see you again!</Text>
                </Box>
            ) : null}
        </>

    )
}

export default Dashboard;