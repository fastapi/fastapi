import React from 'react';

import { Button, Container, Heading, Text } from '@chakra-ui/react';

const DeleteAccount: React.FC = () => {

    return (
        <>
            <Container maxW="full">
                <Heading size="sm" py={4}>
                    Delete Account
                </Heading>
                <Text>
                    Are you sure you want to delete your account? This action cannot be undone.
                </Text>
                <Button bg="ui.danger" color="white" _hover={{ opacity: 0.8 }} mt={4}>
                    Delete
                </Button>
            </ Container>
        </>
    );
}
export default DeleteAccount;