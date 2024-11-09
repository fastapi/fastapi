# Repository Management Tasks

These are the tasks that can be performed to manage the FastAPI repository by [team members](./fastapi-people.md#team){.internal-link target=_blank}.

/// tip

This section is useful only to a handful of people, team members with permissions to manage the repository. You can probably skip it. 😉

///

...so, you are a [team member of FastAPI](./fastapi-people.md#team){.internal-link target=_blank}? Wow, you are so cool! 😎

You can help with everything on [Help FastAPI - Get Help](./help-fastapi.md){.internal-link target=_blank} the same ways as external contributors. But additionally, there are some tasks that only you (as part of the team) can perform.

Here are the general instructions for the tasks you can perform.

Thanks a lot for your help. 🙇

## Be Nice

First of all, be nice. 😊

You probably are super nice if you were added to the team, but it's worth mentioning it. 🤓

### When Things are Difficult

When things are great, everything is easier, so that doesn't need much instructions. But when things are difficult, here are some guidelines.

Try to find the good side. In general, if people are not being unfriendly, try to thank their effort and interest, even if you disagree with the main subject (discussion, PR), just thank them for being interested in the project, or for having dedicated some time to try to do something.

It's difficult to convey emotion in text, use emojis to help. 😅

In discussions and PRs, in many cases, people bring their frustration and show it without filter, in many cases exaggerating, complaining, being entitled, etc. That's really not nice, and when it happens, it lowers our priority to solve their problems. But still, try to breath, and be gentle with your answers.

Try to avoid using bitter sarcasm or potentially passive-aggressive comments. If something is wrong, it's better to be direct (try to be gentle) than sarcastic.

Try to be as specific and objective as possible, avoid generalizations.

For conversations that are more difficult, for example to reject a PR, you can ask me (@tiangolo) to handle it directly.

## Edit PR Titles

* Edit the PR title to start with an emoji from <a href="https://gitmoji.dev/" class="external-link" target="_blank">gitmoji</a>.
    * Use the emoji character, not the GitHub code. So, use `🐛` instead of `:bug:`. This is so that it shows up correctly outside of GitHub, for example in the release notes.
    * For translations use the `🌐` emoji ("globe with meridians").
* Start the title with a verb. For example `Add`, `Refactor`, `Fix`, etc. This way the title will say the action that the PR does. Like `Add support for teleporting`, instead of `Teleporting wasn't working, so this PR fixes it`.
* Edit the text of the PR title to start in "imperative", like giving an order. So, instead of `Adding support for teleporting` use `Add support for teleporting`.
* Try to make the title descriptive about what it achieves. If it's a feature, try to describe it, for example `Add support for teleporting` instead of `Create TeleportAdapter class`.
* Do not finish the title with a period (`.`).
* When the PR is for a translation, start with the `🌐` and then `Add {language} translation for` and then the translated file path. For example:

```Markdown
🌐 Add Spanish translation for `docs/es/docs/teleporting.md`
```

Once the PR is merged, a GitHub Action (<a href="https://github.com/tiangolo/latest-changes" class="external-link" target="_blank">latest-changes</a>) will use the PR title to update the latest changes automatically.

So, having a nice PR title will not only look nice in GitHub, but also in the release notes. 📝

## Add Labels to PRs

The same GitHub Action <a href="https://github.com/tiangolo/latest-changes" class="external-link" target="_blank">latest-changes</a> uses one label in the PR to decide the section in the release notes to put this PR in.

Make sure you use a supported label from the <a href="https://github.com/tiangolo/latest-changes#using-labels" class="external-link" target="_blank">latest-changes list of labels</a>:

* `breaking`: Breaking Changes
    * Existing code will break if they update the version without changing their code. This rarely happens, so this label is not frequently used.
* `security`: Security Fixes
    * This is for security fixes, like vulnerabilities. It would almost never be used.
* `feature`: Features
    * New features, adding support for things that didn't exist before.
* `bug`: Fixes
    * Something that was supported didn't work, and this fixes it. There are many PRs that claim to be bug fixes because the user is doing something in an unexpected way that is not supported, but they considered it what should be supported by default. Many of these are actually features or refactors. But in some cases there's an actual bug.
* `refactor`: Refactors
    * This is normally for changes to the internal code that don't change the behavior. Normally it improves maintainability, or enables future features, etc.
* `upgrade`: Upgrades
    * This is for upgrades to direct dependencies from the project, or extra optional dependencies, normally in `pyproject.toml`. So, things that would affect final users, they would end up receiving the upgrade in their code base once they update. But this is not for upgrades to internal dependencies used for development, testing, docs, etc. Those internal dependencies, normally in `requirements.txt` files or GitHub Action versions should be marked as `internal`, not `upgrade`.
* `docs`: Docs
    * Changes in docs. This includes updating the docs, fixing typos. But it doesn't include changes to translations.
    * You can normally quickly detect it by going to the "Files changed" tab in the PR and checking if the updated file(s) starts with `docs/en/docs`. The original version of the docs is always in English, so in `docs/en/docs`.
* `lang-all`: Translations
    * Use this for translations. You can normally quickly detect it by going to the "Files changed" tab in the PR and checking if the updated file(s) starts with `docs/{some lang}/docs` but not `docs/en/docs`. For example, `docs/es/docs`.
* `internal`: Internal
    * Use this for changes that only affect how the repo is managed. For example upgrades to internal dependencies, changes in GitHub Actions or scripts, etc.

/// tip

Some tools like Dependabot, will add some labels, like `dependencies`, but have in mind that this label is not used by the `latest-changes` GitHub Action, so it won't be used in the release notes. Please make sure one of the labels above is added.

///

## Add Labels to Translation PRs

When there's a PR for a translation, apart from adding the `lang-all` label, also add a label for the language.

There will be a label for each language using the language code, like `lang-{lang code}`, for example, `lang-es` for Spanish, `lang-fr` for French, etc.

* Add the specific language label.
* Add the label `awaiting-review`.

The label `awaiting-review` is special, only used for translations. A GitHub Action will detect it, then it will read the language label, and it will update the GitHub Discussions managing the translations for that language to notify people that there's a new translation to review.

Once a native speaker comes, reviews the PR, and approves it, the GitHub Action will come and remove the `awaiting-review` label, and add the `approved-1` label.

This way, we can notice when there are new translations ready, because they have the `approved-1` label.

## Merge Translation PRs

For Spanish, as I'm a native speaker and it's a language close to me, I will give it a final review myself and in most cases tweak the PR a bit before merging it.

For the other languages, confirm that:

* The title is correct following the instructions above.
* It has the labels `lang-all` and `lang-{lang code}`.
* The PR changes only one Markdown file adding a translation.
    * Or in some cases, at most two files, if they are small, for the same language, and people reviewed them.
    * If it's the first translation for that language, it will have additional `mkdocs.yml` files, for those cases follow the instructions below.
* The PR doesn't add any additional or extraneous files.
* The translation seems to have a similar structure as the original English file.
* The translation doesn't seem to change the original content, for example with obvious additional documentation sections.
* The translation doesn't use different Markdown structures, for example adding HTML tags when the original didn't have them.
* The "admonition" sections, like `tip`, `info`, etc. are not changed or translated. For example:

```
/// tip

This is a tip.

///

```

looks like this:

/// tip

This is a tip.

///

...it could be translated as:

```
/// tip

Esto es un consejo.

///

```

...but needs to keep the exact `tip` keyword. If it was translated to `consejo`, like:

```
/// consejo

Esto es un consejo.

///

```

it would change the style to the default one, it would look like:

/// consejo

Esto es un consejo.

///

Those don't have to be translated, but if they are, they need to be written as:

```
/// tip | consejo

Esto es un consejo.

///

```

Which looks like:

/// tip | consejo

Esto es un consejo.

///

## First Translation PR

When there's a first translation for a language, it will have a `docs/{lang code}/docs/index.md` translated file and a `docs/{lang code}/mkdocs.yml`.

For example, for Bosnian, it would be:

* `docs/bs/docs/index.md`
* `docs/bs/mkdocs.yml`

The `mkdocs.yml` file will have only the following content:

```YAML
INHERIT: ../en/mkdocs.yml
```

The language code would normally be in the <a href="https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes" class="external-link" target="_blank">ISO 639-1 list of language codes</a>.

In any case, the language code should be in the file <a href="https://github.com/fastapi/fastapi/blob/master/docs/language_names.yml" class="external-link" target="_blank">docs/language_names.yml</a>.

There won't be yet a label for the language code, for example, if it was Bosnian, there wouldn't be a `lang-bs`. Before creating the label and adding it to the PR, create the GitHub Discussion:

* Go to the <a href="https://github.com/fastapi/fastapi/discussions/categories/translations" class="external-link" target="_blank">Translations GitHub Discussions</a>
* Create a new discussion with the title `Bosnian Translations` (or the language name in English)
* A description of:

```Markdown
## Bosnian translations

This is the issue to track translations of the docs to Bosnian. 🚀

Here are the [PRs to review with the label `lang-bs`](https://github.com/fastapi/fastapi/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc+label%3Alang-bs+label%3A%22awaiting-review%22). 🤓
```

Update "Bosnian" with the new language.

And update the search link to point to the new language label that will be created, like `lang-bs`.

Create and add the label to that new Discussion just created, like `lang-bs`.

Then go back to the PR, and add the label, like `lang-bs`, and `lang-all` and `awaiting-review`.

Now the GitHub action will automatically detect the label `lang-bs` and will post in that Discussion that this PR is waiting to be reviewed.

## Review PRs

If a PR doesn't explain what it does or why, ask for more information.

A PR should have a specific use case that it is solving.

* If the PR is for a feature, it should have docs.
    * Unless it's a feature we want to discourage, like support for a corner case that we don't want users to use.
* The docs should include a source example file, not write Python directly in Markdown.
* If the source example(s) file can have different syntax for Python 3.8, 3.9, 3.10, there should be different versions of the file, and they should be shown in tabs in the docs.
* There should be tests testing the source example.
* Before the PR is applied, the new tests should fail.
* After applying the PR, the new tests should pass.
* Coverage should stay at 100%.
* If you see the PR makes sense, or we discussed it and considered it should be accepted, you can add commits on top of the PR to tweak it, to add docs, tests, format, refactor, remove extra files, etc.
* Feel free to comment in the PR to ask for more information, to suggest changes, etc.
* Once you think the PR is ready, move it in the internal GitHub project for me to review it.

## FastAPI People PRs

Every month, a GitHub Action updates the FastAPI People data. Those PRs look like this one: <a href="https://github.com/fastapi/fastapi/pull/11669" class="external-link" target="_blank">👥 Update FastAPI People</a>.

If the tests are passing, you can merge it right away.

## External Links PRs

When people add external links they edit this file <a href="https://github.com/fastapi/fastapi/blob/master/docs/en/data/external_links.yml" class="external-link" target="_blank">external_links.yml</a>.

* Make sure the new link is in the correct category (e.g. "Podcasts") and language (e.g. "Japanese").
* A new link should be at the top of its list.
* The link URL should work (it should not return a 404).
* The content of the link should be about FastAPI.
* The new addition should have these fields:
    * `author`: The name of the author.
    * `link`: The URL with the content.
    * `title`: The title of the link (the title of the article, podcast, etc).

After checking all these things and ensuring the PR has the right labels, you can merge it.

## Dependabot PRs

Dependabot will create PRs to update dependencies for several things, and those PRs all look similar, but some are way more delicate than others.

* If the PR is for a direct dependency, so, Dependabot is modifying `pyproject.toml`, **don't merge it**. 😱 Let me check it first. There's a good chance that some additional tweaks or updates are needed.
* If the PR updates one of the internal dependencies, for example it's modifying `requirements.txt` files, or GitHub Action versions, if the tests are passing, the release notes (shown in a summary in the PR) don't show any obvious potential breaking change, you can merge it. 😎

## Mark GitHub Discussions Answers

When a question in GitHub Discussions has been answered, mark the answer by clicking "Mark as answer".

You can filter discussions by <a href="https://github.com/tiangolo/fastapi/discussions/categories/questions?discussions_q=category:Questions+is:open+is:unanswered" class="external-link" target="_blank">`Questions` that are `Unanswered`</a>.
