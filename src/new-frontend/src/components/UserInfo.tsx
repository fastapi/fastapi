import React, { useEffect, useState } from 'react';

import { Avatar, Flex, Skeleton, Text } from '@chakra-ui/react';
import { FaUserAstronaut } from 'react-icons/fa';

import { UserOut, UsersService } from '../client';

const UserInfo: React.FC = () => {
    const [userData, setUserData] = useState<UserOut>();

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const userResponse = await UsersService.readUserMe();
                setUserData(userResponse);
            } catch (error) {
                // TODO: Handle error to give feedback to the user
                console.error(error);
            }
        };
        fetchUserData();
    }, []);

    return (
        <>
            {userData ? (
                <Flex gap={2} maxW="180px">
                    <Avatar icon={<FaUserAstronaut fontSize="18px" />} size='sm' alignSelf="center" />
                    {/* TODO: Conditional tooltip based on email length */}
                    <Text color='gray' alignSelf={"center"} noOfLines={1} fontSize="14px">{userData.email}</Text>
                </Flex>
            ) :
                <Skeleton height='20px' />
            }
        </>
    );

}

export default UserInfo;