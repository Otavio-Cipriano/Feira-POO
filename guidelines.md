# Guia de Arquitetura e Especificação Técnica

Projeto: Feira de Bairro (API REST sem banco de dados)

Este documento define os padrões arquiteturais e de negócio obrigatórios para garantir a máxima pontuação na avaliação de Programação Orientada a Objetos.

## 1. Guideline de arquitetura e regras da disciplina

A guideline estabelece as convenções de projeto, organização de camadas e restrições de implementação que devem ser seguidas em todo o trabalho.

### 1.1 Estrutura de pastas padrão

```text
feira-de-bairro/
├── main.py
├── requirements.txt
├── verificar.py
├── README.md
└── app/
    ├── __init__.py
    ├── data/          # Dados estáticos em listas de dicionários
    ├── models/        # Regras de negócio, OO, encapsulamento e exceções
    ├── controllers/   # Casos de uso e filtros, sem HTTP
    └── routes/        # Endpoints, status HTTP e tradução de erros
```

### 1.2 Regras de ouro

#### 1.2.1 Camada de modelos

- A camada `models` deve usar apenas Python puro.
- Não pode importar `FastAPI` em nenhum arquivo de `app/models/`.
- Exceções de domínio devem ser lançadas com `ValueError`.
- Validações de regra de negócio não devem retornar strings nem códigos HTTP.

#### 1.2.2 Polimorfismo e ausência de `if` por tipo

- É proibido usar `isinstance()`, `type()` ou verificações como `if tipo == "X"`.
- A variação de comportamento deve ser resolvida por polimorfismo.
- Cada subclasse deve definir suas constantes e sobrescrever os métodos necessários.

#### 1.2.3 Encapsulamento rígido

- Atributos privados/protegidos devem usar underscore, como `self._nome`.
- Métodos de leitura devem começar com `mostrar_`.
- Métodos de escrita devem começar com `alterar_`.
- Todas as validações devem ficar dentro dos métodos `alterar_*()`.
- Não é permitido criar `alterar_id()`.
- O construtor `__init__` deve invocar todos os métodos de alteração relevantes.

#### 1.2.4 Controllers

- A camada `controllers` deve retornar dados ou `None`.
- Não deve manipular respostas HTTP.
- Se um recurso não existir, deve retornar `None` ou `[]`.
- Não deve lançar exceções do FastAPI.

#### 1.2.5 Rotas e tratamento de erros

- `201 Created`: sucesso na criação de recursos.
- `200 OK`: leitura ou execução bem-sucedida.
- `404 Not Found`: recurso não encontrado.
- `409 Conflict` ou `422 Unprocessable Entity`: captura de `ValueError` originado na model.

## 2. Especificação do domínio — Feira de Bairro

### 2.1 Modelagem de entidades

Entidades principais:

- `Feirante`
- `Reserva`

Hierarquia exigida:

- `Barraca`
  - `BarracaAlimentacao`
    - `BarracaGourmet`

Associação:

- `Reserva` vincula um `Feirante` e uma `Barraca` em uma determinada data.

### 2.2 Regras do domínio

- Polimorfismo por constante de classe: cada subclasse define sua taxa diária base.
  - Exemplo: `Barraca = 50.0`, `BarracaAlimentacao = 80.0`, `BarracaGourmet = 120.0`
- `BarracaGourmet` deve usar `super().calcular_taxa_diaria()` para reaproveitar a lógica da classe pai e somar o adicional de infraestrutura.
- O `Feirante` possui limite máximo de 2 reservas ativas simultâneas, definido por constante de classe.
- Não é permitido registrar reservas duplicadas para a mesma barraca na mesma data.
- Validações obrigatórias:
  - CPF/CNPJ deve ter exatamente 11 ou 14 dígitos.
  - Metração da barraca deve ser maior que zero.
  - Data da reserva não pode ser string vazia ou inválida.

### 2.3 Mapeamento de rotas

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/barracas` | Lista o catálogo de barracas |
| `GET` | `/api/barracas/disponiveis` | Lista apenas barracas sem reserva |
| `GET` | `/api/barracas/{id}` | Detalhes de uma barraca (`200` ou `404`) |
| `POST` | `/api/reservas` | Cria uma nova reserva (`201`, `409` ou `422`) |
| `GET` | `/api/feirantes/{id}/reservas` | Consulta histórico de reservas do feirante (`200` ou `404`) |
| `GET` | `/api/relatorio/faturamento` | Retorna o faturamento total arrecadado |

## 3. Divisão do projeto por módulos

### Módulo 1 — Otávio

Responsável por:

1. Estrutura inicial do projeto.
2. Criação dos mocks em `app/data/`.
3. Implementação da classe `Feirante`.
4. Criação do arquivo `requirements.txt`.

### Módulo 2 — Nickolas

Responsável por:

1. Arquivo `app/models/barraca.py`.
2. Hierarquia de classes com polimorfismo.
3. Classe `Reserva` com validação de data.
4. Funções de carregamento dos mocks.

### Módulo 3 — Pedro

Responsável por:

1. `app/controllers/barraca_controller.py`
2. `app/controllers/feirante_controller.py`
3. `app/controllers/reserva_controller.py`
4. Lógica de filtragem, histórico e faturamento.

### Módulo 4 — Vinicius

Responsável por:

1. Rotas em `app/routes/`
2. `main.py`
3. `verificar.py`
4. `README.md` e documentação final

## 4. Regras de implementação esperadas

- A organização em módulos é obrigatória.
- O código deve ser orientado a objetos e seguir encapsulamento rigoroso.
- O padrão de negócio deve ser consistente em todas as camadas.
- O projeto deve funcionar sem banco de dados, usando apenas mocks em memória.
- A validação de regras de negócio deve acontecer na camada de modelos e ser convertida em exceções do domínio.

## 5. Checklist de entrega

- [ ] Estrutura de pastas criada corretamente
- [ ] Mocks com dados estáticos e sem lógica
- [ ] Modelos com encapsulamento e validações
- [ ] Controllers sem HTTP e sem tratamento de resposta
- [ ] Rotas com FastAPI e status HTTP adequados
- [ ] Script `verificar.py` com validações automatizadas
- [ ] README com instruções de execução e documentação de rotas

## 6. Observações finais

Este projeto foi concebido para praticar os conceitos fundamentais de POO, incluindo encapsulamento, herança, polimorfismo, regras de negócio e separação de responsabilidades. A aderência estrita a essas regras é parte essencial da avaliação.

