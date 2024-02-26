import React from 'react';

import { Box, Flex, Icon, Text, useColorModeValue } from '@chakra-ui/react';
import { FiBriefcase, FiHome, FiSettings, FiUsers } from 'react-icons/fi';
import { Link, useLocation } from 'react-router-dom';

import { useUserStore } from '../../store/user-store';

const items = [
    { icon: FiHome, title: 'Dashboard', path: "/" },
    { icon: FiBriefcase, title: 'Items', path: "/items" },
    { icon: FiSettings, title: 'User Settings', path: "/settings" },
];

interface SidebarItemsProps {
    onClose?: () => void;
}

const SidebarItems: React.FC<SidebarItemsProps> = ({ onClose }) => {
    const textColor = useColorModeValue("ui.main", "#E2E8F0");
    const bgActive = useColorModeValue("#E2E8F0", "#4A5568");
    const location = useLocation();
    const { user } = useUserStore();

    const finalItems = user?.is_superuser ? [...items, { icon: FiUsers, title: 'Admin', path: "/admin" }] : items;

    const listItems = finalItems.map((item) => (
        <Flex
            as={Link}
            to={item.path}
            w="100%"
            p={2}
            key={item.title}
            style={location.pathname === item.path ? {
                background: bgActive,
                borderRadius: "12px",
            } : {}}
            color={textColor}
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
