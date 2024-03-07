import React, { useEffect } from 'react';

import { Flex } from '@chakra-ui/react';
import { Outlet } from 'react-router-dom';

import Sidebar from '../components/Common/Sidebar';
import UserMenu from '../components/Common/UserMenu';
import { useUserStore } from '../store/user-store';
import { isLoggedIn } from '../hooks/useAuth';

const Layout: React.FC = () => {
    const { getUser } = useUserStore();

    useEffect(() => {
        const fetchUser = async () => {
            if (isLoggedIn()) {
                await getUser();
            }
        };
        fetchUser();
    }, []);

    return (
        <Flex maxW='large' h='auto' position='relative'>
            <Sidebar />
            <Outlet />
            <UserMenu />
        </Flex>
    );
};

export default Layout;