import React from "react";

import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
import { Button, Center, Container, FormControl, Icon, Image, Input, InputGroup, InputRightElement, Link, useBoolean } from "@chakra-ui/react";
import { SubmitHandler, useForm } from "react-hook-form";
import { Link as ReactRouterLink, useNavigate } from "react-router-dom";

import Logo from "../../assets/images/fastapi-logo.png";
import { LoginService } from "../../client";
import { Body_login_login_access_token as AccessToken } from "../../client/models/Body_login_login_access_token";

const Login: React.FC = () => {
  const [show, setShow] = useBoolean();
  const navigate = useNavigate();
  const { register, handleSubmit } = useForm<AccessToken>();

  const onSubmit: SubmitHandler<AccessToken> = async (data) => {
    const response = await LoginService.loginAccessToken({
      formData: data,
    });
    localStorage.setItem("access_token", response.access_token);
    navigate("/");
  };

  return (
    <Container
      as="form"
      onSubmit={handleSubmit(onSubmit)}
      h="100vh"
      maxW="sm"
      alignItems="stretch"
      justifyContent="center"
      gap={4}
      centerContent
    >
      <Image src={Logo} alt="FastAPI logo" height="auto" maxW="2xs" alignSelf="center" />
      <FormControl id="email">
        <Input {...register("username")} focusBorderColor="blue.200" placeholder="Email" type="text" />
      </FormControl>
      <FormControl id="password">
        <InputGroup>
          <Input
            {...register("password")}
            type={show ? "text" : "password"}
            focusBorderColor="blue.200"
            placeholder="Password"
          />
          <InputRightElement
            color="gray.500"
            _hover={{
              cursor: "pointer",
            }}
          >
            <Icon onClick={setShow.toggle} aria-label={show ? "Hide password" : "Show password"}>
              {show ? <ViewOffIcon /> : <ViewIcon />}
            </Icon>
          </InputRightElement>
        </InputGroup>
        <Center>
          <Link as={ReactRouterLink} to="/recover-password" color="blue.500" mt={2}>
            Forgot password?
          </Link>
        </Center>
      </FormControl>
      <Button colorScheme="teal" type="submit">
        Log In
      </Button>
    </Container>
  );
};

export default Login;
