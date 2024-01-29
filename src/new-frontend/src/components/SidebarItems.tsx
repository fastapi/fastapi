import React from 'react';

import { Flex, Icon, Text } from '@chakra-ui/react';
import { FiBriefcase, FiHome, FiLogOut, FiUser, FiUsers } from 'react-icons/fi';
import { Link } from 'react-router-dom';

const items = [
    { icon: FiHome, title: 'Dashboard', path: "/" },
    { icon: FiUser, title: 'Profile', path: "/profile" },
    { icon: FiBriefcase, title: 'Items', path: "/items" },
    { icon: FiUsers, title: 'Admin', path: "/admin" },
    { icon: FiLogOut, title: 'Log out' }
];

interface SidebarItemsProps {
    onClose?: () => void;
}

const SidebarItems: React.FC<SidebarItemsProps> = ({ onClose }) => {
    const listItems = items.map((item) => (
        <Flex w="100%" p={2} key={item.title} _hover={{
            background: "gray.200",
            borderRadius: "12px",
        }} onClick={onClose}>
            <Link to={item.path || "/"}>
                <Flex color="teal.500" gap={4}>
                    <Icon as={item.icon} alignSelf="center" />
                    <Text>{item.title}</Text>
                </Flex>
            </Link>
        </Flex>
    ));

    return (
        <>
            {listItems}
        </>
    );
};

export default SidebarItems;
