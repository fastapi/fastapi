import React from 'react';

import { Button, Flex, Icon, useDisclosure } from '@chakra-ui/react';
import { FaPlus } from "react-icons/fa";

import CreateItem from '../pages/modals/CreateItem';
import CreateUser from '../pages/modals/CreateUser';

interface NavbarProps {
    type: string;
}

const Navbar: React.FC<NavbarProps> = ({ type }) => {
    const createUserModal = useDisclosure();
    const createItemModal = useDisclosure();

    return (
        <>
            <Flex gap={4} py={{ base: "8", md: "4" }} justify={{ base: "center", md: "end" }}>
                <Button bg="ui.main" color="white" gap={1} fontSize={{ base: "sm", md: "inherit" }} onClick={type === "User" ? createUserModal.onOpen : createItemModal.onOpen}>
                    <Icon as={FaPlus} /> Create {type}
                </Button>
                <CreateUser isOpen={createUserModal.isOpen} onClose={createUserModal.onClose} />
                <CreateItem isOpen={createItemModal.isOpen} onClose={createItemModal.onClose} />
            </Flex>
        </>
    );
};

export default Navbar;
