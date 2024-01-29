import Sidebar from '../components/Sidebar';

import { Flex } from '@chakra-ui/react';

const Layout = ({ children }: { children: React.ReactNode }) => {
    return (
        <Flex maxW="large" h="auto" position="relative">
            <Sidebar />
            {children}
        </Flex>
    );
};

export default Layout;
