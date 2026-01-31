# Глобальні залежності { #global-dependencies }

Для деяких типів застосунків ви можете захотіти додати залежності для всього застосунку.

Подібно до того, як ви можете [додати `dependencies` до *декораторів операцій шляху*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, ви можете додати їх і до застосунку `FastAPI`.

У такому разі вони будуть застосовані до всіх *операцій шляху* в застосунку:

{* ../../docs_src/dependencies/tutorial012_an_py39.py hl[17] *}


І всі ідеї з розділу про [додавання `dependencies` до *декораторів операцій шляху*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} усе ще застосовні, але в цьому випадку — до всіх *операцій шляху* в застосунку.

## Залежності для груп *операцій шляху* { #dependencies-for-groups-of-path-operations }

Пізніше, читаючи про те, як структурувати більші застосунки ([Більші застосунки — кілька файлів](../../tutorial/bigger-applications.md){.internal-link target=_blank}), можливо з кількома файлами, ви дізнаєтеся, як оголосити один параметр `dependencies` для групи *операцій шляху*.
