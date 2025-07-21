import { Flex, Image, useBreakpointValue } from "@chakra-ui/react"
import { Link } from "@tanstack/react-router"
import { useTranslation } from "react-i18next"

import Logo from "/assets/images/fastapi-logo.svg"
import LanguageSwitcher from "./LanguageSwitcher"
import UserMenu from "./UserMenu"

function Navbar() {
  const display = useBreakpointValue({ base: "none", md: "flex" })
  const { t } = useTranslation()

  return (
    <Flex
      display={display}
      justify="space-between"
      position="sticky"
      color="white"
      align="center"
      bg="bg.muted"
      w="100%"
      top={0}
      p={4}
    >
      <Link to="/">
        <Image src={Logo} alt={t("common.logo")} maxW="3xs" p={2} />
      </Link>
      <Flex gap={2} alignItems="center">
        <LanguageSwitcher />
        <UserMenu />
      </Flex>
    </Flex>
  )
}

export default Navbar
