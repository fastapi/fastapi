import { Button, Container, Text } from "@chakra-ui/react";

import { Link } from "react-router-dom";

const NotFound = () => (
    <>
        <Container h="100vh"
            alignItems="stretch"
            justifyContent="center" textAlign="center" maxW="xs" centerContent>
            <Text fontSize="8xl" color="ui.main" fontWeight="bold" lineHeight="1" mb={4}>404</Text>
            <Text fontSize="md">Houston, we have a problem.</Text>
            <Text fontSize="md">It looks like the page you're looking for doesn't exist.</Text>
            <Button as={Link} to="/" color="ui.main" borderColor="ui.main" variant="outline" mt={4}>Go back to Home</Button>
        </Container>
    </>
);

export default NotFound;
