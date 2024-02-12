import React, { useEffect, useState } from 'react';

import { Container, Flex, Heading, Spinner, Table, TableContainer, Tbody, Td, Th, Thead, Tr, useToast } from '@chakra-ui/react';

import ActionsMenu from '../../components/ActionsMenu';
import Navbar from '../../components/Navbar';
import { useItemsStore } from '../../store/items-store';


const Items: React.FC = () => {
    const toast = useToast();
    const [isLoading, setIsLoading] = useState(false);
    const { items, getItems } = useItemsStore();

    useEffect(() => {
        const fetchItems = async () => {
            try {
                setIsLoading(true);
                await getItems();
                setIsLoading(false);
            } catch (err) {
                setIsLoading(false);
                toast({
                    title: 'Something went wrong.',
                    description: 'Failed to fetch items. Please try again.',
                    status: 'error',
                    isClosable: true,
                });
            }
        }
        fetchItems();
    }, [])


    return (
        <>
            {isLoading ? (
                // TODO: Add skeleton
                <Flex justify="center" align="center" height="100vh" width="full">
                    <Spinner size="xl" color='ui.main' />
                </Flex>
            ) : (
                items &&
                <Container maxW="full">
                    <Heading size="lg" color="gray.700" textAlign={{ base: "center", md: "left" }} pt={12}>
                        Items Management
                    </Heading>
                    <Navbar type={"Item"} />
                    <TableContainer>
                        <Table size={{ base: "sm", md: "md" }}>
                            <Thead>
                                <Tr>
                                    <Th>ID</Th>
                                    <Th>Title</Th>
                                    <Th>Description</Th>
                                </Tr>
                            </Thead>
                            <Tbody>
                                {items.map((item) => (
                                    <Tr key={item.id}>
                                        <Td>{item.id}</Td>
                                        <Td>{item.title}</Td>
                                        <Td color={!item.description ? "gray.600" : "inherit"}>{item.description || "N/A"}</Td>
                                        <Td>
                                            <ActionsMenu type={"Item"} id={item.id} />
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