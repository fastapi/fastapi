import inspect
import os

import requests

room_id = "5c9c9540d73408ce4fbc1403"  # FastAPI
# room_id = "5cc46398d73408ce4fbed233"  # Gitter development

gitter_token = os.getenv("GITTER_TOKEN")
assert gitter_token
github_token = os.getenv("GITHUB_TOKEN")
assert github_token
tag_name = os.getenv("TRAVIS_TAG")
assert tag_name


def get_github_graphql(tag_name: str):
    github_graphql = """
    {
    repository(owner: "tiangolo", name: "fastapi") {
        release (tagName: "{{tag_name}}" ) {
        description
        }
      }
    }
    """
    github_graphql = github_graphql.replace("{{tag_name}}", tag_name)
    return github_graphql


def get_github_release_text(tag_name: str):
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {github_token}"}
    github_graphql = get_github_graphql(tag_name=tag_name)
    response = requests.post(url, json={"query": github_graphql}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    return data["data"]["repository"]["release"]["description"]


def get_gitter_message(release_text: str):
    text = f"""
    New release! :tada: :rocket:
    (by FastAPI bot)

    ## {tag_name}
    """
    text = inspect.cleandoc(text) + "\n\n" + release_text
    return text


def send_gitter_message(text: str):
    headers = {"Authorization": f"Bearer {gitter_token}"}
    url = f"https://api.gitter.im/v1/rooms/{room_id}/chatMessages"
    data = {"text": text}
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 200


def main():
    release_text = get_github_release_text(tag_name=tag_name)
    text = get_gitter_message(release_text=release_text)
    send_gitter_message(text=text)


if __name__ == "__main__":
    main()
