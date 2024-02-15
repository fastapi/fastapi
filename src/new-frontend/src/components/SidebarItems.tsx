import React from 'react';

import { Box, Flex, Icon, Text } from '@chakra-ui/react';
import { FiBriefcase, FiHome, FiSettings, FiUsers } from 'react-icons/fi';
import { Link, useLocation } from 'react-router-dom';

const items = [
    { icon: FiHome, title: 'Dashboard', path: "/" },
    { icon: FiBriefcase, title: 'Items', path: "/items" },
    { icon: FiUsers, title: 'Admin', path: "/admin" },
    { icon: FiSettings, title: 'User Settings', path: "/settings" },
];

interface SidebarItemsProps {
    onClose?: () => void;
}

const SidebarItems: React.FC<SidebarItemsProps> = ({ onClose }) => {
    const location = useLocation();

    const listItems = items.map((item) => (
        <Flex
            as={Link}
            to={item.path}
            w="100%"
            p={2}
            key={item.title}
            style={location.pathname === item.path ? {
                background: "#E2E8F0",
                borderRadius: "12px",
            } : {}}
            color="ui.main"
            onClick={onClose}
        >
            <Icon as={item.icon} alignSelf="center" />
            <Text ml={2}>{item.title}</Text>
        </Flex>
    ));

    return (
        <>
            <Box>
                {listItems}
            </Box>
           
        </>
    );
};

export default SidebarItems;
