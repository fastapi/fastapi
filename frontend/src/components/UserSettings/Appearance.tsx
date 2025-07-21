import { Container, Heading, Stack } from "@chakra-ui/react"
import { useTheme } from "next-themes"
import { useTranslation } from "react-i18next"

import { Radio, RadioGroup } from "@/components/ui/radio"

const Appearance = () => {
  const { theme, setTheme } = useTheme()
  const { t } = useTranslation()

  return (
    <>
      <Container maxW="full">
        <Heading size="sm" py={4}>
          {t("user.appearance")}
        </Heading>

        <RadioGroup
          onValueChange={(e) => setTheme(e.value)}
          value={theme}
          colorPalette="teal"
        >
          <Stack>
            <Radio value="system">{t("theme.system")}</Radio>
            <Radio value="light">{t("theme.light")}</Radio>
            <Radio value="dark">{t("theme.dark")}</Radio>
          </Stack>
        </RadioGroup>
      </Container>
    </>
  )
}
export default Appearance
