import React from 'react';

import { Avatar, Flex, Skeleton, Text } from '@chakra-ui/react';
import { FaUserAstronaut } from 'react-icons/fa';

import { useUserStore } from '../store/user-store';


const UserInfo: React.FC = () => {
    const { user } = useUserStore();
    

    return (
        <>
            {user ? (
                <Flex gap={2} maxW="180px">
                    <Avatar bg="ui.main" icon={<FaUserAstronaut fontSize="18px" />} size='sm' alignSelf="center" />
                    {/* TODO: Conditional tooltip based on email length */}
                    <Text color='gray' alignSelf={"center"} noOfLines={1} fontSize="14px">{user.email}</Text>
                </Flex>
            ) :
                <Skeleton height='20px' />
            }
        </>
    );

}

export default UserInfo;