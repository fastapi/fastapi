import React from 'react';

import { Box, Text } from '@chakra-ui/react';

import { useUserStore } from '../store/user-store';


const Dashboard: React.FC = () => {
    const { user } = useUserStore();

    return (
        <>
            <Box width="100%" p={8}>
                <Text fontSize="2xl">Hi, {user?.full_name || user?.email} 👋🏼</Text>
                <Text>Welcome back, nice to see you again!</Text>
            </Box>
        </>

    )
}

export default Dashboard;