import React from 'react';

import { Container, Heading, Radio, RadioGroup, Stack, useColorMode } from '@chakra-ui/react';

const Appearance: React.FC = () => {
    const { colorMode, toggleColorMode } = useColorMode();

    return (
        <>
            <Container maxW="full">
                <Heading size="sm" py={4}>
                    Appearance
                </Heading>
                <RadioGroup onChange={toggleColorMode} value={colorMode}>
                    <Stack>
                        <Radio value="light" colorScheme="teal">
                            Light <i>(default)</i>
                        </Radio>
                        <Radio value="dark" colorScheme="teal">
                            Dark
                        </Radio>
                    </Stack>
                </RadioGroup>
            </Container>
        </>
    );
}
export default Appearance;