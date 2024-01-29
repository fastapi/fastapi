import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';

import { Flex } from '@chakra-ui/react';

const Layout = () => {
    return (
        <Flex maxW="large" h="auto" position="relative">
            <Sidebar />
            <Outlet />
        </Flex>
    );
};

export default Layout;
