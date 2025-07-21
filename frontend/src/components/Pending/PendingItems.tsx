import { Table } from "@chakra-ui/react"
import { useTranslation } from "react-i18next"
import { SkeletonText } from "../ui/skeleton"

const PendingItems = () => {
  const { t } = useTranslation()
  
  return (
    <Table.Root size={{ base: "sm", md: "md" }}>
      <Table.Header>
        <Table.Row>
          <Table.ColumnHeader w="sm">{t("common.id")}</Table.ColumnHeader>
          <Table.ColumnHeader w="sm">{t("common.title")}</Table.ColumnHeader>
          <Table.ColumnHeader w="sm">{t("common.description")}</Table.ColumnHeader>
          <Table.ColumnHeader w="sm">{t("common.actions")}</Table.ColumnHeader>
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {[...Array(5)].map((_, index) => (
          <Table.Row key={index}>
            <Table.Cell>
              <SkeletonText noOfLines={1} />
            </Table.Cell>
            <Table.Cell>
              <SkeletonText noOfLines={1} />
            </Table.Cell>
            <Table.Cell>
              <SkeletonText noOfLines={1} />
            </Table.Cell>
            <Table.Cell>
              <SkeletonText noOfLines={1} />
            </Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table.Root>
  )
}

export default PendingItems
