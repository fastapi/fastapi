import React from 'react';

import { Container, Heading, Tab, TabList, TabPanel, TabPanels, Tabs } from '@chakra-ui/react';

import Appearance from '../panels/Appearance';
import ChangePassword from '../panels/ChangePassword';
import DeleteAccount from '../panels/DeleteAccount';
import UserInformation from '../panels/UserInformation';



const Profile: React.FC = () => {

    return (
        <>
            <Container maxW="full">
                <Heading size="lg" color="gray.700" textAlign={{ base: "center", md: "left" }} py={12}>
                    User Settings
                </Heading>
                <Tabs variant='enclosed' >
                    <TabList>
                        <Tab>Profile</Tab>
                        <Tab>Password</Tab>
                        <Tab>Appearance</Tab>
                        <Tab>Danger zone</Tab>
                    </TabList>
                    <TabPanels>
                        <TabPanel>
                            <UserInformation />
                        </TabPanel>
                        <TabPanel>
                            <ChangePassword />
                        </TabPanel>
                        <TabPanel>
                            <Appearance />
                        </TabPanel>
                        <TabPanel>
                            <DeleteAccount />
                        </TabPanel>

                    </TabPanels>
                </Tabs>
            </Container>
        </>
    );
};

export default Profile;

