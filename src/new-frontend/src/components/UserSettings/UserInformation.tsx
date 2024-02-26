import React, { useState } from 'react';

import { Box, Button, Container, Flex, FormControl, FormLabel, Heading, Input, Text, useColorModeValue } from '@chakra-ui/react';

import { SubmitHandler, useForm } from 'react-hook-form';
import { ApiError, UserOut, UserUpdateMe } from '../../client';
import useCustomToast from '../../hooks/useCustomToast';
import { useUserStore } from '../../store/user-store';
import { useUsersStore } from '../../store/users-store';

const UserInformation: React.FC = () => {
    const color = useColorModeValue('gray.700', 'white');
    const showToast = useCustomToast();
    const [editMode, setEditMode] = useState(false);
    const { register, handleSubmit, reset, formState: { isSubmitting } } = useForm<UserOut>();
    const { user, editUser } = useUserStore();
    const { getUsers } = useUsersStore();

    const toggleEditMode = () => {
        setEditMode(!editMode);
    };

    const onSubmit: SubmitHandler<UserUpdateMe> = async (data) => {
        try {
            await editUser(data);
            await getUsers()
            showToast('Success!', 'User updated successfully.', 'success');
        } catch (err) {
            const errDetail = (err as ApiError).body.detail;
            showToast('Something went wrong.', `${errDetail}`, 'error');
        }
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
                                <Input id='name' {...register('full_name')} defaultValue={user?.full_name} type='text' size='md' /> :
                                <Text size='md' py={2}>
                                    {user?.full_name || 'N/A'}
                                </Text>
                        }
                    </FormControl>
                    <FormControl mt={4}>
                        <FormLabel color={color} htmlFor='email'>Email</FormLabel>
                        {
                            editMode ?
                                <Input id='email' {...register('email')} defaultValue={user?.email} type='text' size='md' /> :
                                <Text size='md' py={2}>
                                    {user?.email || 'N/A'}
                                </Text>
                        }
                    </FormControl>
                    <Flex mt={4} gap={3}>
                        <Button
                            bg='ui.main'
                            color='white'
                            _hover={{ opacity: 0.8 }}
                            onClick={toggleEditMode}
                            type={editMode ? 'button' : 'submit'}
                            isLoading={editMode ? isSubmitting : false}
                        >
                            {editMode ? 'Save' : 'Edit'}
                        </Button>
                        {editMode &&
                            <Button onClick={onCancel}>
                                Cancel
                            </Button>}
                    </Flex>
                </Box>
            </ Container>
        </>
    );
}

export default UserInformation;