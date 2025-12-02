# Global Dependencies { #global-dependencies }

For some types of applications you might want to add dependencies to the whole application.

Similar to the way you can [add `dependencies` to the *path operation decorators*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, you can add them to the `FastAPI` application.

In that case, they will be applied to all the *path operations* in the application:

{* ../../docs_src/dependencies/tutorial012_an_py39.py hl[16] *}


And all the ideas in the section about [adding `dependencies` to the *path operation decorators*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} still apply, but in this case, to all of the *path operations* in the app.

## Dependencies for groups of *path operations* { #dependencies-for-groups-of-path-operations }

Later, when reading about how to structure bigger applications ([Bigger Applications - Multiple Files](../../tutorial/bigger-applications.md){.internal-link target=_blank}), possibly with multiple files, you will learn how to declare a single `dependencies` parameter for a group of *path operations*.
