"use client"

import { useTranslation } from "react-i18next"
import { toaster } from "@/components/ui/toaster"

const useCustomToast = () => {
  const { t } = useTranslation()
  
  const showSuccessToast = (description: string) => {
    toaster.create({
      title: t("common.success"),
      description,
      type: "success",
    })
  }

  const showErrorToast = (description: string) => {
    toaster.create({
      title: t("common.error"),
      description,
      type: "error",
    })
  }

  return { showSuccessToast, showErrorToast }
}

export default useCustomToast
