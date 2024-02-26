import React from 'react';

import { Button, FormControl, FormLabel, Input, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay } from '@chakra-ui/react';
import { SubmitHandler, useForm } from 'react-hook-form';

import { ApiError, ItemUpdate } from '../../client';
import useCustomToast from '../../hooks/useCustomToast';
import { useItemsStore } from '../../store/items-store';

interface EditItemProps {
    id: number;
    isOpen: boolean;
    onClose: () => void;
}

const EditItem: React.FC<EditItemProps> = ({ id, isOpen, onClose }) => {
    const showToast = useCustomToast();
    const { register, handleSubmit, reset, formState: { isSubmitting }, } = useForm<ItemUpdate>();
    const { editItem, items } = useItemsStore();

    const currentItem = items.find((item) => item.id === id);

    const onSubmit: SubmitHandler<ItemUpdate> = async (data) => {
        try {
            await editItem(id, data);
            showToast('Success!', 'Item updated successfully.', 'success');
            reset();
            onClose();
        } catch (err) {
            const errDetail = (err as ApiError).body.detail;
            showToast('Something went wrong.', `${errDetail}`, 'error');
        }
    }

    const onCancel = () => {
        reset();
        onClose();
    }

    return (
        <>
            <Modal
                isOpen={isOpen}
                onClose={onClose}
                size={{ base: 'sm', md: 'md' }}
                isCentered
            >
                <ModalOverlay />
                <ModalContent as='form' onSubmit={handleSubmit(onSubmit)}>
                    <ModalHeader>Edit Item</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody pb={6}>
                        <FormControl>
                            <FormLabel htmlFor='title'>Title</FormLabel>
                            <Input id='title' {...register('title')} defaultValue={currentItem?.title} type='text' />
                        </FormControl>
                        <FormControl mt={4}>
                            <FormLabel htmlFor='description'>Description</FormLabel>
                            <Input id='description' {...register('description')} defaultValue={currentItem?.description} placeholder='Description' type='text' />
                        </FormControl>
                    </ModalBody>
                    <ModalFooter gap={3}>
                        <Button bg='ui.main' color='white' _hover={{ opacity: 0.8 }} type='submit' isLoading={isSubmitting}>
                            Save
                        </Button>
                        <Button onClick={onCancel}>Cancel</Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>
        </>
    )
}

export default EditItem;