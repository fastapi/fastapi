import React from 'react'
import {
  Button,
  Checkbox,
  Flex,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
} from '@chakra-ui/react'
import { SubmitHandler, useForm } from 'react-hook-form'
import { useMutation, useQueryClient } from 'react-query'

import { ApiError, UserOut, UserUpdate, UsersService } from '../../client'
import useCustomToast from '../../hooks/useCustomToast'

interface EditUserProps {
  user: UserOut
  isOpen: boolean
  onClose: () => void
}

interface UserUpdateForm extends UserUpdate {
  confirm_password: string
}

const EditUser: React.FC<EditUserProps> = ({ user, isOpen, onClose }) => {
  const queryClient = useQueryClient()
  const showToast = useCustomToast()

  const {
    register,
    handleSubmit,
    reset,
    getValues,
    formState: { errors, isSubmitting, isDirty },
  } = useForm<UserUpdateForm>({
    mode: 'onBlur',
    criteriaMode: 'all',
    defaultValues: user,
  })

  const updateUser = async (data: UserUpdateForm) => {
    await UsersService.updateUser({ userId: user.id, requestBody: data })
  }

  const mutation = useMutation(updateUser, {
    onSuccess: () => {
      showToast('Success!', 'User updated successfully.', 'success')
      onClose()
    },
    onError: (err: ApiError) => {
      const errDetail = err.body.detail
      showToast('Something went wrong.', `${errDetail}`, 'error')
    },
    onSettled: () => {
      queryClient.invalidateQueries('users')
    },
  })

  const onSubmit: SubmitHandler<UserUpdateForm> = async (data) => {
    if (data.password === '') {
      delete data.password
    }
    mutation.mutate(data)
  }

  const onCancel = () => {
    reset()
    onClose()
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
        <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
          <ModalHeader>Edit User</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <FormControl isInvalid={!!errors.email}>
              <FormLabel htmlFor="email">Email</FormLabel>
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
            <FormControl mt={4}>
              <FormLabel htmlFor="name">Full name</FormLabel>
              <Input id="name" {...register('full_name')} type="text" />
            </FormControl>
            <FormControl mt={4} isInvalid={!!errors.password}>
              <FormLabel htmlFor="password">Set Password</FormLabel>
              <Input
                id="password"
                {...register('password', {
                  minLength: {
                    value: 8,
                    message: 'Password must be at least 8 characters',
                  },
                })}
                placeholder="Password"
                type="password"
              />
              {errors.password && (
                <FormErrorMessage>{errors.password.message}</FormErrorMessage>
              )}
            </FormControl>
            <FormControl mt={4} isInvalid={!!errors.confirm_password}>
              <FormLabel htmlFor="confirm_password">Confirm Password</FormLabel>
              <Input
                id="confirm_password"
                {...register('confirm_password', {
                  validate: (value) =>
                    value === getValues().password ||
                    'The passwords do not match',
                })}
                placeholder="Password"
                type="password"
              />
              {errors.confirm_password && (
                <FormErrorMessage>
                  {errors.confirm_password.message}
                </FormErrorMessage>
              )}
            </FormControl>
            <Flex>
              <FormControl mt={4}>
                <Checkbox {...register('is_superuser')} colorScheme="teal">
                  Is superuser?
                </Checkbox>
              </FormControl>
              <FormControl mt={4}>
                <Checkbox {...register('is_active')} colorScheme="teal">
                  Is active?
                </Checkbox>
              </FormControl>
            </Flex>
          </ModalBody>

          <ModalFooter gap={3}>
            <Button
              variant="primary"
              type="submit"
              isLoading={isSubmitting}
              isDisabled={!isDirty}
            >
              Save
            </Button>
            <Button onClick={onCancel}>Cancel</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  )
}

export default EditUser
