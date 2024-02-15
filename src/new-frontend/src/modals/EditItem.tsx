import React from 'react';

import { Button, FormControl, FormLabel, Input, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay } from '@chakra-ui/react';

interface EditItemProps {
    isOpen: boolean;
    onClose: () => void;
}

const EditItem: React.FC<EditItemProps> = ({ isOpen, onClose }) => {

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
                    <ModalHeader>Edit Item</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody pb={6}>
                        <FormControl>
                            <FormLabel>Item</FormLabel>
                            <Input placeholder='Item' type="text" />
                        </FormControl>

                        <FormControl mt={4}>
                            <FormLabel>Description</FormLabel>
                            <Input placeholder='Description' type="text" />
                        </FormControl>
                    </ModalBody>

                    <ModalFooter gap={3}>
                        <Button colorScheme='teal'>
                            Save
                        </Button>
                        <Button onClick={onClose}>Cancel</Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>
        </>
    )
}

export default EditItem;