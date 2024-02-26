import React from 'react';

import { ViewIcon, ViewOffIcon } from '@chakra-ui/icons';
import { Button, Center, Container, FormControl, Icon, Image, Input, InputGroup, InputRightElement, Link, useBoolean } from '@chakra-ui/react';
import { SubmitHandler, useForm } from 'react-hook-form';
import { Link as ReactRouterLink, useNavigate } from 'react-router-dom';

import Logo from '../assets/images/fastapi-logo.svg';
import { Body_login_login_access_token as AccessToken } from '../client/models/Body_login_login_access_token';
import useAuth from '../hooks/useAuth';

const Login: React.FC = () => {
  const [show, setShow] = useBoolean();
  const navigate = useNavigate();
  const { register, handleSubmit } = useForm<AccessToken>();
  const { login } = useAuth();

  const onSubmit: SubmitHandler<AccessToken> = async (data) => {
    await login(data);
    navigate('/');
  };

  return (
    <>
      <Container
        as='form'
        onSubmit={handleSubmit(onSubmit)}
        h='100vh'
        maxW='sm'
        alignItems='stretch'
        justifyContent='center'
        gap={4}
        centerContent
      >
        <Image src={Logo} alt='FastAPI logo' height='auto' maxW='2xs' alignSelf='center' />
        <FormControl id='email'>
          <Input {...register('username')} placeholder='Email' type='text' />
        </FormControl>
        <FormControl id='password'>
          <InputGroup>
            <Input
              {...register('password')}
              type={show ? 'text' : 'password'}

              placeholder='Password'
            />
            <InputRightElement
              color='gray.400'
              _hover={{
                cursor: 'pointer',
              }}
            >
              <Icon onClick={setShow.toggle} aria-label={show ? 'Hide password' : 'Show password'}>
                {show ? <ViewOffIcon /> : <ViewIcon />}
              </Icon>
            </InputRightElement>
          </InputGroup>
          <Center>
            <Link as={ReactRouterLink} to='/recover-password' color='blue.500' mt={2}>
              Forgot password?
            </Link>
          </Center>
        </FormControl>
        <Button bg='ui.main' color='white' _hover={{ opacity: 0.8 }} type='submit'>
          Log In
        </Button>
      </Container>
    </>
  );
};

export default Login;
