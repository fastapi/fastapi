import React, { useEffect, useState } from 'react';

import { Box, Container, Flex, Heading, Spinner, Table, TableContainer, Tbody, Td, Th, Thead, Tr, useToast } from '@chakra-ui/react';

import ActionsMenu from '../components/ActionsMenu';
import Navbar from '../components/Navbar';
import { useUsersStore } from '../store/users-store';

const Admin: React.FC = () => {
    const toast = useToast();
    const [isLoading, setIsLoading] = useState(false);
    const { users, getUsers } = useUsersStore();

    useEffect(() => {
        const fetchUsers = async () => {
            setIsLoading(true);
            try {
                await getUsers();
            } catch (err) {
                toast({
                    title: 'Something went wrong.',
                    description: 'Failed to fetch users. Please try again.',
                    status: 'error',
                    isClosable: true,
                });
            } finally {
                setIsLoading(false);
            }
        }
        if (users.length === 0) {
            fetchUsers();
        }
    }, [])

    return (
        <>
            {isLoading ? (
                // TODO: Add skeleton
                <Flex justify="center" align="center" height="100vh" width="full">
                    <Spinner size="xl" color='ui.main' />
                </Flex>
            ) : (
                users &&
                <Container maxW="full">
                    <Heading size="lg" color="gray.700" textAlign={{ base: "center", md: "left" }} pt={12}>
                        User Management
                    </Heading>
                    <Navbar type={"User"} />
                    <TableContainer>
                        <Table fontSize="md" size={{ base: "sm", md: "md" }}>
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
                                {users.map((user) => (
                                    <Tr key={user.id}>
                                        <Td color={!user.full_name ? "gray.600" : "inherit"}>{user.full_name || "N/A"}</Td>
                                        <Td>{user.email}</Td>
                                        <Td>{user.is_superuser ? "Superuser" : "User"}</Td>
                                        <Td>
                                            <Flex gap={2}>
                                                <Box
                                                    w="2"
                                                    h="2"
                                                    borderRadius="50%"
                                                    bg={user.is_active ? "ui.success" : "ui.danger"}
                                                    alignSelf="center"
                                                />
                                                {user.is_active ? "Active" : "Inactive"}
                                            </Flex>
                                        </Td>
                                        <Td>
                                            <ActionsMenu type="User" id={user.id} />
                                        </Td>
                                    </Tr>
                                ))}
                            </Tbody>
                        </Table>
                    </TableContainer>
                </Container>
            )}
        </>
    )
}

export default Admin;
