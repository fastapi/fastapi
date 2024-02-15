import React, { useState } from 'react';

import { Button, Checkbox, Flex, FormControl, FormLabel, Input, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, useToast } from '@chakra-ui/react';
import { SubmitHandler, useForm } from 'react-hook-form';

import { UserCreate } from '../client';
import { useUsersStore } from '../store/users-store';

interface AddUserProps {
    isOpen: boolean;
    onClose: () => void;
}

const AddUser: React.FC<AddUserProps> = ({ isOpen, onClose }) => {
    const toast = useToast();
    const [isLoading, setIsLoading] = useState(false);
    const { register, handleSubmit, reset } = useForm<UserCreate>();
    const { addUser } = useUsersStore();

    const onSubmit: SubmitHandler<UserCreate> = async (data) => {
        setIsLoading(true);
        try {
            await addUser(data);
            toast({
                title: 'Success!',
                description: 'User created successfully.',
                status: 'success',
                isClosable: true,
            });
            reset();
            onClose();

        } catch (err) {
            toast({
                title: 'Something went wrong.',
                description: 'Failed to create user. Please try again.',
                status: 'error',
                isClosable: true,
            });
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <>
            <Modal
                isOpen={isOpen}
                onClose={onClose}
                size={{ base: "sm", md: "md" }}
                isCentered
            >
                <ModalOverlay />
                <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
                    {/* TODO: Check passwords */}
                    <ModalHeader>Add User</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody pb={6}>
                        <FormControl>
                            <FormLabel>Email</FormLabel>
                            <Input {...register('email')} placeholder='Email' type="email" />
                        </FormControl>
                        <FormControl mt={4}>
                            <FormLabel>Full name</FormLabel>
                            <Input {...register('full_name')} placeholder='Full name' type="text" />
                        </FormControl>
                        <FormControl mt={4}>
                            <FormLabel>Set Password</FormLabel>
                            <Input {...register('password')} placeholder='Password' type="password" />
                        </FormControl>
                        <FormControl mt={4}>
                            <FormLabel>Confirm Password</FormLabel>
                            <Input {...register('confirmPassword')} placeholder='Password' type="password" />
                        </FormControl>
                        <Flex>
                            <FormControl mt={4}>
                                <Checkbox {...register('is_superuser')} colorScheme='teal'>Is superuser?</Checkbox>
                            </FormControl>
                            <FormControl mt={4}>
                                <Checkbox {...register('is_active')} colorScheme='teal'>Is active?</Checkbox>
                            </FormControl>
                        </Flex>
                    </ModalBody>

                    <ModalFooter gap={3}>
                        <Button bg="ui.main" color="white" type="submit" isLoading={isLoading}>
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