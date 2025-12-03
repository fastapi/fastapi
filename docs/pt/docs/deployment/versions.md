# Sobre as versões do FastAPI { #about-fastapi-versions }

**FastAPI** já está sendo usado em produção em muitas aplicações e sistemas. E a cobertura de testes é mantida em 100%. Mas seu desenvolvimento ainda está avançando rapidamente.

Novas funcionalidades são adicionadas com frequência, bugs são corrigidos regularmente e o código continua melhorando continuamente.

É por isso que as versões atuais ainda são `0.x.x`, isso reflete que cada versão pode potencialmente ter mudanças significativas. Isso segue as convenções de <a href="https://semver.org/" class="external-link" target="_blank">Versionamento Semântico</a>.

Você pode criar aplicações de produção com **FastAPI** agora mesmo (e provavelmente já vem fazendo isso há algum tempo), apenas certifique-se de usar uma versão que funcione corretamente com o resto do seu código.

## Fixe a sua versão de `fastapi` { #pin-your-fastapi-version }

A primeira coisa que você deve fazer é "fixar" a versão do **FastAPI** que você está utilizando na versão mais recente específica que você sabe que funciona corretamente para a sua aplicação.

Por exemplo, suponha que você esteja usando a versão `0.112.0` em sua aplicação.

Se você usa um arquivo `requirements.txt`, você poderia especificar a versão com:

```txt
fastapi[standard]==0.112.0
```

isso significaria que você usaria exatamente a versão `0.112.0`.

Ou você também poderia fixá-la com:

```txt
fastapi[standard]>=0.112.0,<0.113.0
```

isso significaria que você usaria as versões `0.112.0` ou superiores, mas menores que `0.113.0`, por exemplo, a versão `0.112.2` ainda seria aceita.

Se você usa qualquer outra ferramenta para gerenciar suas instalações, como `uv`, Poetry, Pipenv ou outras, todas elas têm uma forma de definir versões específicas para seus pacotes.

## Versões disponíveis { #available-versions }

Você pode ver as versões disponíveis (por exemplo, para verificar qual é a mais recente) nas [Release Notes](../release-notes.md){.internal-link target=_blank}.

## Sobre versões { #about-versions }

Seguindo as convenções de Versionamento Semântico, qualquer versão abaixo de `1.0.0` pode potencialmente adicionar mudanças significativas.

FastAPI também segue a convenção de que qualquer alteração de versão "PATCH" é para correções de bugs e mudanças que não quebram compatibilidade.

/// tip | Dica

O "PATCH" é o último número, por exemplo, em `0.2.3`, a versão PATCH é `3`.

///

Logo, você deveria conseguir fixar a versão, como:

```txt
fastapi>=0.45.0,<0.46.0
```

Mudanças significativas e novas funcionalidades são adicionadas em versões "MINOR".

/// tip | Dica

O "MINOR" é o número do meio, por exemplo, em `0.2.3`, a versão MINOR é `2`.

///

## Atualizando as versões do FastAPI { #upgrading-the-fastapi-versions }

Você deve adicionar testes para a sua aplicação.

Com **FastAPI** isso é muito fácil (graças ao Starlette), veja a documentação: [Testing](../tutorial/testing.md){.internal-link target=_blank}

Depois que você tiver testes, você pode atualizar a sua versão do **FastAPI** para uma mais recente e se certificar de que todo o seu código está funcionando corretamente executando seus testes.

Se tudo estiver funcionando, ou após você realizar as alterações necessárias e todos os testes estiverem passando, então você pode fixar sua versão de `fastapi` para essa versão mais recente.

## Sobre Starlette { #about-starlette }

Não é recomendado fixar a versão de `starlette`.

Versões diferentes de **FastAPI** utilizarão uma versão específica e mais recente de Starlette.

Então, você pode deixar **FastAPI** usar a versão correta do Starlette.

## Sobre Pydantic { #about-pydantic }

Pydantic inclui os testes para **FastAPI** em seus próprios testes, então novas versões do Pydantic (acima de `1.0.0`) são sempre compatíveis com FastAPI.

Você pode fixar o Pydantic em qualquer versão acima de `1.0.0` que funcione para você.

Por exemplo:

```txt
pydantic>=2.7.0,<3.0.0
```
