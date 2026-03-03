# Глобальні залежності { #global-dependencies }

Для деяких типів застосунків ви можете захотіти додати залежності до всього застосунку.

Подібно до того, як ви можете [додавати `dependencies` до *декораторів операцій шляху*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, ви можете додати їх до застосунку `FastAPI`.

У такому разі вони будуть застосовані до всіх *операцій шляху* в застосунку:

{* ../../docs_src/dependencies/tutorial012_an_py310.py hl[17] *}

Усі ідеї з розділу про [додавання `dependencies` до *декораторів операцій шляху*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} так само застосовні, але в цьому випадку - до всіх *операцій шляху* в застосунку.

## Залежності для груп *операцій шляху* { #dependencies-for-groups-of-path-operations }

Пізніше, читаючи про структуру більших застосунків ([Більші застосунки - кілька файлів](../../tutorial/bigger-applications.md){.internal-link target=_blank}), можливо з кількома файлами, ви дізнаєтеся, як оголосити єдиний параметр `dependencies` для групи *операцій шляху*.
