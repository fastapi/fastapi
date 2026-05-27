# Translations

Translation pull requests are made by LLMs guided with prompts designed by the FastAPI team together with the community of native speakers for each supported language.

## LLM Prompt per Language

Each language has a directory: [https://github.com/fastapi/fastapi/tree/master/docs](https://github.com/fastapi/fastapi/tree/master/docs), in it you can see a file `llm-prompt.md` with the prompt specific for that language.

For example, for Spanish, the prompt is at: [`docs/es/llm-prompt.md`](https://github.com/fastapi/fastapi/blob/master/docs/es/llm-prompt.md).

If you see mistakes in your language, you can make suggestions to the prompt in that file for your language, and request the specific pages you would like to re-generate after the changes.

PRs with suggestions to the language-specific LLM prompt require approval from at least one native speaker. Your help here is very much appreciated!

## Request a New Language

Let's say that you want to request translations for a language that is not yet translated, not even some pages. For example, Latin.

* The first step would be for you to find other 2 people that would be willing to be reviewing translation PRs for that language with you.
* Once there are at least 3 people that would be willing to commit to help maintain that language, you can continue the next steps.
* Create a new discussion following the template.
* Tag the other 2 people that will help with the language, and ask them to confirm there they will help.

Once there are several people in the discussion, the FastAPI team can evaluate it and can make it an official translation.

Then the docs will be automatically translated using LLMs, and the team of native speakers can review the translation, and help tweak the LLM prompts.

Once there's a new translation, for example if docs are updated or there's a new section, there will be a comment in the same discussion with the link to the new translation to review.
