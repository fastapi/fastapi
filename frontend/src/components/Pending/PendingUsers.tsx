import { Skeleton, Table } from "@chakra-ui/react"

const PendingUsers = () => (
  <Table.Root size={{ base: "sm", md: "md" }}>
    <Table.Header>
      <Table.Row>
        <Table.ColumnHeader w="20%">Full name</Table.ColumnHeader>
        <Table.ColumnHeader w="25%">Email</Table.ColumnHeader>
        <Table.ColumnHeader w="15%">Role</Table.ColumnHeader>
        <Table.ColumnHeader w="20%">Status</Table.ColumnHeader>
        <Table.ColumnHeader w="20%">Actions</Table.ColumnHeader>
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
          <Table.Cell>
            <Skeleton h="20px" />
          </Table.Cell>
        </Table.Row>
      ))}
    </Table.Body>
  </Table.Root>
)

export default PendingUsers
