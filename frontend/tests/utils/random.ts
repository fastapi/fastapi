export const randomEmail = () =>
  `test_${Math.random().toString(36).substring(7)}@example.com`

export const randomTeamName = () =>
  `Team ${Math.random().toString(36).substring(7)}`

export const randomPassword = () => `${Math.random().toString(36).substring(2)}`

export const slugify = (text: string) =>
  text
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^\w-]+/g, "")
