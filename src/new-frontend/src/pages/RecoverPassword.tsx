import React from "react";

import { Button, Container, FormControl, Heading, Input, Text, useToast } from "@chakra-ui/react";
import { SubmitHandler, useForm } from "react-hook-form";

import { LoginService } from "../client";

interface FormData {
  email: string;
}

const RecoverPassword: React.FC = () => {
  const { register, handleSubmit } = useForm<FormData>();
  const toast = useToast();

  const onSubmit: SubmitHandler<FormData> = async (data) => {
    const response = await LoginService.recoverPassword({
      email: data.email,
    });
    console.log(response);

    toast({
      title: "Email sent.",
      description: "We sent an email with a link to get back into your account.",
      status: "success",
      isClosable: true,
    });
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
      <Heading size="xl" color="ui.main" textAlign="center" mb={2}>
        Password Recovery
      </Heading>
      <FormControl id="username">
        <Text align="center" color="gray.600">
          A password recovery email will be sent to the registered account.
        </Text>
        <Input
          {...register("email")}

          mt={4}
          placeholder="Enter your email"
          type="text"
        />
      </FormControl>
      <Button bg="ui.main" color="white" _hover={{ opacity: 0.8 }} type="submit">
        Continue
      </Button>
    </Container>
  );
};

export default RecoverPassword;
