import React from 'react';

import { Button, Checkbox, Flex, FormControl, FormLabel, Input, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay } from '@chakra-ui/react';
import { SubmitHandler, useForm } from 'react-hook-form';

import { ApiError, UserUpdate } from '../../client';
import useCustomToast from '../../hooks/useCustomToast';
import { useUsersStore } from '../../store/users-store';

interface EditUserProps {
    user_id: number;
    isOpen: boolean;
    onClose: () => void;
}

interface UserUpdateForm extends UserUpdate {
    confirm_password: string;
}

const EditUser: React.FC<EditUserProps> = ({ user_id, isOpen, onClose }) => {
    const showToast = useCustomToast();
    const { register, handleSubmit, reset, formState: { isSubmitting } } = useForm<UserUpdateForm>();
    const { editUser, users } = useUsersStore();

    const currentUser = users.find((user) => user.id === user_id);

    const onSubmit: SubmitHandler<UserUpdateForm> = async (data) => {
        if (data.password === data.confirm_password) {
            try {
                await editUser(user_id, data);
                showToast('Success!', 'User updated successfully.', 'success');
                reset();
                onClose();
            } catch (err) {
                const errDetail = (err as ApiError).body.detail;
                showToast('Something went wrong.', `${errDetail}`, 'error');
            }
        } else {
            // TODO: Complete when form validation is implemented
            console.log("Passwords don't match")
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
                    <ModalHeader>Edit User</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody pb={6}>
                        <FormControl>
                            <FormLabel htmlFor='email'>Email</FormLabel>
                            <Input id="email" {...register('email')} defaultValue={currentUser?.email} type='email' />
                        </FormControl>
                        <FormControl mt={4}>
                            <FormLabel htmlFor='name'>Full name</FormLabel>
                            <Input id="name" {...register('full_name')} defaultValue={currentUser?.full_name} type='text' />
                        </FormControl>
                        <FormControl mt={4}>
                            <FormLabel htmlFor='password'>Password</FormLabel>
                            <Input id="password" {...register('password')} placeholder='••••••••' type='password' />
                        </FormControl>
                        <FormControl mt={4}>
                            <FormLabel htmlFor='confirmPassword'>Confirmation Password</FormLabel>
                            <Input id='confirmPassword' {...register('confirm_password')} placeholder='••••••••' type='password' />
                        </FormControl>
                        <Flex>
                            <FormControl mt={4}>
                                <Checkbox {...register('is_superuser')} defaultChecked={currentUser?.is_superuser} colorScheme='teal'>Is superuser?</Checkbox>
                            </FormControl>
                            <FormControl mt={4}>
                                <Checkbox {...register('is_active')} defaultChecked={currentUser?.is_active} colorScheme='teal'>Is active?</Checkbox>
                            </FormControl>
                        </Flex>
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

export default EditUser;