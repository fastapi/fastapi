# Transmitir dados { #stream-data }

Se você quer transmitir dados que podem ser estruturados como JSON, você deveria [Transmitir JSON Lines](../tutorial/stream-json-lines.md).

Mas se você quer transmitir dados binários puros ou strings, veja como fazer.

/// info | Informação

Adicionado no FastAPI 0.134.0.

///

## Casos de uso { #use-cases }

Você pode usar isto para transmitir strings puras, por exemplo diretamente da saída de um serviço de AI LLM.

Você também pode usá-lo para transmitir arquivos binários grandes, enviando cada bloco de dados à medida que o lê, sem precisar carregar tudo na memória de uma vez.

Você também pode transmitir vídeo ou áudio desta forma; pode até ser gerado enquanto você processa e envia.

## Um `StreamingResponse` com `yield` { #a-streamingresponse-with-yield }

Se você declarar `response_class=StreamingResponse` na sua função de operação de rota, você pode usar `yield` para enviar cada bloco de dados em sequência.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[1:23] hl[20,23] *}

O FastAPI entregará cada bloco de dados para `StreamingResponse` como está, não tentará convertê-lo para JSON nem nada semelhante.

### Funções de operação de rota não assíncronas { #non-async-path-operation-functions }

Você também pode usar funções `def` normais (sem `async`) e usar `yield` da mesma forma.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[26:29] hl[27] *}

### Sem anotação { #no-annotation }

Você não precisa declarar a anotação de tipo de retorno para transmitir dados binários.

Como o FastAPI não tentará converter os dados para JSON com Pydantic nem serializá-los de nenhuma forma, neste caso a anotação de tipo serve apenas para seu editor e ferramentas; ela não será usada pelo FastAPI.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[32:35] hl[33] *}

Isso também significa que, com `StreamingResponse`, você tem a liberdade e a responsabilidade de produzir e codificar os bytes exatamente como precisam ser enviados, independentemente das anotações de tipo. 🤓

### Transmitir bytes { #stream-bytes }

Um dos principais casos de uso é transmitir `bytes` em vez de strings; você pode fazer isso sem problemas.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[44:47] hl[47] *}

## Um `PNGStreamingResponse` personalizado { #a-custom-pngstreamingresponse }

Nos exemplos acima, os bytes eram transmitidos, mas a resposta não tinha um cabeçalho `Content-Type`, então o cliente não sabia que tipo de dado estava recebendo.

Você pode criar uma subclasse personalizada de `StreamingResponse` que define o cabeçalho `Content-Type` para o tipo de dado que você está transmitindo.

Por exemplo, você pode criar um `PNGStreamingResponse` que define o cabeçalho `Content-Type` como `image/png` usando o atributo `media_type`:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[6,19:20] hl[20] *}

Em seguida, você pode usar essa nova classe em `response_class=PNGStreamingResponse` na sua função de operação de rota:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[23:27] hl[23] *}

### Simular um arquivo { #simulate-a-file }

Neste exemplo, estamos simulando um arquivo com `io.BytesIO`, que é um objeto semelhante a arquivo que vive somente na memória, mas nos permite usar a mesma interface.

Por exemplo, podemos iterar sobre ele para consumir seu conteúdo, como faríamos com um arquivo.

{* ../../docs_src/stream_data/tutorial002_py310.py ln[1:27] hl[3,12:13,25] *}

/// note | Detalhes Técnicos

As outras duas variáveis, `image_base64` e `binary_image`, são uma imagem codificada em Base64 e depois convertida para bytes, para então passá-la para `io.BytesIO`.

Apenas para que possa viver no mesmo arquivo deste exemplo e você possa copiar e executar como está. 🥚

///

Ao usar um bloco `with`, garantimos que o objeto semelhante a arquivo seja fechado após a função geradora (a função com `yield`) terminar. Ou seja, após terminar de enviar a resposta.

Isso não seria tão importante neste exemplo específico porque é um arquivo falso em memória (com `io.BytesIO`), mas com um arquivo real, seria importante garantir que o arquivo fosse fechado ao final do trabalho.

### Arquivos e async { #files-and-async }

Na maioria dos casos, objetos semelhantes a arquivo não são compatíveis com async e await por padrão.

Por exemplo, eles não têm `await file.read()`, nem `async for chunk in file`.

E, em muitos casos, lê-los seria uma operação bloqueante (que poderia bloquear o loop de eventos), pois são lidos do disco ou da rede.

/// info | Informação

O exemplo acima é, na verdade, uma exceção, porque o objeto `io.BytesIO` já está em memória, então lê-lo não bloqueará nada.

Mas, em muitos casos, ler um arquivo ou um objeto semelhante a arquivo bloquearia.

///

Para evitar bloquear o loop de eventos, você pode simplesmente declarar a função de operação de rota com `def` normal em vez de `async def`. Assim, o FastAPI a executará em um worker de threadpool, evitando bloquear o loop principal.

{* ../../docs_src/stream_data/tutorial002_py310.py ln[30:34] hl[31] *}

/// tip | Dica

Se você precisar chamar código bloqueante de dentro de uma função assíncrona ou uma função assíncrona de dentro de uma função bloqueante, você poderia usar o [Asyncer](https://asyncer.tiangolo.com), uma biblioteca irmã do FastAPI.

///

### `yield from` { #yield-from }

Quando você está iterando sobre algo, como um objeto semelhante a arquivo, e faz `yield` para cada item, você também pode usar `yield from` para produzir cada item diretamente e pular o loop `for`.

Isso não é particular do FastAPI, é apenas Python, mas é um truque útil para conhecer. 😎

{* ../../docs_src/stream_data/tutorial002_py310.py ln[37:40] hl[40] *}
