import React, { useEffect } from 'react';

import { Flex } from '@chakra-ui/react';
import { Outlet } from 'react-router-dom';

import Sidebar from '../components/Common/Sidebar';
import UserMenu from '../components/Common/UserMenu';
import { useUserStore } from '../store/user-store';

const Layout: React.FC = () => {
    const { getUser } = useUserStore();

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (token) {
            (async () => {
                await getUser();
            })();
        }
    }, [getUser]);

    return (
        <Flex maxW='large' h='auto' position='relative'>
            <Sidebar />
            <Outlet />
            <UserMenu />
        </Flex>
    );
};

export default Layout;