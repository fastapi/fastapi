import React, { useEffect, useState } from 'react';

import { Container, Flex, Heading, Spinner, Table, TableContainer, Tbody, Td, Th, Thead, Tr } from '@chakra-ui/react';

import { ApiError } from '../client';
import ActionsMenu from '../components/Common/ActionsMenu';
import Navbar from '../components/Common/Navbar';
import useCustomToast from '../hooks/useCustomToast';
import { useItemsStore } from '../store/items-store';

const Items: React.FC = () => {
    const showToast = useCustomToast();
    const [isLoading, setIsLoading] = useState(false);
    const { items, getItems } = useItemsStore();

    useEffect(() => {
        const fetchItems = async () => {
            setIsLoading(true);
            try {
                await getItems();
            } catch (err) {
                const errDetail = (err as ApiError).body.detail;
                showToast('Something went wrong.', `${errDetail}`, 'error');
            } finally {
                setIsLoading(false);
            }
        }
        if (items.length === 0) {
            fetchItems();
        }
    }, [])


    return (
        <>
            {isLoading ? (
                // TODO: Add skeleton
                <Flex justify='center' align='center' height='100vh' width='full'>
                    <Spinner size='xl' color='ui.main' />
                </Flex>
            ) : (
                items &&
                <Container maxW='full'>
                    <Heading size='lg' textAlign={{ base: 'center', md: 'left' }} pt={12}>
                        Items Management
                    </Heading>
                    <Navbar type={'Item'} />
                    <TableContainer>
                        <Table size={{ base: 'sm', md: 'md' }}>
                            <Thead>
                                <Tr>
                                    <Th>ID</Th>
                                    <Th>Title</Th>
                                    <Th>Description</Th>
                                    <Th>Actions</Th>
                                </Tr>
                            </Thead>
                            <Tbody>
                                {items.map((item) => (
                                    <Tr key={item.id}>
                                        <Td>{item.id}</Td>
                                        <Td>{item.title}</Td>
                                        <Td color={!item.description ? 'gray.600' : 'inherit'}>{item.description || 'N/A'}</Td>
                                        <Td>
                                            <ActionsMenu type={'Item'} id={item.id} />
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

export default Items;