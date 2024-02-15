import React, { useState } from 'react';

import { Button, FormControl, FormLabel, Input, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, useToast } from '@chakra-ui/react';
import { SubmitHandler, useForm } from 'react-hook-form';

import { ItemCreate } from '../client';
import { useItemsStore } from '../store/items-store';

interface AddItemProps {
    isOpen: boolean;
    onClose: () => void;
}

const AddItem: React.FC<AddItemProps> = ({ isOpen, onClose }) => {
    const toast = useToast();
    const [isLoading, setIsLoading] = useState(false);
    const { register, handleSubmit, reset } = useForm<ItemCreate>();
    const { addItem } = useItemsStore();

    const onSubmit: SubmitHandler<ItemCreate> = async (data) => {
        setIsLoading(true);
        try {
            await addItem(data);
            toast({
                title: 'Success!',
                description: 'Item created successfully.',
                status: 'success',
                isClosable: true,
            });
            reset();
            onClose();
        } catch (err) {
            toast({
                title: 'Something went wrong.',
                description: 'Failed to create item. Please try again.',
                status: 'error',
                isClosable: true,
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <>
            <Modal
                isOpen={isOpen}
                onClose={onClose}
                size={{ base: 'sm', md: 'md' }}
                isCentered
            >
                <ModalOverlay />
                <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
                    <ModalHeader>Add Item</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody pb={6}>
                        <FormControl>
                            <FormLabel>Title</FormLabel>
                            <Input
                                {...register('title')}
                                placeholder="Title"
                                type="text"
                            />
                        </FormControl>
                        <FormControl mt={4}>
                            <FormLabel>Description</FormLabel>
                            <Input
                                {...register('description')}
                                placeholder="Description"
                                type="text"
                            />
                        </FormControl>
                    </ModalBody>

                    <ModalFooter gap={3}>
                        <Button bg="ui.main" color="white" _hover={{ opacity: 0.8 }} type="submit" isLoading={isLoading}>
                            Save
                        </Button>
                        <Button onClick={onClose} isDisabled={isLoading}>
                            Cancel
                        </Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>
        </>
    );
};

export default AddItem;
