import React from 'react';

import { Button, Container, Heading, Radio, RadioGroup, Stack } from '@chakra-ui/react';

const Appearance: React.FC = () => {
    const [value, setValue] = React.useState('system');

    return (
        <>
            <Container maxW="full">
                <Heading size="sm" py={4}>
                    Appearance
                </Heading>
                <RadioGroup onChange={setValue} value={value}>
                    <Stack>
                        <Radio value="system" colorScheme="teal" defaultChecked>
                            Use system settings (default)
                        </Radio>
                        <Radio value="light" colorScheme="teal">
                            Light
                        </Radio>
                        <Radio value="dark" colorScheme="teal">
                            Dark
                        </Radio>
                    </Stack>
                </RadioGroup>
                <Button bg="ui.main" color="white" _hover={{ opacity: 0.8 }} mt={4}>Save</Button>
            </ Container>
        </>
    );
}
export default Appearance;