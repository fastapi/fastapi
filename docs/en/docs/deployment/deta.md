# Deploy FastAPI on Deta Space

In this section you will learn how to easily deploy a **FastAPI** application on <a href="https://deta.space?ref=fastapi" class="external-link" target="_blank">Deta Space</a>, for free. 🎁

It will take you about **10 minutes** to deploy an API that you can use. After that, you can optionally release it to anyone.

Let's dive in.

!!! info
    <a href="https://deta.space?ref=fastapi" class="external-link" target="_blank">Deta</a> is a **FastAPI** sponsor. 🎉

## A simple **FastAPI** app

* To start, create an empty directory with the name of your app, for example `./fastapi-deta/`, and then navigate into it.

```console
$ mkdir fastapi-deta
$ cd fastapi-deta
```

### FastAPI code

* Create a `main.py` file with:

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

### Requirements

Now, in the same directory create a file `requirements.txt` with:

```text
fastapi
uvicorn[standard]
```

### Directory structure

You will now have a directory `./fastapi-deta/` with two files:

```
.
└── main.py
└── requirements.txt
```

## Create a free **Deta Space** account

Next, create a free account on <a href="https://deta.space/signup?dev_mode=true&ref=fastapi" class="external-link" target="_blank">Deta Space</a>, you just need an email and password.

You don't even need a credit card, but make sure **Developer Mode** is enabled when you sign up.


## Install the CLI

Once you have your account, install the Deta Space <abbr title="Command Line Interface application">CLI</abbr>:

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
    If you have problems installing the CLI, check the official <a href="https://deta.space/docs/en/basics/cli?ref=fastapi" class="external-link" target="_blank">Deta Space Documentation</a>.

## Login with the CLI

In order to authenticate your CLI with Deta Space, you will need an access token.

To obtain this token, open your <a href="https://deta.space/login?ref=fastapi" class="external-link" target="_blank">Deta Space Canvas</a>, open the **Teletype** (command bar at the bottom of the Canvas), and then click on **Settings**. From there, select **Generate Token** and copy the resulting token.

<img src="/img/deployment/deta/image03.png">

Now run `space login` from the Space CLI. Upon pasting the token into the CLI prompt and pressing enter, you should see a confirmation message.

<div class="termy">

```console
$ space login

To authenticate the Space CLI with your Space account, generate a new access token in your Space settings and paste it below:

# Enter access token (41 chars) >$ *****************************************

👍 Login Successful!
```

</div>

## Create a new project in Space

Now that you've authenticated with the Space CLI, use it to create a new <a href="https://deta.space/docs/en/basics/projects" class="external-link" target="_blank">Space Project</a>:

```console
$ space new

# What is your project's name? >$ fastapi-deta
```

The Space CLI will ask you to name the project, we will call ours `fastapi-deta`.

Then, it will try to automatically detect which framework or language you are using, showing you what it finds. In our case it will identify the Python app with the following message, prompting you to confirm:

```console
⚙️ No Spacefile found, trying to auto-detect configuration ...
👇 Deta detected the following configuration:

Micros:
name: fastapi-deta
 L src: .
 L engine: python3.9

# Do you want to bootstrap "fastapi-deta" with this configuration? (y/n)$ y
```

After you confirm, your project will be created in Deta Space inside a special app called <a href="https://deta.space/docs/en/basics/projects#projects-in-builder?ref=fastapi" class="external-link" target="_blank">Builder</a>. Builder is a toolbox that helps you to create and manage your apps in Deta Space.

The CLI will also create a `Spacefile` locally in the `fastapi-deta` directory. The <a href="https://deta.space/docs/en/reference/spacefile?ref=fastapi" class="external-link" target="_blank">Spacefile</a> is a configuration file which tells Deta Space how to run your app. The `Spacefile` for your app will be as follows:

```yaml
v: 0
micros:
  - name: fastapi-deta
    src: .
    engine: python3.9
```

It is a `yaml` file, and you can use it to add features like scheduled tasks or modify how your app functions, which we'll do later. To learn more, read <a href="https://deta.space/docs/en/reference/spacefile" class="external-link" target="_blank">the `Spacefile` documentation</a>.

!!! tip
    The Space CLI will also create a hidden `.space` folder in your local directory to link your local environment with Deta Space. This folder should not be included in your version control and will automatically be added to your `.gitignore` file, if you have initialized a Git repository.

## Define the run command in the Spacefile

The `run` command in the Spacefile tells Space what command should be executed to start your app. In this case it would be `uvicorn main:app`.

```diff
v: 0
micros:
  - name: fastapi-deta
    src: .
    engine: python3.9
+   run: uvicorn main:app
```

## Deploy to Deta Space

To get your FastAPI live in the cloud, use one more CLI command:

<div class="termy">

```console
$ space push

---> 100%

build complete... created revision: satyr-jvjk

✔ Successfully pushed your code and created a new Revision!
ℹ Updating your development instance with the latest Revision, it will be available on your Canvas shortly.
```
</div>

This command will package your code, upload all the necessary files to Deta Space, and run a remote build of your app, resulting in a **revision**. Whenever you run `space push` successfully, a live instance of your API is automatically updated with the latest revision.

!!! tip
    You can manage your <a href="https://deta.space/docs/en/basics/revisions#whats-a-revision" class="external-link" target="_blank">revisions</a> by opening your project in the Builder app. The live copy of your API will be visible under the **Develop** tab in Builder.

## Check it

The live instance of your API will also be added automatically to your Canvas (the dashboard) on Deta Space.

<img src="/img/deployment/deta/image04.png">

Click on the new app called `fastapi-deta`, and it will open your API in a new browser tab on a URL like `https://fastapi-deta-gj7ka8.deta.app/`.

