# Deploy FastAPI on Deta Space

In this section you will learn how to easily deploy a **FastAPI** application on <a href="https://deta.space?ref=fastapi" class="external-link" target="_blank">Deta Space</a> for free. 🎁

It will take you about **10 minutes**.

!!! info
    <a href="https://deta.space?ref=fastapi" class="external-link" target="_blank">Deta</a> is a **FastAPI** sponsor. 🎉

## A simple **FastAPI** app

- Create an empty directory with the name of your app, and then navigate into it.

```console
$ mkdir fastapi-deta
$ cd fastapi-deta
```

### FastAPI app code

- Create a `main.py` file with:

```py
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
		print({"item_id": item_id})
    return {"item_id": item_id}
```

### Requirements

Now, in the same directory create a file `requirements.txt` with:

```text
fastapi
```

!!! tip
    You don't need to install Uvicorn to deploy on Deta Space, although you would probably want to install it locally to test your app.

### Directory structure

You will now have a directory with two files:

```
fastapi-deta/
└── main.py
└── requirements.txt
```

## Create a free **Deta Space** account

Now create a free account on <a href="https://deta.space?ref=fastapi" class="external-link" target="_blank">Deta Space</a>, you just need an email and password.

You don't even need a credit card.

## Install the CLI

Once you have your account, install the Space <abbr title="Command Line Interface application">CLI</abbr>:

=== "Linux, macOS"

    <div class="termy">

    ```console
    $ curl -fsSL https://get.deta.dev/space-cli.sh | sh
    ```

    </div>

=== "Windows PowerShell"

    <div class="termy">

    ```console
    $ iwr https://get.deta.dev/space-cli.ps1 -useb | iex
    ```

    </div>

After installing it, open a new terminal so that the installed CLI is detected.

In a new terminal, confirm that it was correctly installed with:

<div class="termy">

```console
$ space --help

Deta command line interface for managing deta micros.
Complete documentation available at https://deta.space/docs

Usage:
  space [flags]
  space [command]

Available Commands:
  help        Help about any command
  link        link code to project
  login       login to space
  new         create new project
  push        push code for project
  release     create release for a project
  validate    validate spacefile in dir
  version     Space CLI version
...
```

</div>

!!! tip
    If you have problems installing the CLI, check the <a href="https://deta.space/docs/en/basics/cli?ref=fastapi" class="external-link" target="_blank">official Space Docs</a>.

## Login with the CLI

Now login to Space from the CLI with:

<div class="termy">

```console
$ space login

To authenticate the Space CLI with your Space account, generate a new access token in your Space settings and paste it below:

? Enter access token (41 chars) > *****************************************

👍 Login Successful!
```

</div>

