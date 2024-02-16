import React from 'react';

import { IconButton } from '@chakra-ui/button';
import { Box } from '@chakra-ui/layout';
import { Menu, MenuButton, MenuItem, MenuList } from '@chakra-ui/menu';
import { FaUserAstronaut } from 'react-icons/fa';
import { FiLogOut, FiUser } from 'react-icons/fi';
import { useNavigate } from 'react-router';
import { Link } from 'react-router-dom';

const UserMenu: React.FC = () => {
    const navigate = useNavigate();

    const handleLogout = async () => {
        localStorage.removeItem("access_token");
        navigate("/login");
        // TODO: reset all Zustand states
    };

    return (
        <>
            <Box position="fixed" top={4} right={4}>
                <Menu>
                    <MenuButton
                        as={IconButton}
                        aria-label='Options'
                        icon={<FaUserAstronaut color="white" fontSize="18px" />}
                        bg="ui.main"
                        isRound
                    />
                    <MenuList>
                        <MenuItem icon={<FiUser fontSize="18px" />} as={Link} to="settings">
                            My profile
                        </MenuItem>
                        <MenuItem icon={<FiLogOut fontSize="18px" />} onClick={handleLogout} color="ui.danger" fontWeight="bold">
                            Log out
                        </MenuItem>
                    </MenuList>
                </Menu>
            </Box>
        </>
    );
};

export default UserMenu;