You will get a JSON response from your FastAPI app:

```JSON
{
    "Hello": "World"
}
```

And now you can head over to the `/docs` of your API. For this example, it would be `https://fastapi-deta-gj7ka8.deta.app/docs`.

<img src="/img/deployment/deta/image05.png">

## Enable public access

Deta will handle authentication for your account using cookies. By default, every app or API that you `push` or install to your Space is personal - it's only accessible to you.

But you can also make your API public using the `Spacefile` from earlier.

With a `public_routes` parameter, you can specify which paths of your API should be available to the public.

Set your `public_routes` to `"*"` to open every route of your API to the public:

```yaml
v: 0
micros:
  - name: fastapi-deta
    src: .
    engine: python3.9
    public_routes:
      - "/*"
```

Then run `space push` again to update your live API on Deta Space.

Once it deploys, you can share your URL with anyone and they will be able to access your API. 🚀

## HTTPS

Congrats! You deployed your FastAPI app to Deta Space! 🎉 🍰

Also, notice that Deta Space correctly handles HTTPS for you, so you don't have to take care of that and can be sure that your users will have a secure encrypted connection. ✅ 🔒

## Create a release

Space also allows you to publish your API. When you publish it, anyone else can install their own copy of your API, in their own Deta Space cloud.

To do so, run `space release` in the Space CLI to create an **unlisted release**:

<div class="termy">

```console
$ space release

# Do you want to use the latest revision (buzzard-hczt)? (y/n)$ y

~ Creating a Release with the latest Revision

---> 100%

creating release...
publishing release in edge locations..
completed...
released: fastapi-deta-exp-msbu
https://deta.space/discovery/r/5kjhgyxewkdmtotx

 Lift off -- successfully created a new Release!
 Your Release is available globally on 5 Deta Edges
 Anyone can install their own copy of your app.
```
</div>

This command publishes your revision as a release and gives you a link. Anyone you give this link to can install your API.


You can also make your app publicly discoverable by creating a **listed release** with `space release --listed` in the Space CLI:

<div class="termy">

```console
$ space release --listed

# Do you want to use the latest revision (buzzard-hczt)? (y/n)$ y

~ Creating a listed Release with the latest Revision ...

creating release...
publishing release in edge locations..
completed...
released: fastapi-deta-exp-msbu
https://deta.space/discovery/@user/fastapi-deta

 Lift off -- successfully created a new Release!
 Your Release is available globally on 5 Deta Edges
 Anyone can install their own copy of your app.
 Listed on Discovery for others to find!
```
</div>

This will allow anyone to find and install your app via <a href="https://deta.space/discovery?ref=fastapi" class="external-link" target="_blank">Deta Discovery</a>. Read more about <a href="https://deta.space/docs/en/basics/releases?ref=fastapi" class="external-link" target="_blank">releasing your app in the docs</a>.

## Check runtime logs

Deta Space also lets you inspect the logs of every app you build or install.

Add some logging functionality to your app by adding a `print` statement to your `main.py` file.

```py
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    print(item_id)
    return {"item_id": item_id}
```

The code within the `read_item` function includes a print statement that will output the `item_id` that is included in the URL. Send a request to your _path operation_ `/items/{item_id}` from the docs UI (which will have a URL like `https://fastapi-deta-gj7ka8.deta.app/docs`), using an ID like `5` as an example.

Now go to your <a href="https://deta.space?ref=fastapi" class="external-link" target="_blank">Space's Canvas</a>. Click on the context menu (`...`) of your live app instance, and then click on **View Logs**. Here you can view your app's logs, sorted by time.

<img src="/img/deployment/deta/image06.png">

## Learn more

At some point, you will probably want to store some data for your app in a way that persists through time. For that you can use <a href="https://deta.space/docs/en/basics/data#deta-base?ref=fastapi" class="external-link" target="_blank">Deta Base</a> and <a href="https://deta.space/docs/en/basics/data#deta-drive?ref=fastapi" class="external-link" target="_blank">Deta Drive</a>, both of which have a generous **free tier**.

You can also read more in the <a href="https://deta.space/docs/?ref=fastapi" class="external-link" target="_blank">Deta Space Documentation</a>.

!!! tip
    If you have any Deta related questions, comments, or feedback, head to the <a href="https://go.deta.dev/discord" class="external-link" target="_blank">Deta Discord server</a>.


## Deployment Concepts

Coming back to the concepts we discussed in [Deployments Concepts](./concepts.md){.internal-link target=_blank}, here's how each of them would be handled with Deta Space:

- **HTTPS**: Handled by Deta Space, they will give you a subdomain and handle HTTPS automatically.
- **Running on startup**: Handled by Deta Space, as part of their service.
- **Restarts**: Handled by Deta Space, as part of their service.
- **Replication**: Handled by Deta Space, as part of their service.
- **Authentication**: Handled by Deta Space, as part of their service.
- **Memory**: Limit predefined by Deta Space, you could contact them to increase it.
- **Previous steps before starting**: Can be configured using the <a href="https://deta.space/docs/en/reference/spacefile?ref=fastapi" class="external-link" target="_blank">`Spacefile`</a>.

!!! note
    Deta Space is designed to make it easy and free to build cloud applications for yourself. Then you can optionally share them with anyone.

    It can simplify several use cases, but at the same time, it doesn't support others, like using external databases (apart from Deta's own NoSQL database system), custom virtual machines, etc.

    You can read more details in the <a href="https://deta.space/docs/en/basics/micros?ref=fastapi" class="external-link" target="_blank">Deta Space Documentation</a> to see if it's the right choice for you.
