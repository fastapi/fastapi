import {
  Button,
  Container,
  FormControl,
  FormErrorMessage,
  Heading,
  Input,
  Text,
} from '@chakra-ui/react'
import { createFileRoute, redirect } from '@tanstack/react-router'
import { SubmitHandler, useForm } from 'react-hook-form'

import { LoginService } from '../client'
import useCustomToast from '../hooks/useCustomToast'
import { isLoggedIn } from '../hooks/useAuth'

interface FormData {
  email: string
}

export const Route = createFileRoute('/recover-password')({
  component: RecoverPassword,
  beforeLoad: async () => {
    if (isLoggedIn()) {
      throw redirect({
        to: '/',
      })
    }
  },
})

function RecoverPassword() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>()
  const showToast = useCustomToast()

  const onSubmit: SubmitHandler<FormData> = async (data) => {
    await LoginService.recoverPassword({
      email: data.email,
    })
    showToast(
      'Email sent.',
      'We sent an email with a link to get back into your account.',
      'success',
    )
  }

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
        Password Recovery
      </Heading>
      <Text align="center">
        A password recovery email will be sent to the registered account.
      </Text>
      <FormControl isInvalid={!!errors.email}>
        <Input
          id="email"
          {...register('email', {
            required: 'Email is required',
            pattern: {
              value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i,
              message: 'Invalid email address',
            },
          })}
          placeholder="Email"
          type="email"
        />
        {errors.email && (
          <FormErrorMessage>{errors.email.message}</FormErrorMessage>
        )}
      </FormControl>
      <Button
        bg="ui.main"
        color="white"
        _hover={{ opacity: 0.8 }}
        type="submit"
        isLoading={isSubmitting}
      >
        Continue
      </Button>
    </Container>
  )
}

export default RecoverPassword
