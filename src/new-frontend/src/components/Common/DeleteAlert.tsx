import React, { useState } from 'react';

import { AlertDialog, AlertDialogBody, AlertDialogContent, AlertDialogFooter, AlertDialogHeader, AlertDialogOverlay, Button } from '@chakra-ui/react';
import { useForm } from 'react-hook-form';

import useCustomToast from '../../hooks/useCustomToast';
import { useItemsStore } from '../../store/items-store';
import { useUsersStore } from '../../store/users-store';

interface DeleteProps {
    type: string;
    id: number
    isOpen: boolean;
    onClose: () => void;
}

const Delete: React.FC<DeleteProps> = ({ type, id, isOpen, onClose }) => {
    const showToast = useCustomToast();
    const cancelRef = React.useRef<HTMLButtonElement | null>(null);
    const { handleSubmit, formState: {isSubmitting} } = useForm();
    const { deleteItem } = useItemsStore();
    const { deleteUser } = useUsersStore();

    const onSubmit = async () => {
        try {
            type === 'Item' ? await deleteItem(id) : await deleteUser(id);
            showToast('Success', `The ${type.toLowerCase()} was deleted successfully.`, 'success');
            onClose();
        } catch (err) {
            showToast('An error occurred.', `An error occurred while deleting the ${type.toLowerCase()}.`, 'error');
        }
    }

    return (
        <>
            <AlertDialog
                isOpen={isOpen}
                onClose={onClose}
                leastDestructiveRef={cancelRef}
                size={{ base: "sm", md: "md" }}
                isCentered
            >
                <AlertDialogOverlay>
                    <AlertDialogContent as="form" onSubmit={handleSubmit(onSubmit)}>
                        <AlertDialogHeader>
                            Delete {type}
                        </AlertDialogHeader>

                        <AlertDialogBody>
                            {type === 'User' && <span>All items associated with this user will also be <strong>permantly deleted. </strong></span>}
                            Are you sure? You will not be able to undo this action.
                        </AlertDialogBody>

                        <AlertDialogFooter gap={3}>
                            <Button bg="ui.danger" color="white" _hover={{ opacity: 0.8 }} type="submit" isLoading={isSubmitting}>
                                Delete
                            </Button>
                            <Button ref={cancelRef} onClick={onClose} isDisabled={isSubmitting}>
                                Cancel
                            </Button>
                        </AlertDialogFooter>
                    </AlertDialogContent>
                </AlertDialogOverlay>
            </AlertDialog>
        </>
    )
}

export default Delete;