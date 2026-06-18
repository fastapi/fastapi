import http

from fastapi import FastAPI, Path, Query

external_docs = {
    "description": "External API documentation.",
    "url": "https://docs.example.com/api-general",
}

app = FastAPI(openapi_external_docs=external_docs)


@app.api_route("/api_route")
def non_operation():
    return {"message": "Hello World"}


def non_decorated_route():
    return {"message": "Hello World"}


app.add_api_route("/non_decorated_route", non_decorated_route)


@app.get("/text")
def get_text():
    return "Hello World"


@app.get("/path/{item_id}")
def get_id(item_id):
    return item_id


@app.get("/path/str/{item_id}")
def get_str_id(item_id: str):
    return item_id


@app.get("/path/int/{item_id}")
def get_int_id(item_id: int):
    return item_id


@app.get("/path/float/{item_id}")
def get_float_id(item_id: float):
    return item_id


@app.get("/path/bool/{item_id}")
def get_bool_id(item_id: bool):
    return item_id


@app.get("/path/param/{item_id}")
def get_path_param_id(item_id: str | None = Path()):
    return item_id


@app.get("/path/param-minlength/{item_id}")
def get_path_param_min_length(item_id: str = Path(min_length=3)):
    return item_id


@app.get("/path/param-maxlength/{item_id}")
def get_path_param_max_length(item_id: str = Path(max_length=3)):
    return item_id


@app.get("/path/param-min_maxlength/{item_id}")
def get_path_param_min_max_length(item_id: str = Path(max_length=3, min_length=2)):
    return item_id


@app.get("/path/param-gt/{item_id}")
def get_path_param_gt(item_id: float = Path(gt=3)):
    return item_id


@app.get("/path/param-gt0/{item_id}")
def get_path_param_gt0(item_id: float = Path(gt=0)):
    return item_id


@app.get("/path/param-ge/{item_id}")
def get_path_param_ge(item_id: float = Path(ge=3)):
    return item_id


@app.get("/path/param-lt/{item_id}")
def get_path_param_lt(item_id: float = Path(lt=3)):
    return item_id


@app.get("/path/param-lt0/{item_id}")
def get_path_param_lt0(item_id: float = Path(lt=0)):
    return item_id


@app.get("/path/param-le/{item_id}")
def get_path_param_le(item_id: float = Path(le=3)):
    return item_id


@app.get("/path/param-lt-gt/{item_id}")
def get_path_param_lt_gt(item_id: float = Path(lt=3, gt=1)):
    return item_id


@app.get("/path/param-le-ge/{item_id}")
def get_path_param_le_ge(item_id: float = Path(le=3, ge=1)):
    return item_id


@app.get("/path/param-lt-int/{item_id}")
def get_path_param_lt_int(item_id: int = Path(lt=3)):
    return item_id


@app.get("/path/param-gt-int/{item_id}")
def get_path_param_gt_int(item_id: int = Path(gt=3)):
    return item_id


@app.get("/path/param-le-int/{item_id}")
def get_path_param_le_int(item_id: int = Path(le=3)):
    return item_id


@app.get("/path/param-ge-int/{item_id}")
def get_path_param_ge_int(item_id: int = Path(ge=3)):
    return item_id


@app.get("/path/param-lt-gt-int/{item_id}")
def get_path_param_lt_gt_int(item_id: int = Path(lt=3, gt=1)):
    return item_id


@app.get("/path/param-le-ge-int/{item_id}")
def get_path_param_le_ge_int(item_id: int = Path(le=3, ge=1)):
    return item_id


@app.get("/query")
def get_query(query):
    return f"foo bar {query}"


@app.get("/query/optional")
def get_query_optional(query=None):
    if query is None:
        return "foo bar"
    return f"foo bar {query}"


@app.get("/query/int")
def get_query_type(query: int):
    return f"foo bar {query}"


@app.get("/query/int/optional")
def get_query_type_optional(query: int | None = None):
    if query is None:
        return "foo bar"
    return f"foo bar {query}"


@app.get("/query/int/default")
def get_query_type_int_default(query: int = 10):
    return f"foo bar {query}"


@app.get("/query/param")
def get_query_param(query=Query(default=None)):
    if query is None:
        return "foo bar"
    return f"foo bar {query}"


@app.get("/query/param-required")
def get_query_param_required(query=Query()):
    return f"foo bar {query}"


@app.get("/query/param-required/int")
def get_query_param_required_type(query: int = Query()):
    return f"foo bar {query}"


@app.get("/enum-status-code", status_code=http.HTTPStatus.CREATED)
def get_enum_status_code():
    return "foo bar"


@app.get("/query/frozenset")
def get_query_type_frozenset(query: frozenset[int] = Query(...)):
    return ",".join(map(str, sorted(query)))


@app.get("/query/list")
def get_query_list(device_ids: list[int] = Query()) -> list[int]:
    return device_ids


@app.get("/query/list-default")
def get_query_list_default(device_ids: list[int] = Query(default=[])) -> list[int]:
    return device_ids
class TipoUsuario(str, Enum):
    ALUNO = "aluno"
    PROFESSOR = "professor"

