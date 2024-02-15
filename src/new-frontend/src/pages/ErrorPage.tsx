import { Button, Container, Text } from "@chakra-ui/react";

import { Link, useRouteError } from "react-router-dom";

const ErrorPage: React.FC = () => {
    const error = useRouteError();
    console.log(error);

    return (
        <>
            <Container h="100vh"
                alignItems="stretch"
                justifyContent="center" textAlign="center" maxW="xs" centerContent>
                <Text fontSize="8xl" color="ui.main" fontWeight="bold" lineHeight="1" mb={4}>Oops!</Text>
                <Text fontSize="md">Houston, we have a problem.</Text>
                <Text fontSize="md">An unexpected error has occurred.</Text>
                <Text color="ui.danger"><i>{error.statusText || error.message}</i></Text>
                <Button as={Link} to="/" color="ui.main" borderColor="ui.main" variant="outline" mt={4}>Go back to Home</Button>
            </Container>
        </>
    );
}

export default ErrorPage;


