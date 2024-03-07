import React, { useState } from 'react';

import { Box, Button, Container, Flex, FormControl, FormErrorMessage, FormLabel, Heading, Input, Text, useColorModeValue } from '@chakra-ui/react';
import { SubmitHandler, useForm } from 'react-hook-form';
import { useMutation, useQueryClient } from 'react-query';

import { ApiError, UserOut, UserUpdateMe, UsersService } from '../../client';
import useAuth from '../../hooks/useAuth';
import useCustomToast from '../../hooks/useCustomToast';

const UserInformation: React.FC = () => {
    const queryClient = useQueryClient();
    const color = useColorModeValue('gray.700', 'white');
    const showToast = useCustomToast();
    const [editMode, setEditMode] = useState(false);
    const { user: currentUser } = useAuth();
    const { register, handleSubmit, reset, formState: { isSubmitting, errors, isDirty } } = useForm<UserOut>({
        mode: 'onBlur', criteriaMode: 'all', defaultValues: {
            full_name: currentUser?.full_name,
            email: currentUser?.email
        }
    })

    const toggleEditMode = () => {
        setEditMode(!editMode);
    };

    const updateInfo = async (data: UserUpdateMe) => {
        await UsersService.updateUserMe({ requestBody: data })
    }

    const mutation = useMutation(updateInfo, {
        onSuccess: () => {
            showToast('Success!', 'User updated successfully.', 'success');
        },
        onError: (err: ApiError) => {
            const errDetail = err.body.detail;
            showToast('Something went wrong.', `${errDetail}`, 'error');
        },
        onSettled: () => {
            queryClient.invalidateQueries('users');
            queryClient.invalidateQueries('currentUser');
        }
    });

    const onSubmit: SubmitHandler<UserUpdateMe> = async (data) => {
        mutation.mutate(data)
    }

    const onCancel = () => {
        reset();
        toggleEditMode();
    }

    return (
        <>
            <Container maxW='full' as='form' onSubmit={handleSubmit(onSubmit)}>
                <Heading size='sm' py={4}>
                    User Information
                </Heading>
                <Box w={{ 'sm': 'full', 'md': '50%' }}>
                    <FormControl>
                        <FormLabel color={color} htmlFor='name'>Full name</FormLabel>
                        {
                            editMode ?
                                <Input id='name' {...register('full_name', { maxLength: 30 })} type='text' size='md' /> :
                                <Text size='md' py={2}>
                                    {currentUser?.full_name || 'N/A'}
                                </Text>
                        }
                    </FormControl>
                    <FormControl mt={4} isInvalid={!!errors.email}>
                        <FormLabel color={color} htmlFor='email'>Email</FormLabel>
                        {
                            editMode ?
                                <Input id='email' {...register('email', { required: 'Email is required', pattern: { value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i, message: 'Invalid email address' } })} type='text' size='md' /> :
                                <Text size='md' py={2}>
                                    {currentUser!.email}
                                </Text>
                        }
                        {errors.email && <FormErrorMessage>{errors.email.message}</FormErrorMessage>}
                    </FormControl>
                    <Flex mt={4} gap={3}>
                        <Button
                            bg='ui.main'
                            color='white'
                            _hover={{ opacity: 0.8 }}
                            onClick={toggleEditMode}
                            type={editMode ? 'button' : 'submit'}
                            isLoading={editMode ? isSubmitting : false}
                            isDisabled={editMode ? !isDirty : false}
                        >
                            {editMode ? 'Save' : 'Edit'}
                        </Button>
                        {editMode &&
                            <Button onClick={onCancel} isDisabled={isSubmitting}>
                                Cancel
                            </Button>}
                    </Flex>
                </Box>
            </ Container>
        </>
    );
}

export default UserInformation;