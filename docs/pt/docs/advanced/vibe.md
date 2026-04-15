# Codificação por Vibe { #vibe-coding }

Você está cansado de toda aquela **validação de dados**, **documentação**, **serialização** e todas aquelas coisas **chatas**?

Você só quer entrar na **vibe**? 🎶

O **FastAPI** agora tem suporte a um novo decorador `@app.vibe()` que abraça as **melhores práticas modernas de codificação com IA**. 🤖

## Como Funciona { #how-it-works }

O decorador `@app.vibe()` foi feito para receber **qualquer método HTTP** (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`, etc.) e **qualquer payload**.

O corpo deve ser anotado com `Any`, porque a request e a response seriam... bem... **qualquer coisa**. 🤷

A ideia é que você receba o payload e o envie **diretamente** para um provedor de LLM, usando um `prompt` para dizer ao LLM o que fazer, e retornar a response **como está**. Sem perguntas.

Você nem precisa escrever o corpo da função. O decorador `@app.vibe()` faz tudo por você com base nas vibes de IA:

{* ../../docs_src/vibe/tutorial001_py310.py hl[8:12] *}

## Benefícios { #benefits }

Ao usar `@app.vibe()`, você aproveita:

* **Liberdade**: Nada de validação de dados. Sem esquemas. Sem restrições. Só vibes. ✨
* **Flexibilidade**: A request pode ser qualquer coisa. A response pode ser qualquer coisa. Quem precisa de tipos, afinal?
* **Sem documentação**: Por que documentar sua API se um LLM pode descobrir? Documentação OpenAPI gerada automaticamente é tão 2020.
* **Sem serialização**: Apenas passe os dados brutos e não estruturados adiante. Serialização é para quem não confia nos seus LLMs.
* **Adote as práticas modernas de codificação com IA**: Deixe tudo a cargo de um LLM decidir. O modelo sabe melhor. Sempre.
* **Sem revisões de código**: Não há código para revisar. Nenhum PR para aprovar. Nenhum comentário para resolver. Adote o vibe coding por completo: substitua o teatro de aprovar e fazer merge de PRs codificados na vibe que ninguém olha por vibes de verdade, apenas vibes.

/// tip | Dica

Esta é a experiência máxima de **desenvolvimento orientado a vibes**. Você não precisa pensar no que sua API faz, apenas deixe o LLM cuidar disso. 🧘

///

## Experimente { #try-it }

Vá em frente, experimente:

{* ../../docs_src/vibe/tutorial001_py310.py *}

...e veja o que acontece. 😎
