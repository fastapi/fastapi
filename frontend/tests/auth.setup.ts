import { test as setup } from "@playwright/test"

const authFile = "playwright/.auth/user.json"

setup("authenticate", async ({ page }) => {
  await page.goto("/login")
  await page.getByPlaceholder("Email").fill("admin@example.com")
  await page.getByPlaceholder("Password").fill("changethis")
  await page.getByRole("button", { name: "Log In" }).click()
  await page.waitForURL("/")
  await page.context().storageState({ path: authFile })
})
