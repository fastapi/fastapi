# Testando Dependências com Sobreposições { #testing-dependencies-with-overrides }

## Sobrepondo dependências durante os testes { #overriding-dependencies-during-testing }

Existem alguns cenários onde você deseje sobrepor uma dependência durante os testes.

Você não quer que a dependência original execute (e nenhuma das subdependências que você possa ter).

Em vez disso, você deseja fornecer uma dependência diferente que será usada somente durante os testes (possivelmente apenas para alguns testes específicos) e fornecerá um valor que pode ser usado onde o valor da dependência original foi usado.

### Casos de uso: serviço externo { #use-cases-external-service }

Um exemplo pode ser que você possua um provedor de autenticação externo que você precisa chamar.

Você envia ao serviço um *token* e ele retorna um usuário autenticado.

Este provedor pode cobrar por requisição, e chamá-lo pode levar mais tempo do que se você tivesse um usuário fixo para os testes.

Você provavelmente quer testar o provedor externo uma vez, mas não necessariamente chamá-lo em todos os testes que executarem.

Neste caso, você pode sobrepor (*override*) a dependência que chama o provedor, e utilizar uma dependência customizada que retorna um *mock* do usuário, apenas para os seus testes.

### Utilize o atributo `app.dependency_overrides` { #use-the-app-dependency-overrides-attribute }

Para estes casos, a sua aplicação **FastAPI** possui o atributo `app.dependency_overrides`. Ele é um simples `dict`.

Para sobrepor a dependência para os testes, você coloca como chave a dependência original (a função), e como valor, a sua sobreposição da dependência (outra função).

E então o **FastAPI** chamará a sobreposição no lugar da dependência original.

{* ../../docs_src/dependency_testing/tutorial001_an_py310.py hl[26:27,30] *}

/// tip | Dica

Você pode definir uma sobreposição de dependência para uma dependência que é utilizada em qualquer lugar da sua aplicação **FastAPI**.

A dependência original pode estar sendo utilizada em uma *função de operação de rota*, um *decorador de operação de rota* (quando você não utiliza o valor retornado), uma chamada ao `.include_router()`, etc.

O FastAPI ainda poderá sobrescrevê-lo.

///

E então você pode redefinir as suas sobreposições (removê-las) definindo o `app.dependency_overrides` como um `dict` vazio:

```Python
app.dependency_overrides = {}
```

/// tip | Dica

Se você quer sobrepor uma dependência apenas para alguns testes, você pode definir a sobreposição no início do teste (dentro da função de teste) e reiniciá-la ao final (no final da função de teste).

///
