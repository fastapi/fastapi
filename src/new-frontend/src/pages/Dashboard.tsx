import React from 'react';

import { Container, Text } from '@chakra-ui/react';

import { useUserStore } from '../store/user-store';


const Dashboard: React.FC = () => {
    const { user } = useUserStore();

    return (
        <>
            <Container maxW="full" pt={12}>
                <Text fontSize="2xl">Hi, {user?.full_name || user?.email} 👋🏼</Text>
                <Text>Welcome back, nice to see you again!</Text>
            </Container>
        </>

    )
}

export default Dashboard;