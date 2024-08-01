import path from "node:path"
import { fileURLToPath } from "node:url"
import dotenv from "dotenv"

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

dotenv.config({ path: path.join(__dirname, "../../.env") })

const { FIRST_SUPERUSER, FIRST_SUPERUSER_PASSWORD } = process.env

if (typeof FIRST_SUPERUSER !== "string") {
  throw new Error("Environment variable FIRST_SUPERUSER is undefined")
}

if (typeof FIRST_SUPERUSER_PASSWORD !== "string") {
  throw new Error("Environment variable FIRST_SUPERUSER_PASSWORD is undefined")
}

export const firstSuperuser = FIRST_SUPERUSER as string
export const firstSuperuserPassword = FIRST_SUPERUSER_PASSWORD as string
