import React, { useState } from 'react';

import { AlertDialog, AlertDialogBody, AlertDialogContent, AlertDialogFooter, AlertDialogHeader, AlertDialogOverlay, Button, useToast } from '@chakra-ui/react';
import { useForm } from 'react-hook-form';

interface DeleteProps {
    isOpen: boolean;
    onClose: () => void;
}

const DeleteConfirmation: React.FC<DeleteProps> = ({ isOpen, onClose }) => {
    const toast = useToast();
    const cancelRef = React.useRef<HTMLButtonElement | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const { handleSubmit } = useForm();

    const onSubmit = async () => {
        setIsLoading(true);
        try {
            // TODO: Delete user account when API is ready
            onClose();
        } catch (err) {
            toast({
                title: "An error occurred.",
                description: `An error occurred while deleting your account.`,
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
                        <AlertDialogHeader>
                            Confirmation Required
                        </AlertDialogHeader>

                        <AlertDialogBody>
                            All your account data will be <b>permanently deleted.</b> If you're sure, please click <b>'Confirm'</b> to proceed.
                        </AlertDialogBody>

                        <AlertDialogFooter gap={3}>
                            <Button bg="ui.danger" color="white" _hover={{ opacity: 0.8 }} type="submit" isLoading={isLoading}>
                                Confirm
                            </Button>
                            <Button ref={cancelRef} onClick={onClose} isDisabled={isLoading}>
                                Cancel
                            </Button>
                        </AlertDialogFooter>
                    </AlertDialogContent>
                </AlertDialogOverlay>
            </AlertDialog >
        </>
    )
}

export default DeleteConfirmation;




