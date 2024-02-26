import React from 'react';

import { Button, Checkbox, Flex, FormControl, FormLabel, Input, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay } from '@chakra-ui/react';
import { SubmitHandler, useForm } from 'react-hook-form';

import { UserCreate } from '../../client';
import useCustomToast from '../../hooks/useCustomToast';
import { useUsersStore } from '../../store/users-store';
import { ApiError } from '../../client/core/ApiError';

interface AddUserProps {
    isOpen: boolean;
    onClose: () => void;
}

interface UserCreateForm extends UserCreate {
    confirmPassword: string;

}

const AddUser: React.FC<AddUserProps> = ({ isOpen, onClose }) => {
    const showToast = useCustomToast();
    const { register, handleSubmit, reset, formState: { isSubmitting } } = useForm<UserCreateForm>();
    const { addUser } = useUsersStore();

    const onSubmit: SubmitHandler<UserCreateForm> = async (data) => {
        if (data.password === data.confirmPassword) {
            try {
                await addUser(data);
                showToast('Success!', 'User created successfully.', 'success');
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
                    <ModalHeader>Add User</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody pb={6} >
                        <FormControl>
                            <FormLabel htmlFor='email'>Email</FormLabel>
                            <Input id='email' {...register('email')} placeholder='Email' type='email' />
                        </FormControl>
                        <FormControl mt={4}>
                            <FormLabel htmlFor='name'>Full name</FormLabel>
                            <Input id='name' {...register('full_name')} placeholder='Full name' type='text' />
                        </FormControl>
                        <FormControl mt={4}>
                            <FormLabel htmlFor='password'>Set Password</FormLabel>
                            <Input id='password' {...register('password')} placeholder='Password' type='password' />
                        </FormControl>
                        <FormControl mt={4}>
                            <FormLabel htmlFor='confirmPassword'>Confirm Password</FormLabel>
                            <Input id='confirmPassword' {...register('confirmPassword')} placeholder='Password' type='password' />
                        </FormControl>
                        <Flex mt={4}>
                            <FormControl>
                                <Checkbox {...register('is_superuser')} colorScheme='teal'>Is superuser?</Checkbox>
                            </FormControl>
                            <FormControl>
                                <Checkbox {...register('is_active')} colorScheme='teal'>Is active?</Checkbox>
                            </FormControl>
                        </Flex>
                    </ModalBody>
                    <ModalFooter gap={3}>
                        <Button bg='ui.main' color='white' type='submit' isLoading={isSubmitting}>
                            Save
                        </Button>
                        <Button onClick={onClose}>Cancel</Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>
        </>
    )
}

export default AddUser;