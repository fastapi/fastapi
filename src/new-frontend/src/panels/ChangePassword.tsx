import React from 'react';

import { Box, Button, Container, FormControl, FormLabel, Heading, Input } from '@chakra-ui/react';

const ChangePassword: React.FC = () => {

    return (
        <>
            <Container maxW="full">
                <Heading size="sm" py={4}>
                    Change Password
                </Heading>
                <Box as="form" display="flex" flexDirection="column" alignItems="start">
                    <FormControl>
                        <FormLabel color="gray.700">Old password</FormLabel>
                        <Input placeholder='Password' type="password" />
                    </FormControl>
                    <FormControl mt={4}>
                        <FormLabel color="gray.700">New password</FormLabel>
                        <Input placeholder='Password' type="password" />
                    </FormControl>
                    <FormControl mt={4}>
                        <FormLabel color="gray.700">Confirm new password</FormLabel>
                        <Input placeholder='Password' type="password" />
                    </FormControl>
                    <Button bg="ui.main" color="white" _hover={{ opacity: 0.8 }} mt={4} type="submit">
                        Save
                    </Button>
                </Box>
            </ Container>
        </>
    );
}
export default ChangePassword;