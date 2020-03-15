In most cases your application is going to have some configuration, for example, secrets for generating JWT tokes, OAuth2 ID and secret, database connection credentials, token to send out emails using external services.

It is conventional to store such settings in file `.env`. This file should be placed in the root folder of your project.

Such file contains very sensitive information, it is best practice not to commit `.env` to your repository. This is especially crucial for open source projects, as anyone on the internet can read your source code. Exposing such information as database credentials can lead to a data breach.

To prevent this, you should include your `.env` file into `.gitignore` file. Simply add `.env` as a new line.

You can read more about best practices on <a href="https://12factor.net/" class="external-link" target="_blank">Twelve Factor</a> website.

Basically, this means that application should not store any credentials itself but it can read these credentials from the environment variables. Such variables are set outside of an application on operation system level.

In this case, `.env` file is just a convention to store environment variables.

Both Starlette and Pydantic can read `.env` and environment variables out of the box. We are going to use Pydantic as it also provides us the way to validate variables.

```Python hl_lines="2 5 6 7 8 9 10 14 21"
{!./src/configuration/tutorial001.py!}
```

!!! danger
    Never expose your credentials they way it's shown in this endpoint.
    Example is only to see the outcome of our code.

In this example, we import Pydantic's `BaseSettings` and create our class `Settings` that inherits from `BaseSettings`.

Then we declare variables with the same name we expect them to come from environment or `.env` file. We also declare their type, in our case they are strings, so Pydantic will make sure we get strings, not integers.

Our `.env` file would look like this:

```
CLIENT_ID=test_id
CLIENT_SECRET=5ad9caf4-328d-49a8-ab9a-429f571b3b22
```

Optionally, we can set up a default value, in case there was no such environment variable or it was also not found in `.env` file.

!!! danger
    Remember not to set default values in your code for sensitive data, such as credentials.
    Default values can be handy to store regular settings.

Next, we define a filename to retrieve settings from. In our case, it's `.env`

Finally, we store resulting object `Settings` in variable `settings` which can be later used to get our configuration from.

This code can be put in a separate module which you can import any time you need to use your configuration settings.

```Python
#  config.py
from pydantic import BaseSettings


class Settings(BaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET: str

    class Config:
        env_file = ".env"


settings = Settings()
```

So next time you need to access your settings just import them:

```Python
from .config import settings
...
```