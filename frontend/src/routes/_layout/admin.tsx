import {
  Badge,
  Box,
  Container,
  Flex,
  Heading,
  Spinner,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from '@chakra-ui/react'
import { createFileRoute } from '@tanstack/react-router'
import { useQuery, useQueryClient } from 'react-query'

import { ApiError, UserOut, UsersService } from '../../client'
import ActionsMenu from '../../components/Common/ActionsMenu'
import Navbar from '../../components/Common/Navbar'
import useCustomToast from '../../hooks/useCustomToast'

export const Route = createFileRoute('/_layout/admin')({
  component: Admin,
})

function Admin() {
  const queryClient = useQueryClient()
  const showToast = useCustomToast()
  const currentUser = queryClient.getQueryData<UserOut>('currentUser')
  const {
    data: users,
    isLoading,
    isError,
    error,
  } = useQuery('users', () => UsersService.readUsers({}))

  if (isError) {
    const errDetail = (error as ApiError).body?.detail
    showToast('Something went wrong.', `${errDetail}`, 'error')
  }

  return (
    <>
      {isLoading ? (
        // TODO: Add skeleton
        <Flex justify="center" align="center" height="100vh" width="full">
          <Spinner size="xl" color="ui.main" />
        </Flex>
      ) : (
        users && (
          <Container maxW="full">
            <Heading
              size="lg"
              textAlign={{ base: 'center', md: 'left' }}
              pt={12}
            >
              User Management
            </Heading>
            <Navbar type={'User'} />
            <TableContainer>
              <Table fontSize="md" size={{ base: 'sm', md: 'md' }}>
                <Thead>
                  <Tr>
                    <Th>Full name</Th>
                    <Th>Email</Th>
                    <Th>Role</Th>
                    <Th>Status</Th>
                    <Th>Actions</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  {users.data.map((user) => (
                    <Tr key={user.id}>
                      <Td color={!user.full_name ? 'gray.400' : 'inherit'}>
                        {user.full_name || 'N/A'}
                        {currentUser?.id === user.id && (
                          <Badge ml="1" colorScheme="teal">
                            You
                          </Badge>
                        )}
                      </Td>
                      <Td>{user.email}</Td>
                      <Td>{user.is_superuser ? 'Superuser' : 'User'}</Td>
                      <Td>
                        <Flex gap={2}>
                          <Box
                            w="2"
                            h="2"
                            borderRadius="50%"
                            bg={user.is_active ? 'ui.success' : 'ui.danger'}
                            alignSelf="center"
                          />
                          {user.is_active ? 'Active' : 'Inactive'}
                        </Flex>
                      </Td>
                      <Td>
                        <ActionsMenu
                          type="User"
                          value={user}
                          disabled={currentUser?.id === user.id ? true : false}
                        />
                      </Td>
                    </Tr>
                  ))}
                </Tbody>
              </Table>
            </TableContainer>
          </Container>
        )
      )}
    </>
  )
}

export default Admin