class Materia(str, Enum):
    MATEMATICA = "matematica"
    FISICA = "fisica"
    ADMINISTRACAO = "administracao"
    ROBOTICA = "robotica"
    PORTUGUES = "portugues"
    INGLES = "ingles"
    ESPANHOL = "espanhol"
    HISTORIA = "historia"
    REDACAO = "redacao"

class Usuario(BaseModel):
    id: int
    nome: str
    tipo: TipoUsuario
    nivel: int = 1 # Relevante para o aluno

class AtividadeDiagnostica(BaseModel):
    id: int
    materia: Materia
    pergunta: str
    opcoes: List[str]
    resposta_correta: str
    criado_por_professor_id: int


import random

class SlimeIA:
    def __init__(self, nome_mascote: str = "Gloop"):
        self.nome = nome_mascote

    def gerar_resposta_adaptativa(self, aluno: Usuario, materia: Materia, duvida: str) -> dict:
        """
        Simula a engine de IA que adapta o conhecimento ao nível do aluno.
        Em produção, aqui haveria uma chamada para a API da OpenAI/Anthropic com um prompt de sistema.
        """
        # Adaptação de tom baseada no nível/idade simulada
        if aluno.nivel < 5:
            tom = "super simples, lúdico e com metáforas visuais"
            expressao_slime = "✨ Slime Brilhante e Feliz! ✨"
        else:
            tom = "focado, dinâmico e contextualizado para jovens"
            expressao_slime = "🧠 Slime Cientista! 🧠"

        # Resposta simulada da IA
        resposta_base = f"Olá {aluno.nome}! Eu sou o {self.nome}. Vi que sua dúvida em {materia.value} é: '{duvida}'."
       
        return {
            "mascote_expressao": expressao_slime,
            "resposta_ia": f"{resposta_base} Explicando de forma {tom}: Vamos resolver isso juntos passo a passo!",
            "sugestao_proximo_passo": f"Que tal fazermos uma atividade de {materia.value} agora?"
        }


import random

class SlimeIA:
    def __init__(self, nome_mascote: str = "Gloop"):
        self.nome = nome_mascote

    def gerar_resposta_adaptativa(self, aluno: Usuario, materia: Materia, duvida: str) -> dict:
        """
        Simula a engine de IA que adapta o conhecimento ao nível do aluno.
        Em produção, aqui haveria uma chamada para a API da OpenAI/Anthropic com um prompt de sistema.
        """
        # Adaptação de tom baseada no nível/idade simulada
        if aluno.nivel < 5:
            tom = "super simples, lúdico e com metáforas visuais"
            expressao_slime = "✨ Slime Brilhante e Feliz! ✨"
        else:
            tom = "focado, dinâmico e contextualizado para jovens"
            expressao_slime = "🧠 Slime Cientista! 🧠"

        # Resposta simulada da IA
        resposta_base = f"Olá {aluno.nome}! Eu sou o {self.nome}. Vi que sua dúvida em {materia.value} é: '{duvida}'."
       
        return {
            "mascote_expressao": expressao_slime,
            "resposta_ia": f"{resposta_base} Explicando de forma {tom}: Vamos resolver isso juntos passo a passo!",
            "sugestao_proximo_passo": f"Que tal fazermos uma atividade de {materia.value} agora?"
        }


from fastapi import FastAPI, HTTPException

app = FastAPI(title="SlimyEdu API", version="1.0")
slime_brain = SlimeIA()

# Banco de dados temporário (em memória)
banco_atividades = []
banco_usuarios = [
    Usuario(id=1, nome= "Lucas", tipo=TipoUsuario.ALUNO, nivel=3),
    Usuario(id=2, nome="Profª Marina", tipo=TipoUsuario.PROFESSOR)
]

@app.post("/atividades/inserir", tags=["Professor"])
def professor_insere_atividade(atividade: AtividadeDiagnostica):
    # Verifica se quem está inserindo é realmente um professor
    professor = next((u for u in banco_usuarios if u.id == atividade.criado_por_professor_id), None)
    if not professor or professor.tipo != TipoUsuario.PROFESSOR:
        raise HTTPException(status_code=403, detail="Apenas professores podem inserir conteúdos.")
   
    banco_atividades.append(atividade)
    return {"status": "Sucesso", "mensagem": f"Atividade de {atividade.materia} inserida com sucesso!"}

@app.get("/slime/perguntar", tags=["Aluno / IA"])
def perguntar_para_slime(aluno_id: int, materia: Materia, duvida: str):
    # Busca o aluno
    aluno = next((u for u in banco_usuarios if u.id == aluno_id), None)
    if not aluno or aluno.tipo != TipoUsuario.ALUNO:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
   
    # Gera a resposta personalizada da IA da Slime
    resposta_slime = slime_brain.gerar_resposta_adaptativa(aluno, materia, duvida)
    return resposta_slime

@app.get("/atividades/diagnostica/{materia}", tags=["Aluno / IA"])
def obter_atividades_por_materia(materia: Materia):
    # Filtra as atividades que os professores cadastraram para o aluno responder
    atividades_filtradas = [a for a in banco_atividades if a.materia == materia]
    return {"atividades": atividades_filtradas}