In order to authenticate your CLI, this command will prompt you for an `access token`. To obtain this token, open the Teletype in your [Space dashboard](https://deta.space/), click on `Settings` and then select `Generate Token`. Copy the token and paste it into the CLI prompt. Upon entering the token and pressing enter, you should see a confirmation message.

<img src="/img/deployment/deta/image01.png">

## Create a new project in Space

Now create a new project from the Space CLI with:

```console
$ space new

? What is your project's name? > fastapi-deta
```

The Space CLI will ask you to name the project, we will call ours `fastapi-deta`. Then it will try to detect which framework or language you are using and show you what’s found. In our case it should correctly indentify our python app with the following message, prompting you to confirm:

```console
⚙️ No Spacefile found, trying to auto-detect configuration ...
👇 Deta detected the following configuration:

Micros:
name: fastapi-deta
 L src: .
 L engine: python3.9

? Do you want to bootstrap "fastapi-deta" with this configuration? (y/n)
y
```

This will create a new project in Builder and a Spacefile in the `fastapi-deta` directory.


Projects in Space live inside [Builder](https://deta.space/docs/en/basics/projects#projects-in-builder), which you can access from the Canvas. Builder is like a toolbox that helps you to create and manage your app on Space.

The [Spacefile](https://deta.space/docs/en/reference/spacefile) has the configuration details of your app and Space needs it to know what your app looks like and how to get it running. You can adjust it based on your requirements, following the instructions in the docs.

```yaml
v: 0
micros:
  - name: fastapi-deta
    src: .
    engine: python3.9
```

The CLI will also create a hidden .space folder in the same directory with all the information necessary to work with your project in Builder. This folder should not be included in your version control and will automatically get added to your .gitignore file, if you have initialized a Git repository.

## Deploy to Space

Next, deploy your application using Space CLI with:

<div class="termy">

```console
$ space push

...
build complete... created revision: satyr-jvjk

✔ Successfully pushed your code and created a new Revision!
ℹ Updating your developement instance with the latest Revision, it will be available on your Canvas shortly.
```
</div>

This will package and upload all the necessary files to create a new `revision`. A revision is a complete package of your app at one moment in time. A new revision is created with each push. You can take a look at this new revision by opening your project in Builder. It'll be visible on the `Develop` tab.

## Check it

Whenever you run `space push` successfully, a live instance of your project is automatically updated.

This instance is automatically added to your Canvas on Deta Space. Clicking on the instance's card will open it in your browser with an endpoint URL like `https://fastapideta-gj7ka8.deta.app/`.

You will get a JSON response from your FastAPI app:

```JSON
{
    "Hello": "World"
}
```

And now you can head over to the `/docs` of your API. For this example, it would be `https://fastapi-deta-gj7ka8.deta.app/docs`.

It will show your docs like:

<img src="/img/deployment/deta/image02.png">

## Enable public access

By default, Deta will handle authentication for your account.

But once you are ready, you can make it public by defining which paths of your API should be available to the public with the `public_routes` parameter in your project's Spacefile.

Setting your `public_routes` to `/*` will open every route to the public:

```yaml
v: 0
micros:
  - name: fastapi-deta
    src: .
    engine: python3.9
    public_routes:
      - '/*'
```

Run `space push` again to update your personal instance on Deta Space.

Once it deploys, now you can share your URL with anyone and they will be able to access your API. 🚀

## HTTPS

Congrats! You deployed your FastAPI app to Deta Space! 🎉 🍰

Also, notice that Deta Space correctly handles HTTPS for you, so you don't have to take care of that and can be sure that your clients will have a secure encrypted connection. ✅ 🔒

## Check Runtime Logs

Now taking a look at the code in main.py of the FastAPI app, you'll find that the second route, "/items/{item_id}", is managed by the read_item() function. The code within this function includes a print statement that will output the item_id that is included in the URL. To send a request to your _path operation_ `/items/{item_id}` from the docs UI (which will have a URL like `https://fastapi-deta-gj7ka8.deta.app/docs`), use an ID such as `5` as an example.

Now go to your Space's Canvas <a href="https://deta.space" class="external-link" target="_blank">https://deta.space</a>.

Click on the context menu (`...`) of your app instance. Now click on `Resources`.

Under the `Develop` tab, you can view the logs of your development instance, sorted by time under the `Runtime logs`.

<img src="/img/deployment/deta/image03.png">

## Create a release

Space also allows lets you publish your API, so anyone in the can to install their own copy.

To do so, you can create a Unlisted Release of your app using the Space CLI:

```console
space release
```

This command will publish your app and give you a Release link. Only people given this link can install it.

You can also make your app publicly discoverable on [Deta Discovery](https://deta.space/docs/en/basics/releases#discovery--app-pages?ref=fastapi) by creating a Listed Release with the Space CLI:

```console
space release --listed
```

This will allow anyone to find and install your API via Deta Discovery.

## Learn more

At some point, you will probably want to store some data for your app in a way that persists through time. For that you can use <a href="https://deta.space/docs/en/basics/data#deta-base?ref=fastapi" class="external-link" target="_blank">Deta Base</a> and <a href="https://deta.space/docs/en/basics/data#drive?ref=fastapi" class="external-link" target="_blank">Deta Drive</a>.

You can also read more in the <a href="https://deta.space/docs/?ref=fastapi" class="external-link" target="_blank">Space Docs</a>.

## Deployment Concepts

Coming back to the concepts we discussed in [Deployments Concepts](./concepts.md){.internal-link target=\_blank}, here's how each of them would be handled with Deta Space:

- **HTTPS**: Handled by Deta Space, they will give you a subdomain and handle HTTPS automatically.
- **Running on startup**: Handled by Deta Space, as part of their service.
- **Restarts**: Handled by Deta Space, as part of their service.
- **Replication**: Handled by Deta Space, as part of their service.
- **Memory**: Limit predefined by Deta Space, you could contact them to increase it.
- **Previous steps before starting**: Not directly supported, you could make it work with their Cron system or additional scripts.

!!! note
    Deta Space is designed to make it easy (and free) to deploy simple applications quickly.

    It can simplify several use cases, but at the same time, it doesn't support others, like using external databases (apart from Deta's own NoSQL database system), custom virtual machines, etc.

    You can read more details in the <a href="https://deta.space/docs/en/basics/micros" class="external-link" target="_blank">Deta Space docs</a> to see if it's the right choice for you.
