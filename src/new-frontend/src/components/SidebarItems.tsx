import React from 'react';

import { Flex, Icon, Text } from '@chakra-ui/react';
import { FiBriefcase, FiHome, FiLogOut, FiSettings, FiUsers } from 'react-icons/fi';
import { Link, useNavigate } from 'react-router-dom';


const items = [
    { icon: FiHome, title: 'Dashboard', path: "/" },
    { icon: FiBriefcase, title: 'Items', path: "/items" },
    { icon: FiUsers, title: 'Admin', path: "/admin" },
    { icon: FiSettings, title: 'User Settings', path: "/settings" },
    { icon: FiLogOut, title: 'Log out' }
];

interface SidebarItemsProps {
    onClose?: () => void;
}

const SidebarItems: React.FC<SidebarItemsProps> = ({ onClose }) => {
    const navigate = useNavigate();

    const handleLogout = async () => {
        localStorage.removeItem("access_token");
        navigate("/login");
    // TODO: reset all Zustand states
    };

    const listItems = items.map((item) => (
        <Flex w="100%" p={2} key={item.title} _hover={{
            background: "gray.200",
            borderRadius: "12px",
        }} onClick={item.title === 'Log out' ? handleLogout : onClose}>
            <Link to={item.path || "/"}>
                <Flex gap={4}>
                    <Icon color="ui.main" as={item.icon} alignSelf="center" />
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
