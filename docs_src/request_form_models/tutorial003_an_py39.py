from typing import Annotated

from pydantic import BaseModel
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import DictLoader, Environment

class MyModel(BaseModel):
    checkbox: bool = True

form_template = """
<form action="/form" method="POST">
{% for field_name, field in model.model_fields.items() %}
<p>
  <label for="{{ field_name }}">{{ field_name }}</label>
  {% if field.annotation.__name__ == "bool" %}
  <input type="checkbox" name="{{field_name}}"
    {% if field.default %} 
    checked="checked"
    {% endif %}
  >
  {% else %}
  <input name="{{ field_name }}">
  {% endif %}
</p>
{% endfor %}
<button type="submit">Submit</button>
</form>
"""
loader = DictLoader({"form.html": form_template})
templates = Jinja2Templates(env=Environment(loader=loader))

app = FastAPI()

@app.get("/form", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse(
        request=request, name="form.html", context={"model": MyModel}
    )

@app.post('/form')
async def submit_form(data: Annotated[MyModel, Form()]) -> MyModel:
    return data
