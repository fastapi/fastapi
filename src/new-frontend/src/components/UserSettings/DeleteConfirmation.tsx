import React from 'react';

import { AlertDialog, AlertDialogBody, AlertDialogContent, AlertDialogFooter, AlertDialogHeader, AlertDialogOverlay, Button } from '@chakra-ui/react';
import { useForm } from 'react-hook-form';
import { ApiError } from '../../client';
import useAuth from '../../hooks/useAuth';
import useCustomToast from '../../hooks/useCustomToast';
import { useUserStore } from '../../store/user-store';

interface DeleteProps {
    isOpen: boolean;
    onClose: () => void;
}

const DeleteConfirmation: React.FC<DeleteProps> = ({ isOpen, onClose }) => {
    const showToast = useCustomToast();
    const cancelRef = React.useRef<HTMLButtonElement | null>(null);
    const { handleSubmit, formState: { isSubmitting } } = useForm();
    const { user, deleteUser } = useUserStore();
    const { logout } = useAuth();

    const onSubmit = async () => {
        try {
            await deleteUser(user!.id);
            logout();
            onClose();
            showToast('Success', 'Your account has been successfully deleted.', 'success');
        } catch (err) {
            const errDetail = (err as ApiError).body.detail;
            showToast('Something went wrong.', `${errDetail}`, 'error');
        }
    }

    return (
        <>
            <AlertDialog
                isOpen={isOpen}
                onClose={onClose}
                leastDestructiveRef={cancelRef}
                size={{ base: 'sm', md: 'md' }}
                isCentered
            >
                <AlertDialogOverlay>
                    <AlertDialogContent as='form' onSubmit={handleSubmit(onSubmit)}>
                        <AlertDialogHeader>
                            Confirmation Required
                        </AlertDialogHeader>

                        <AlertDialogBody>
                            All your account data will be <strong>permanently deleted.</strong> If you are sure, please click <strong>'Confirm'</strong> to proceed.
                        </AlertDialogBody>

                        <AlertDialogFooter gap={3}>
                            <Button bg='ui.danger' color='white' _hover={{ opacity: 0.8 }} type='submit' isLoading={isSubmitting}>
                                Confirm
                            </Button>
                            <Button ref={cancelRef} onClick={onClose} isDisabled={isSubmitting}>
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




