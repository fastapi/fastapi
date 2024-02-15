import React, { useState } from 'react';

import { AlertDialog, AlertDialogBody, AlertDialogContent, AlertDialogFooter, AlertDialogHeader, AlertDialogOverlay, Button, useToast } from '@chakra-ui/react';
import { useForm } from 'react-hook-form';

import { useItemsStore } from '../store/items-store';
import { useUsersStore } from '../store/users-store';

interface DeleteProps {
    type: string;
    id: number
    isOpen: boolean;
    onClose: () => void;
}

const Delete: React.FC<DeleteProps> = ({ type, id, isOpen, onClose }) => {
    const toast = useToast();
    const cancelRef = React.useRef<HTMLButtonElement | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const { handleSubmit } = useForm();
    const { deleteItem } = useItemsStore();
    const { deleteUser } = useUsersStore();

    const onSubmit = async () => {
        setIsLoading(true);
        try {
            type === 'Item' ? await deleteItem(id) : await deleteUser(id);
            toast({
                title: "Success",
                description: `The ${type.toLowerCase()} was deleted successfully.`,
                status: "success",
                isClosable: true,
            });
            onClose();
        } catch (err) {
            toast({
                title: "An error occurred.",
                description: `An error occurred while deleting the ${type.toLowerCase()}.`,
                status: "error",
                isClosable: true,
            });
        } finally {
            setIsLoading(false);
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
                        <AlertDialogHeader fontSize='lg' fontWeight='bold'>
                            Delete {type}
                        </AlertDialogHeader>

                        <AlertDialogBody>
                            Are you sure? You will not be able to undo this action.
                        </AlertDialogBody>

                        <AlertDialogFooter gap={3}>
                            <Button bg="ui.danger" color="white" _hover={{ opacity: 0.8 }} type="submit" isLoading={isLoading}>
                                Delete
                            </Button>
                            <Button ref={cancelRef} onClick={onClose} isDisabled={isLoading}>
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