You can create (set) Cookies in your response.

To do that, you can create a response as described in <a href="https://fastapi.tiangolo.com/tutorial/response-directly/" target="_blank">Return a Response directly</a>.

Then set Cookies in it, and then return it:

```Python hl_lines="10 11 12"
{!./src/response_cookies/tutorial001.py!}
```

## More info

To see all the available parameters and options, check the <a href="https://www.starlette.io/responses/#set-cookie" target="_blank">documentation in Starlette</a>.
