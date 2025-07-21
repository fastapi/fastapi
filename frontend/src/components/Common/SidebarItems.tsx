import { Box, Flex, Icon, Text } from "@chakra-ui/react"
import { useQueryClient } from "@tanstack/react-query"
import { Link as RouterLink } from "@tanstack/react-router"
import { useTranslation } from "react-i18next"
import { FiBriefcase, FiHome, FiSettings, FiUsers } from "react-icons/fi"
import type { IconType } from "react-icons/lib"

import type { UserPublic } from "@/client"

interface SidebarItemsProps {
  onClose?: () => void
}

interface Item {
  icon: IconType
  titleKey: string
  path: string
}

const SidebarItems = ({ onClose }: SidebarItemsProps) => {
  const queryClient = useQueryClient()
  const currentUser = queryClient.getQueryData<UserPublic>(["currentUser"])
  const { t } = useTranslation()

  const items: Item[] = [
    { icon: FiHome, titleKey: "navigation.dashboard", path: "/" },
    { icon: FiBriefcase, titleKey: "navigation.items", path: "/items" },
    { icon: FiSettings, titleKey: "navigation.userSettings", path: "/settings" },
  ]

  const finalItems: Item[] = currentUser?.is_superuser
    ? [...items, { icon: FiUsers, titleKey: "navigation.admin", path: "/admin" }]
    : items

  const listItems = finalItems.map(({ icon, titleKey, path }) => (
    <RouterLink key={titleKey} to={path} onClick={onClose}>
      <Flex
        gap={4}
        px={4}
        py={2}
        _hover={{
          background: "gray.subtle",
        }}
        alignItems="center"
        fontSize="sm"
      >
        <Icon as={icon} alignSelf="center" />
        <Text ml={2}>{t(titleKey)}</Text>
      </Flex>
    </RouterLink>
  ))

  return (
    <>
      <Text fontSize="xs" px={4} py={2} fontWeight="bold">
        {t('navigation.menu')}
      </Text>
      <Box>{listItems}</Box>
    </>
  )
}

export default SidebarItems
