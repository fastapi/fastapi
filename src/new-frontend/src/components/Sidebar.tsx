import React from 'react';

import { Box, Drawer, DrawerBody, DrawerCloseButton, DrawerContent, DrawerOverlay, Flex, IconButton, Image, useDisclosure } from '@chakra-ui/react';
import { FiMenu } from 'react-icons/fi';

import Logo from "../assets/images/fastapi-logo.png";
import SidebarItems from './SidebarItems';
import UserInfo from './UserInfo';


const Sidebar: React.FC = () => {
    const { isOpen, onOpen, onClose } = useDisclosure();

    return (
        <>
            {/* Mobile */}
            <IconButton onClick={onOpen} display={{ base: 'flex', md: 'none' }} aria-label="Open Menu" position="absolute" fontSize='20px' m={4} icon={<FiMenu />} />
            <Drawer isOpen={isOpen} placement="left" onClose={onClose}>
                <DrawerOverlay />
                <DrawerContent bg="gray.100" maxW="250px">
                    <DrawerCloseButton />
                    <DrawerBody py={8}>
                        <Flex flexDir="column" justify="space-between" h="100%">
                            <Box>
                                <Image src={Logo} alt="Logo" />
                                <SidebarItems />
                            </Box>
                            <UserInfo />
                        </Flex>
                    </DrawerBody>
                </DrawerContent>
            </Drawer>

            {/* Desktop */}
            <Box bg="white" p={3} h="100vh" position="sticky" top="0" display={{ base: 'none', md: 'flex' }}>
                <Flex flexDir="column" justify="space-between" bg="gray.100" p={6} borderRadius={12}>
                    <Box>
                        <Image src={Logo} alt="Logo" w="180px" maxW="2xs" />
                        <SidebarItems />
                    </Box>
                    <UserInfo />
                </Flex>
            </Box>
        </>
    );
}

export default Sidebar;
