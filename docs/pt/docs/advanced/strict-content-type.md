# Verificação Estrita de Content-Type { #strict-content-type-checking }

Por padrão, o **FastAPI** usa verificação estrita do cabeçalho `Content-Type` para corpos de requisição JSON; isso significa que requisições JSON devem incluir um `Content-Type` válido (por exemplo, `application/json`) para que o corpo seja interpretado como JSON.

## Risco de CSRF { #csrf-risk }

Esse comportamento padrão oferece proteção contra uma classe de ataques de **Cross-Site Request Forgery (CSRF)** em um cenário muito específico.

Esses ataques exploram o fato de que navegadores permitem que scripts enviem requisições sem fazer qualquer verificação de preflight de CORS quando:

- não têm um cabeçalho `Content-Type` (por exemplo, usando `fetch()` com um corpo `Blob`)
- e não enviam nenhuma credencial de autenticação.

Esse tipo de ataque é relevante principalmente quando:

- a aplicação está em execução localmente (por exemplo, em `localhost`) ou em uma rede interna
- e a aplicação não tem autenticação, pressupondo que qualquer requisição da mesma rede é confiável.

## Exemplo de Ataque { #example-attack }

Imagine que você desenvolve uma forma de executar um agente de IA local.

Ele fornece uma API em

```
http://localhost:8000/v1/agents/multivac
```

Há também um frontend em

```
http://localhost:8000
```

/// tip | Dica

Observe que ambos têm o mesmo host.

///

Usando o frontend, você pode fazer o agente de IA executar ações em seu nome.

Como está em execução localmente e não na Internet aberta, você decide não configurar autenticação, confiando apenas no acesso à rede local.

Então um de seus usuários poderia instalá-lo e executá-lo localmente.

Em seguida, poderia abrir um site malicioso, por exemplo:

```
https://evilhackers.example.com
```

E esse site malicioso envia requisições usando `fetch()` com um corpo `Blob` para a API local em

```
http://localhost:8000/v1/agents/multivac
```

Mesmo que o host do site malicioso e o da aplicação local sejam diferentes, o navegador não acionará uma requisição preflight de CORS porque:

- Está em execução sem autenticação, não precisa enviar credenciais.
- O navegador acha que não está enviando JSON (devido à falta do cabeçalho `Content-Type`).

Então o site malicioso poderia fazer o agente de IA local enviar mensagens raivosas ao ex-chefe do usuário... ou pior. 😅

## Internet Aberta { #open-internet }

Se sua aplicação está na Internet aberta, você não “confiaria na rede” nem deixaria qualquer pessoa enviar requisições privilegiadas sem autenticação.

Atacantes poderiam simplesmente executar um script para enviar requisições à sua API, sem necessidade de interação do navegador, então você provavelmente já está protegendo quaisquer endpoints privilegiados.

Nesse caso, esse ataque/risco não se aplica a você.

Esse risco e ataque é relevante principalmente quando a aplicação roda na rede local e essa é a única proteção presumida.

## Permitindo Requisições sem Content-Type { #allowing-requests-without-content-type }

Se você precisa dar suporte a clientes que não enviam um cabeçalho `Content-Type`, você pode desativar a verificação estrita definindo `strict_content_type=False`:

{* ../../docs_src/strict_content_type/tutorial001_py310.py hl[4] *}

Com essa configuração, requisições sem um cabeçalho `Content-Type` terão o corpo interpretado como JSON, o mesmo comportamento das versões mais antigas do FastAPI.

/// info | Informação

Esse comportamento e configuração foram adicionados no FastAPI 0.132.0.

///
