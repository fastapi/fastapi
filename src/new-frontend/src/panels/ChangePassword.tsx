import React from 'react';

import { Box, Button, Container, FormControl, FormLabel, Heading, Input, useColorModeValue } from '@chakra-ui/react';

const ChangePassword: React.FC = () => {
    const color = useColorModeValue("gray.700", "white");

    return (
        <>
            <Container maxW="full">
                <Heading size="sm" py={4}>
                    Change Password
                </Heading>
                <Box as="form" display="flex" flexDirection="column" alignItems="start">
                    <FormControl>
                        <FormLabel color={color}>Old password</FormLabel>
                        <Input placeholder='Password' type="password" />
                    </FormControl>
                    <FormControl mt={4}>
                        <FormLabel color={color}>New password</FormLabel>
                        <Input placeholder='Password' type="password" />
                    </FormControl>
                    <FormControl mt={4}>
                        <FormLabel color={color}>Confirm new password</FormLabel>
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