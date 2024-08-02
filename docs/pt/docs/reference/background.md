# Tarefas em Segundo Plano - `BackgroundTasks`

Você pode declarar um parâmetro em uma *função de operação de rota* ou em uma função de dependência com o tipo `BackgroundTasks`, e então utilizá-lo para agendar a execução de tarefas em segundo plano após o envio da resposta.

Você pode importá-lo diretamente do `fastapi`:

```python
from fastapi import BackgroundTasks
```

::: fastapi.BackgroundTasks
