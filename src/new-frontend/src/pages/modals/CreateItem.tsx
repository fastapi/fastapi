import React, { useState } from 'react';

import { Button, FormControl, FormLabel, Input, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, useToast } from '@chakra-ui/react';
import { SubmitHandler, useForm } from 'react-hook-form';

import { ItemCreate } from '../../client';
import { useItemsStore } from '../../store/items-store';

interface CreateItemProps {
    isOpen: boolean;
    onClose: () => void;
}

const CreateItem: React.FC<CreateItemProps> = ({ isOpen, onClose }) => {
    const toast = useToast();
    const [isLoading, setIsLoading] = useState(false);
    const { register, handleSubmit } = useForm<ItemCreate>();
    const { addItem } = useItemsStore();

    const onSubmit: SubmitHandler<ItemCreate> = async (data) => {
        try {
            setIsLoading(true);
            await addItem(data);
            setIsLoading(false);

            toast({
                title: 'Success!',
                description: 'Item created successfully.',
                status: 'success',
                isClosable: true,
            });
            onClose();
        } catch (err) {
            setIsLoading(false);
            toast({
                title: 'Something went wrong.',
                description: 'Failed to create item. Please try again.',
                status: 'error',
                isClosable: true,
            });
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
                    <ModalHeader>Create Item</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody pb={6}>
                        <FormControl>
                            <FormLabel>Title</FormLabel>
                            <Input
                                {...register('title')}
                                placeholder="Title"

                            />
                        </FormControl>
                        <FormControl mt={4}>
                            <FormLabel>Description</FormLabel>
                            <Input
                                {...register('description')}
                                placeholder="Description"

                            />
                        </FormControl>
                    </ModalBody>

                    <ModalFooter gap={3}>
                        <Button bg="ui.main" color="white" type="submit" isLoading={isLoading}>
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

export default CreateItem;
