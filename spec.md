# Especificação do Projeto — Feira de Bairro

Esta seção divide o projeto em 4 módulos independentes para garantir commits individuais por participante.

## Módulo 1 — Otávio (Data Mocks & Base Models)

Você é o  responsável por executar a parte 1 do projeto "Feira de Bairro".

#### Tarefas

1. Crie a estrutura de diretórios do projeto:
   - `app/`
   - `app/data/`
   - `app/models/`
   - `app/controllers/`
   - `app/routes/`

2. Crie os arquivos de dados estáticos na pasta `app/data/`:
   - `feirante_mock.py`: lista de dicionários com no mínimo 5 feirantes.
   - `barraca_mock.py`: lista de dicionários com no mínimo 5 barracas, variando tipos.
   - `reserva_mock.py`: lista de dicionários com no mínimo 5 reservas.
   - Nenhum arquivo na camada `data` pode conter classes, imports ou regras de negócio.

3. Crie a classe `Feirante` em `app/models/feirante.py`:
   - Encapsulamento completo com atributos privados: `_id`, `_nome`, `_documento`, `_telefone`.
   - Métodos `mostrar_*()` para leitura.
   - Métodos `alterar_*()` contendo validação, como documento com 11 ou 14 caracteres, disparando `ValueError`.
   - O construtor `__init__` deve chamar todos os métodos `alterar_*()`.
   - Proibido implementar `alterar_id()`.
   - Adicione a constante de classe `LIMITE_RESERVAS = 2`.
   - Implemente o método `__repr__`.
   - Crie a função `carregar_feirantes()` ao final do arquivo para instanciar a partir do mock.

4. Crie o arquivo `requirements.txt` contendo `fastapi` e `uvicorn`.

> Atenção: não importe `FastAPI` em nenhum arquivo dentro de `app/models/`.

---

## Módulo 2 — Nickolas (OO Advanced, Hierarquia & Polimorfismo)

Você é o responsável por executar a parte 2 do projeto "Feira de Bairro".

#### Tarefas

1. Crie o arquivo `app/models/barraca.py` com a seguinte hierarquia de 3 classes em 2 níveis:
   - Classe base: `Barraca`
     - Atributos: `_id`, `_codigo`, `_metragem`
     - Constante de classe: `TAXA_BASE = 50.0`
     - Método `calcular_taxa_diaria()` retornando `TAXA_BASE`
   - Classe filha nível 1: `BarracaAlimentacao` (herda de `Barraca`)
     - Constante de classe: `TAXA_BASE = 80.0`
     - Método `calcular_taxa_diaria()` adiciona taxa fixa de vigilância sanitária
   - Classe filha nível 2: `BarracaGourmet` (herda de `BarracaAlimentacao`)
     - Constante de classe: `TAXA_BASE = 120.0`
     - Método `calcular_taxa_diaria()` utiliza obrigatoriamente `super().calcular_taxa_diaria()` para estender o cálculo somando a taxa de energia/gás

2. Defina o dicionário `BARRACAS_TIPOS` mapeando as strings dos mocks para as classes correspondentes, sem utilizar condicionais `if`.

3. Crie a classe `Reserva` em `app/models/reserva.py`:
   - Atributos: `_id`, `_feirante` (objeto `Feirante`), `_barraca` (objeto `Barraca`), `_data`
   - Validação no método `alterar_data()` para evitar strings vazias.

4. Implemente `__repr__` e as funções `carregar_barracas()` e `carregar_reservas()` em seus arquivos correspondentes.

> Atenção: é terminantemente proibido utilizar `if tipo == ...` ou `isinstance()` para tratar as variações de classe.

---

## Módulo 3 — Pedro (Controllers & Business Logic Rules)

Você é  responsável por executar a parte 3 do projeto "Feira de Bairro".

#### Tarefas

1. Crie `app/controllers/barraca_controller.py`:
   - Função para listar todas as barracas.
   - Função para buscar barraca por ID.
   - Função para filtrar barracas disponíveis utilizando obrigatoriamente list comprehension.

2. Crie `app/controllers/feirante_controller.py`:
   - Função para listar feirantes e buscar por ID.
   - Função para obter o histórico de reservas de um feirante específico.

3. Crie `app/controllers/reserva_controller.py`:
   - Função para registrar reserva: deve verificar se a barraca já está reservada na data e se o feirante atingiu a constante `LIMITE_RESERVAS`. Se violado, disparar `ValueError`.
   - Função para calcular o faturamento total somando a taxa diária de todas as reservas ativas.

4. Garanta que cada controller possua o método utilitário `_para_dicionario()` para conversão de objetos.

> Atenção: os controllers devem retornar dados ou listas, ou `None`. NUNCA utilize status HTTP nem lance exceções do FastAPI nesta camada.

---

## Módulo 4 — Vinicius (Routes, Main, Verification Script & README)

Você é o responsável por executar a parte 4 do projeto "Feira de Bairro".

#### Tarefas

1. Crie os arquivos de rotas em `app/routes/`:
   - `barraca_routes.py`
   - `feirante_routes.py`
   - `reserva_routes.py`
   - `relatorio_routes.py`

2. Mapeie todas as rotas com FastAPI tratando os códigos de retorno HTTP:
   - `200 OK` para consultas realizadas.
   - `201 Created` para criação de reservas com sucesso.
   - `404 Not Found` quando controllers retornarem `None`.
   - Bloco `try/except ValueError` convertendo exceções de negócio da model para `409 Conflict` ou `422 Unprocessable Entity`.

3. Crie o arquivo `main.py` inicializando a aplicação FastAPI e incluindo os roteadores.

4. Crie o arquivo `verificar.py` contendo no mínimo 12 validações automáticas da estrutura do projeto e das regras de negócio.

5. Crie o `README.md` com:
   - instruções de execução (`uvicorn main:app --reload`)
   - tabela descritiva de rotas e status HTTP
   - diagrama de classes em formato Mermaid
   - tabela com a divisão de tarefas dos integrantes
