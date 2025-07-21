import { Button, Text } from "@chakra-ui/react";
import { useTranslation } from "react-i18next";
import { FiGlobe } from "react-icons/fi";
import { MenuContent, MenuItem, MenuRoot, MenuTrigger } from "../ui/menu";

const LanguageSwitcher = () => {
  const { i18n, t } = useTranslation();

  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng);
  };

  const currentLanguage =
    i18n.language === "zh" ? t("language.chinese") : t("language.english");

  return (
    <MenuRoot>
      <MenuTrigger asChild>
        <Button variant="ghost" size="sm" gap={2}>
          <FiGlobe />
          <Text fontSize="sm">{currentLanguage}</Text>
        </Button>
      </MenuTrigger>
      <MenuContent>
        <MenuItem
          value="en"
          onClick={() => changeLanguage("en")}
          style={{ cursor: "pointer" }}
        >
          {t("language.english")}
        </MenuItem>
        <MenuItem
          value="zh"
          onClick={() => changeLanguage("zh")}
          style={{ cursor: "pointer" }}
        >
          {t("language.chinese")}
        </MenuItem>
      </MenuContent>
    </MenuRoot>
  );
};

export default LanguageSwitcher;
