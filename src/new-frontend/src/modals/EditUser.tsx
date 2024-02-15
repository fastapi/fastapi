import React from 'react';

import { Button, Checkbox, Flex, FormControl, FormLabel, Input, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, useDisclosure } from '@chakra-ui/react';

interface EditUserProps {
    isOpen: boolean;
    onClose: () => void;
}

const EditUser: React.FC<EditUserProps> = ({ isOpen, onClose }) => {

    return (
        <>
            <Modal
                isOpen={isOpen}
                onClose={onClose}
                size={{ base: "sm", md: "md" }}
                isCentered
            >
                <ModalOverlay />
                <ModalContent>
                    <ModalHeader>Edit User</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody pb={6}>
                        <FormControl>
                            <FormLabel>Email</FormLabel>
                            <Input placeholder='Email' type="email" />
                        </FormControl>

                        <FormControl mt={4}>
                            <FormLabel>Full name</FormLabel>
                            <Input placeholder='Full name' type="text" />
                        </FormControl>
                        <FormControl mt={4}>
                            <FormLabel>Password</FormLabel>
                            <Input placeholder='Password' type="password" />
                        </FormControl>
                        <Flex>
                            <FormControl mt={4}>
                                <Checkbox colorScheme='teal'>Is superuser?</Checkbox>
                            </FormControl>
                            <FormControl mt={4}>
                                <Checkbox colorScheme='teal'>Is active?</Checkbox>
                            </FormControl>
                        </Flex>
                    </ModalBody>

                    <ModalFooter gap={3}>
                        <Button bg="ui.main" color="white" _hover={{ opacity: 0.8 }}>
                            Save
                        </Button>
                        <Button onClick={onClose}>Cancel</Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>
        </>
    )
}

export default EditUser;