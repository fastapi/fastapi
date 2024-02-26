import React from 'react';

import { Box, IconButton, Menu, MenuButton, MenuItem, MenuList } from '@chakra-ui/react';
import { FaUserAstronaut } from 'react-icons/fa';
import { FiLogOut, FiUser } from 'react-icons/fi';
import { Link, useNavigate } from 'react-router-dom';

import useAuth from '../../hooks/useAuth';

const UserMenu: React.FC = () => {
    const navigate = useNavigate();
    const { logout } = useAuth();

    const handleLogout = async () => {
        logout()
        navigate('/login');
    };

    return (
        <>
            {/* Desktop */}
            <Box display={{ base: 'none', md: 'block' }} position='fixed' top={4} right={4}>
                <Menu>
                    <MenuButton
                        as={IconButton}
                        aria-label='Options'
                        icon={<FaUserAstronaut color='white' fontSize='18px' />}
                        bg='ui.main'
                        isRound
                    />
                    <MenuList>
                        <MenuItem icon={<FiUser fontSize='18px' />} as={Link} to='settings'>
                            My profile
                        </MenuItem>
                        <MenuItem icon={<FiLogOut fontSize='18px' />} onClick={handleLogout} color='ui.danger' fontWeight='bold'>
                            Log out
                        </MenuItem>
                    </MenuList>
                </Menu>
            </Box>
        </>
    );
};

export default UserMenu;
