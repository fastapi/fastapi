import React from 'react';

import { Button, Menu, MenuButton, MenuItem, MenuList, useDisclosure } from '@chakra-ui/react';
import { BsThreeDotsVertical } from 'react-icons/bs';
import { FiTrash, FiEdit } from 'react-icons/fi';

import Delete from '../modals/DeleteAlert';
import EditUser from '../modals/EditUser';
import EditItem from '../modals/EditItem';

interface ActionsMenuProps {
    type: string;
    id: number;
}

const ActionsMenu: React.FC<ActionsMenuProps> = ({ type, id }) => {
    const editUserModal = useDisclosure();
    const deleteModal = useDisclosure();

    return (
        <>
            <Menu>
                <MenuButton as={Button} bg="white" rightIcon={<BsThreeDotsVertical />} variant="unstyled">
                </MenuButton>
                <MenuList>
                    <MenuItem onClick={editUserModal.onOpen} icon={<FiEdit fontSize="16px" />}>Edit {type}</MenuItem>
                    <MenuItem onClick={deleteModal.onOpen} icon={<FiTrash fontSize="16px" />} color="ui.danger">Delete {type}</MenuItem>
                </MenuList>
                {
                    type === "User" ? <EditUser isOpen={editUserModal.isOpen} onClose={editUserModal.onClose} />
                        : <EditItem isOpen={editUserModal.isOpen} onClose={editUserModal.onClose} />
                }
                <Delete type={type} id={id} isOpen={deleteModal.isOpen} onClose={deleteModal.onClose} />
            </Menu>
        </>
    );
};

export default ActionsMenu;
