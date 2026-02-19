# Dépendances globales { #global-dependencies }

Pour certains types d'applications, vous pourriez vouloir ajouter des dépendances à l'application entière.

Comme vous pouvez [ajouter des `dependencies` aux *décorateurs de chemin d'accès*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, vous pouvez les ajouter à l'application `FastAPI`.

Dans ce cas, elles seront appliquées à tous les *chemins d'accès* de l'application :

{* ../../docs_src/dependencies/tutorial012_an_py310.py hl[17] *}

Et toutes les idées de la section sur [l'ajout de `dependencies` aux *décorateurs de chemin d'accès*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} s'appliquent toujours, mais dans ce cas à tous les *chemins d'accès* de l'application.

## Dépendances pour des groupes de *chemins d'accès* { #dependencies-for-groups-of-path-operations }

Plus tard, en lisant comment structurer des applications plus grandes ([Applications plus grandes - Plusieurs fichiers](../../tutorial/bigger-applications.md){.internal-link target=_blank}), éventuellement avec plusieurs fichiers, vous apprendrez comment déclarer un unique paramètre `dependencies` pour un groupe de *chemins d'accès*.
