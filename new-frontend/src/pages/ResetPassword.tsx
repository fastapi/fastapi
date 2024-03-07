import React from "react";

import { Button, Container, FormControl, FormErrorMessage, FormLabel, Heading, Input, Text } from "@chakra-ui/react";
import { SubmitHandler, useForm } from "react-hook-form";

import { LoginService, NewPassword } from "../client";
import useCustomToast from "../hooks/useCustomToast";

interface NewPasswordForm extends NewPassword {
    confirm_password: string;
}

const ResetPassword: React.FC = () => {
    const { register, handleSubmit, getValues, formState: { errors } } = useForm<NewPasswordForm>({
        mode: 'onBlur',
        criteriaMode: 'all',
        defaultValues: {
            new_password: '',
        }
    });
    const showToast = useCustomToast();

    const onSubmit: SubmitHandler<NewPasswordForm> = async (data) => {
        try {
            const token = new URLSearchParams(window.location.search).get('token');
            await LoginService.resetPassword({
                requestBody: { new_password: data.new_password, token: token! }
            });
            showToast("Password reset.", "Your password has been reset successfully.", "success");
        } catch (error) {
            showToast("Error", "An error occurred while resetting your password.", "error");
        }
    };

    return (
        <Container
            as="form"
            onSubmit={handleSubmit(onSubmit)}
            h="100vh"
            maxW="sm"
            alignItems="stretch"
            justifyContent="center"
            gap={4}
            centerContent
        >
            <Heading size="xl" color="ui.main" textAlign="center" mb={2}>
                Reset Password
            </Heading>
            <Text textAlign="center">
                Please enter your new password and confirm it to reset your password.
            </Text>
            <FormControl mt={4} isInvalid={!!errors.new_password}>
                <FormLabel htmlFor='password'>Set Password</FormLabel>
                <Input id='password' {...register('new_password', { required: 'Password is required', minLength: { value: 8, message: 'Password must be at least 8 characters' } })} placeholder='Password' type='password' />
                {errors.new_password && <FormErrorMessage>{errors.new_password.message}</FormErrorMessage>}
            </FormControl>
            <FormControl mt={4} isInvalid={!!errors.confirm_password}>
                <FormLabel htmlFor='confirm_password'>Confirm Password</FormLabel>
                <Input id='confirm_password' {...register('confirm_password', {
                    required: 'Please confirm your password',
                    validate: value => value === getValues().new_password || 'The passwords do not match'
                })} placeholder='Password' type='password' />
                {errors.confirm_password && <FormErrorMessage>{errors.confirm_password.message}</FormErrorMessage>}
            </FormControl>
            <Button bg="ui.main" color="white" _hover={{ opacity: 0.8 }} type="submit">
                Reset Password
            </Button>
        </Container>
    );
};

export default ResetPassword;