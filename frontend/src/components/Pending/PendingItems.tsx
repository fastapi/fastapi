import { Skeleton, Table } from "@chakra-ui/react"

const PendingItems = () => (
  <Table.Root size={{ base: "sm", md: "md" }}>
    <Table.Header>
      <Table.Row>
        <Table.ColumnHeader w="30%">ID</Table.ColumnHeader>
        <Table.ColumnHeader w="30%">Title</Table.ColumnHeader>
        <Table.ColumnHeader w="30%">Description</Table.ColumnHeader>
        <Table.ColumnHeader w="10%">Actions</Table.ColumnHeader>
      </Table.Row>
    </Table.Header>
    <Table.Body>
      {[...Array(5)].map((_, index) => (
        <Table.Row key={index}>
          <Table.Cell>
            <Skeleton h="20px" />
          </Table.Cell>
          <Table.Cell>
            <Skeleton h="20px" />
          </Table.Cell>
          <Table.Cell>
            <Skeleton h="20px" />
          </Table.Cell>
          <Table.Cell>
            <Skeleton h="20px" />
          </Table.Cell>
        </Table.Row>
      ))}
    </Table.Body>
  </Table.Root>
)

export default PendingItems
