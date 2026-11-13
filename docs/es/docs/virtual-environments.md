# Entornos Virtuales { #virtual-environments }

Cuando trabajas con proyectos de Python, deberías usar un **entorno virtual** para aislar los paquetes instalados para cada proyecto.

Para proyectos de FastAPI, recomiendo usar [uv](https://docs.astral.sh/uv/) para gestionar el proyecto, sus dependencias y su entorno virtual.

## Crea un Proyecto { #create-a-project }

Instala `uv` usando la [guía oficial de instalación](https://docs.astral.sh/uv/getting-started/installation/), y luego crea un proyecto:

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"
```

</div>

`uv` crea un entorno virtual para el proyecto automáticamente. No necesitas crear ni activar uno tú mismo.

Ejecuta comandos dentro del entorno del proyecto con `uv run`, por ejemplo:

<div class="termy">

```console
$ uv run fastapi dev
```

</div>

## Aprende Más { #learn-more }

Lee la [guía de Entornos Virtuales](https://tiangolo.com/guides/virtual-environments/) para aprender cómo funcionan los entornos virtuales por debajo, incluyendo la activación y el flujo de trabajo alternativo con `python -m venv` y `pip`.
