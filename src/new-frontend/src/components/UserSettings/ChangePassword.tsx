import React from 'react';

import { Box, Button, Container, FormControl, FormLabel, Heading, Input, useColorModeValue } from '@chakra-ui/react';
import { SubmitHandler, useForm } from 'react-hook-form';
import { ApiError, UpdatePassword } from '../../client';
import useCustomToast from '../../hooks/useCustomToast';
import { useUserStore } from '../../store/user-store';

interface UpdatePasswordForm extends UpdatePassword {
    confirm_password: string;
}

const ChangePassword: React.FC = () => {
    const color = useColorModeValue('gray.700', 'white');
    const showToast = useCustomToast();
    const { register, handleSubmit, reset, formState: { isSubmitting } } = useForm<UpdatePasswordForm>();
    const { editPassword } = useUserStore();

    const onSubmit: SubmitHandler<UpdatePasswordForm> = async (data) => {
        try {
            await editPassword(data);
            showToast('Success!', 'Password updated.', 'success');
            reset();
        } catch (err) {
            const errDetail = (err as ApiError).body.detail;
            showToast('Something went wrong.', `${errDetail}`, 'error');
        }

    }

    return (
        <>
            <Container maxW='full' as='form' onSubmit={handleSubmit(onSubmit)}>
                <Heading size='sm' py={4}>
                    Change Password
                </Heading>
                <Box w={{ 'sm': 'full', 'md': '50%' }}>
                    <FormControl>
                        <FormLabel color={color} htmlFor='currentPassword'>Current password</FormLabel>
                        <Input id='currentPassword' {...register('current_password')} placeholder='••••••••' type='password' />
                    </FormControl>
                    <FormControl mt={4}>
                        <FormLabel color={color} htmlFor='newPassword'>New password</FormLabel>
                        <Input id='newPassword' {...register('new_password')} placeholder='••••••••' type='password' />
                    </FormControl>
                    <FormControl mt={4}>
                        <FormLabel color={color} htmlFor='confirmPassword'>Confirm new password</FormLabel>
                        <Input id='confirmPassword' {...register('confirm_password')} placeholder='••••••••' type='password' />
                    </FormControl>
                    <Button bg='ui.main' color='white' _hover={{ opacity: 0.8 }} mt={4} type='submit' isLoading={isSubmitting}>
                        Save
                    </Button>
                </Box>
            </ Container>
        </>
    );
}
export default ChangePassword;