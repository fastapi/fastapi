# OpenAPI condicional { #conditional-openapi }

Se necessário, você pode usar configurações e variáveis de ambiente para configurar o OpenAPI condicionalmente dependendo do ambiente e até mesmo desativá-lo completamente.

## Sobre segurança, APIs e documentação { #about-security-apis-and-docs }

Ocultar suas interfaces de usuário de documentação na produção não *deveria* ser a maneira de proteger sua API.

Isso não adiciona nenhuma segurança extra à sua API; as *operações de rota* ainda estarão disponíveis onde estão.

Se houver uma falha de segurança no seu código, ela ainda existirá.

Ocultar a documentação apenas torna mais difícil entender como interagir com sua API e pode dificultar sua depuração na produção. Pode ser considerado simplesmente uma forma de <a href="https://en.wikipedia.org/wiki/Security_through_obscurity" class="external-link" target="_blank">Segurança através da obscuridade</a>.

Se você quiser proteger sua API, há várias coisas melhores que você pode fazer, por exemplo:

* Certifique-se de ter modelos Pydantic bem definidos para seus corpos de solicitação e respostas.
* Configure quaisquer permissões e funções necessárias usando dependências.
* Nunca armazene senhas em texto simples, apenas hashes de senha.
* Implemente e use ferramentas criptográficas bem conhecidas, como pwdlib e tokens JWT, etc.
* Adicione controles de permissão mais granulares com escopos OAuth2 quando necessário.
* ...etc.

No entanto, você pode ter um caso de uso muito específico em que realmente precisa desabilitar a documentação da API para algum ambiente (por exemplo, para produção) ou dependendo de configurações de variáveis de ambiente.

## OpenAPI condicional com configurações e variáveis de ambiente { #conditional-openapi-from-settings-and-env-vars }

Você pode usar facilmente as mesmas configurações do Pydantic para configurar sua OpenAPI gerada e as interfaces de usuário da documentação.

Por exemplo:

{* ../../docs_src/conditional_openapi/tutorial001.py hl[6,11] *}

Aqui declaramos a configuração `openapi_url` com o mesmo padrão de `"/openapi.json"`.

E então a usamos ao criar a aplicação `FastAPI`.

Então você pode desabilitar o OpenAPI (incluindo a documentação da interface do usuário) definindo a variável de ambiente `OPENAPI_URL` como uma string vazia, como:

<div class="termy">

```console
$ OPENAPI_URL= uvicorn main:app

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Então, se você acessar as URLs em `/openapi.json`, `/docs` ou `/redoc`, você receberá apenas um erro `404 Not Found` como:

```JSON
{
    "detail": "Not Found"
}
```
