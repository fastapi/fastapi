import React, { useState } from 'react';

import { Box, Button, Checkbox, Flex, FormControl, FormLabel, Input, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, Spinner, useToast } from '@chakra-ui/react';
import { SubmitHandler, useForm } from 'react-hook-form';

import { UserCreate } from '../../client';
import { useUsersStore } from '../../store/users-store';

interface CreateUserProps {
    isOpen: boolean;
    onClose: () => void;
}

const CreateUser: React.FC<CreateUserProps> = ({ isOpen, onClose }) => {
    const toast = useToast();
    const [isLoading, setIsLoading] = useState(false);
    const { register, handleSubmit } = useForm<UserCreate>();
    const { addUser } = useUsersStore();

    const onSubmit: SubmitHandler<UserCreate> = async (data) => {
        try {
            setIsLoading(true);
            await addUser(data);
            setIsLoading(false);
            toast({
                title: 'Success!',
                description: 'User created successfully.',
                status: 'success',
                isClosable: true,
            });
            onClose();

        } catch (err) {
            setIsLoading(false);
            toast({
                title: 'Something went wrong.',
                description: 'Failed to create user. Please try again.',
                status: 'error',
                isClosable: true,
            });
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
                    <ModalHeader>Create User</ModalHeader>
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
                            <Input placeholder='Password' type="password" />
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

export default CreateUser;