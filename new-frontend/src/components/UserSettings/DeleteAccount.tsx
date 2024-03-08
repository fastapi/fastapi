import React from 'react'
import {
  Button,
  Container,
  Heading,
  Text,
  useDisclosure,
} from '@chakra-ui/react'

import DeleteConfirmation from './DeleteConfirmation'

const DeleteAccount: React.FC = () => {
  const confirmationModal = useDisclosure()

  return (
    <>
      <Container maxW="full">
        <Heading size="sm" py={4}>
          Delete Account
        </Heading>
        <Text>
          Are you sure you want to delete your account? This action cannot be
          undone.
        </Text>
        <Button
          bg="ui.danger"
          color="white"
          _hover={{ opacity: 0.8 }}
          mt={4}
          onClick={confirmationModal.onOpen}
        >
          Delete
        </Button>
        <DeleteConfirmation
          isOpen={confirmationModal.isOpen}
          onClose={confirmationModal.onClose}
        />
      </Container>
    </>
  )
}
export default DeleteAccount
