import React, { useState } from 'react';

import { AlertDialog, AlertDialogBody, AlertDialogContent, AlertDialogFooter, AlertDialogHeader, AlertDialogOverlay, Button } from '@chakra-ui/react';
import { useForm } from 'react-hook-form';

import { useItemsStore } from '../../store/items-store';

interface DeleteProps {
    toDelete: string;
    id: number
    isOpen: boolean;
    onClose: () => void;
}

const Delete: React.FC<DeleteProps> = ({ toDelete, id, isOpen, onClose }) => {
    const cancelRef = React.useRef<HTMLButtonElement | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const { handleSubmit } = useForm();
    const { deleteItem } = useItemsStore();

    const onSubmit = async () => {
        try {
            setIsLoading(true);
            await deleteItem(id);
            setIsLoading(false);
            onClose();
        } catch (err) {
            setIsLoading(false);
            console.error(err);

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
                            Delete {toDelete}
                        </AlertDialogHeader>

                        <AlertDialogBody>
                            Are you sure? You will not be able to undo this action.
                        </AlertDialogBody>

                        <AlertDialogFooter gap={3}>
                            <Button colorScheme='red' type="submit" isLoading={isLoading}>
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