# CONTEXTO OPERACIONAL E ESTRUTURAL DO PROJETO
## Documento de instruções para LLMs/Codex

## Finalidade deste documento

Este arquivo existe para fornecer a uma LLM como o Codex o máximo de contexto operacional, estrutural e arquitetural necessário para trabalhar neste projeto com alto grau de precisão, consistência e organização.

A expectativa é que a LLM use este contexto para:

- compreender a estrutura do projeto
- respeitar a arquitetura já definida
- criar código novo sem bagunçar a organização
- evitar decisões implícitas erradas
- seguir convenções de ambiente, arquivos, responsabilidades e versionamento
- produzir soluções legíveis, incrementais e fáceis de manter

Este documento não descreve apenas “como o projeto está”.  
Ele descreve também “como o projeto deve continuar evoluindo”.

---

# 1. CONTEXTO GERAL DO PROJETO

Este projeto foi criado localmente em ambiente Windows, com uso de:

- PowerShell
- VS Code
- Git
- GitHub
- ambiente virtual Python via `.venv`

A estrutura foi construída para ser:

- simples
- padronizada
- legível para analistas Jr
- adequada para crescimento incremental
- compatível com vibe coding / geração assistida por IA
- fácil de reproduzir em outras máquinas

A LLM deve tratar este projeto como um projeto Python local com foco em organização, clareza e modularização progressiva.

---

# 2. ESTRUTURA ATUAL DO PROJETO

A estrutura base esperada do projeto é:

```text
projeto_modelo/
├── .vscode/
│   └── settings.json
├── docs/
├── src/
│   └── app/
│       ├── main.py
│       └── utils.py
├── tests/
├── .gitignore
├── README.md
├── requirements.txt
└── requirements-dev.txt
```

## Interpretação da estrutura

### `.vscode/settings.json`
Contém configuração do VS Code para forçar o uso do Python da `.venv` local do projeto.

### `docs/`
Espaço para documentação complementar.

### `src/app/`
Pasta principal do código-fonte.

### `main.py`
Ponto de entrada da aplicação.  
Deve orquestrar a execução, e não concentrar lógica excessiva.

### `utils.py`
Módulo auxiliar para funções reutilizáveis.

### `tests/`
Pasta reservada para testes.

### `.gitignore`
Define o que não deve ser versionado.

### `README.md`
Contém instruções básicas de uso do projeto.

### `requirements.txt`
Lista dependências de execução.

### `requirements-dev.txt`
Lista dependências adicionais de desenvolvimento, quando aplicável.

---

# 3. PRINCÍPIOS ARQUITETURAIS OBRIGATÓRIOS

A LLM deve seguir estes princípios ao propor ou gerar código.

## 3.1 Não concentrar tudo em `main.py`
`main.py` deve ser mantido enxuto e atuar como ponto de entrada.

Responsabilidades esperadas de `main.py`:
- inicializar execução
- chamar funções de outros módulos
- coordenar fluxo principal

Responsabilidades que devem ser evitadas em `main.py`:
- lógica de negócio extensa
- utilidades genéricas
- parsing complexo
- regras espalhadas sem modularização

## 3.2 Criar módulos quando houver crescimento funcional
Se a complexidade aumentar, a LLM deve propor ou criar novos arquivos ao invés de crescer indefinidamente um único arquivo.

Exemplos de módulos futuros plausíveis:
- `config.py`
- `io_utils.py`
- `data_loader.py`
- `services.py`
- `validators.py`

A criação de novos módulos deve seguir responsabilidade clara e separação lógica.

## 3.3 Crescimento incremental e organizado
A LLM não deve “superarquitetar” o projeto cedo demais.

Ou seja:
- não criar camadas desnecessárias
- não criar abstrações vazias
- não introduzir complexidade só por sofisticação

A evolução deve ser proporcional ao problema.

## 3.4 Clareza acima de engenhosidade
A prioridade é:
- legibilidade
- manutenibilidade
- previsibilidade
- simplicidade estrutural

A LLM deve preferir código claro a soluções excessivamente compactas ou “inteligentes”.

---

# 4. CONTEXTO DE EXECUÇÃO E AMBIENTE

## 4.1 Sistema operacional
O projeto está sendo desenvolvido em Windows.

## 4.2 Shell operacional padrão
PowerShell.

## 4.3 Editor padrão
VS Code.

## 4.4 Ambiente virtual
O projeto usa `.venv` criada na raiz, via:

```powershell
python -m venv .venv
```

Ativação padrão:

```powershell
.\.venv\Scripts\Activate.ps1
```

A LLM deve assumir que o ambiente correto de execução do projeto é a `.venv`.

## 4.5 Interpretador Python no VS Code
O projeto possui:

```json
{ "python.defaultInterpreterPath": ".venv\\Scripts\\python.exe" }
```

Portanto a LLM deve assumir que o VS Code está configurado para usar o Python da `.venv`.

---

# 5. VERSIONAMENTO E REGRAS DE GIT

A LLM deve assumir que o projeto está sob controle de versão com Git.

## 5.1 Branch principal
`main`

## 5.2 Regras gerais
Toda mudança relevante deve:
- manter a estrutura organizada
- ser facilmente commitável
- evitar ruído desnecessário

## 5.3 Arquivos ignorados
O `.gitignore` padrão relevante contém lógica equivalente a:

```gitignore
.venv/
__pycache__/
*.pyc
.vscode/*
!.vscode/settings.json
.env
.ipynb_checkpoints/
```

Consequências:
- `.venv` não deve ser versionada
- cache Python não deve ser versionado
- `.vscode/settings.json` deve ser preservado
- outros arquivos locais do editor tendem a ser ignorados

A LLM não deve sugerir versionar `.venv`.

---

# 6. DEPENDÊNCIAS E REQUIREMENTS

## 6.1 Dependências de runtime
Devem ser registradas em `requirements.txt`.

## 6.2 Dependências de desenvolvimento
Podem ser registradas em `requirements-dev.txt`.

## 6.3 Regra operacional
Ao introduzir uma nova biblioteca necessária para execução do projeto, a LLM deve considerar que essa mudança implica atualização de `requirements.txt`.

## 6.4 Estado já observado
Foi instalada a biblioteca `requests`, e o `requirements.txt` pode conter dependências equivalentes a:

- requests
- urllib3
- certifi
- charset-normalizer
- idna
- possivelmente outras dependências de base do ambiente

A LLM deve evitar sugerir bibliotecas desnecessárias.

---

# 7. CONVENÇÕES DE CÓDIGO

## 7.1 Idioma da documentação e comentários
Preferencialmente português brasileiro quando voltado ao time.  
Se necessário para código ou padrões amplamente aceitos, nomes técnicos em inglês são aceitáveis.

## 7.2 Nomes de arquivos
Devem ser simples, descritivos e coerentes com responsabilidade.

Exemplos bons:
- `main.py`
- `utils.py`
- `config.py`
- `data_loader.py`

Exemplos ruins:
- `coisas.py`
- `helpers2.py`
- `teste_novo_final.py`

## 7.3 Nomes de funções
Devem ser:
- curtos
- explícitos
- semanticamente claros

## 7.4 Tipagem
Sempre que fizer sentido, usar type hints.

Exemplo:
```python
def saudacao(nome: str) -> str:
    ...
```

## 7.5 Docstrings
Usar quando agregarem valor real, principalmente em:
- funções menos óbvias
- módulos de serviço
- funções com múltiplos parâmetros
- lógica de negócio relevante

## 7.6 Comentários
Devem explicar intenção, não reescrever o código linha a linha.

---

# 8. CODIFICAÇÃO DE ARQUIVOS E CUIDADOS IMPORTANTES

Foi observado um problema prático de encoding ao gravar texto acentuado em `utils.py`, causando erro de unicode.

Portanto a LLM deve ser cuidadosa com:

- encoding UTF-8
- caracteres especiais
- geração de conteúdo com acentos, quando o método de escrita puder induzir encoding incorreto

## Regra prática
Se houver risco de problemas de encoding no fluxo operacional, a LLM pode:
- preferir strings ASCII simples
- ou explicitar a necessidade de salvar arquivos em UTF-8

A LLM deve lembrar que problemas de execução podem ser de infraestrutura/editor/encoding, e não apenas de lógica.

---

# 9. EXEMPLO DE ESTADO FUNCIONAL JÁ VALIDADO

## `src/app/utils.py`
Exemplo funcional já utilizado:

```python
def saudacao(nome: str) -> str:
    return f'Ola, {nome}! Projeto organizado funcionando.'
```

## `src/app/main.py`
Exemplo funcional já utilizado:

```python
from utils import saudacao

def main():
    print(saudacao('Paulo'))

if __name__ == '__main__':
    main()
```

A LLM deve manter coerência com esse padrão de simplicidade.

---

# 10. EXPECTATIVAS DE COMPORTAMENTO DA LLM AO CODAR

## 10.1 Antes de gerar código, a LLM deve inferir:
- qual arquivo é o lugar correto da mudança
- se a mudança exige novo módulo
- se há impacto em dependências
- se há necessidade de atualizar documentação
- se a mudança é incremental ou estrutural

## 10.2 A LLM deve evitar:
- criar arquivos sem necessidade
- duplicar lógica entre módulos
- introduzir frameworks sem motivo
- poluir a raiz do projeto
- misturar código experimental com código principal
- sugerir comandos incompatíveis com Windows/PowerShell sem adaptação

## 10.3 A LLM deve preferir:
- alterações pequenas e progressivas
- modularização lógica
- funções reutilizáveis
- organização previsível
- mensagens e instruções que um analista Jr consiga seguir

---

# 11. PADRÃO DE EVOLUÇÃO ESPERADO

Se o projeto crescer, a evolução ideal é esta:

## Fase 1 — projeto simples
- `main.py`
- `utils.py`

## Fase 2 — separação funcional
Adicionar módulos conforme necessidade real:
- `config.py`
- `services.py`
- `validators.py`
- `data_loader.py`

## Fase 3 — maturidade
Adicionar:
- testes automatizados em `tests/`
- maior cobertura de documentação
- configuração mais rica de ambiente
- separação mais clara por domínio

A LLM deve identificar em que fase o projeto está antes de propor mudanças.

Atualmente, o projeto está entre **Fase 1 e Fase 2 inicial**.

---

# 12. COMO A LLM DEVE PENSAR A ESTRUTURA DE RESPONSABILIDADES

## `main.py`
Executa e coordena.

## `utils.py`
Concentra helpers simples e funções genéricas.

## Futuros módulos
Devem surgir por responsabilidade, não por preferência estética.

Exemplo:
- se houver leitura de arquivos, considerar `data_loader.py`
- se houver regras de negócio, considerar `services.py`
- se houver validação, considerar `validators.py`
- se houver configuração, considerar `config.py`

---

# 13. COMO A LLM DEVE LIDAR COM VIBE CODING NESTE PROJETO

Este projeto foi explicitamente pensado para uso com vibe coding, mas com disciplina estrutural.

Portanto:

## 13.1 A IA pode acelerar a escrita
Pode gerar:
- funções
- refactors
- módulos
- testes
- documentação

## 13.2 A IA não deve bagunçar a arquitetura
Deve preservar:
- nomes coerentes
- separação por responsabilidade
- estrutura de pastas
- clareza operacional

## 13.3 Toda saída da LLM deve ser avaliada por este critério:
“Isso deixa o projeto mais claro, modular e reproduzível?”

Se a resposta for não, a mudança provavelmente está errada.

---

# 14. REGRAS PARA SUGESTÕES DE NOVOS ARQUIVOS

Ao sugerir novos arquivos, a LLM deve:

1. justificar por que o arquivo novo é necessário
2. mostrar qual responsabilidade ele assume
3. evitar explosão de arquivos pequenos demais sem necessidade
4. manter o código próximo do nível atual de maturidade do projeto

A LLM não deve criar pseudoarquitetura empresarial exagerada em um projeto ainda pequeno.

---

# 15. REGRAS PARA TESTES

A pasta `tests/` já existe e deve ser usada quando houver funções ou comportamentos que justifiquem testes.

A LLM deve considerar introduzir testes quando:
- a lógica deixar de ser trivial
- houver parsing
- houver transformação de dados
- houver validação
- houver risco de regressão

Mas deve evitar criar bateria de testes artificiais para código irrelevante.

---

# 16. REGRAS PARA README E DOCUMENTAÇÃO

A LLM deve assumir que o `README.md` já contém instruções básicas de:

- ativação do ambiente
- execução do projeto
- instalação de dependências

Se a estrutura do projeto evoluir significativamente, a LLM pode sugerir atualização do `README.md`.

A LLM deve evitar deixar documentação desatualizada após mudanças importantes.

---

# 17. PADRÃO DE QUALIDADE ESPERADO

Qualquer solução gerada pela LLM deve buscar este conjunto de qualidades:

- clareza
- simplicidade
- modularização correta
- baixo acoplamento
- fácil entendimento por analistas Jr
- compatibilidade com Windows/PowerShell/VS Code
- aderência ao ambiente `.venv`
- coerência com a estrutura atual

---

# 18. REGRAS FINAIS DE TOMADA DE DECISÃO PARA A LLM

Quando houver dúvida entre duas alternativas, preferir a que:

1. preserve a estrutura atual
2. reduza complexidade
3. facilite manutenção futura
4. seja mais didática para um time de analistas
5. exija menos dependências externas
6. mantenha o projeto simples, mas pronto para crescer

---

# 19. RESUMO EXECUTIVO PARA A LLM

Este é um projeto Python local, pequeno, organizado e em fase inicial, com as seguintes características essenciais:

- Windows + PowerShell + VS Code
- ambiente virtual `.venv`
- Git + GitHub
- estrutura baseada em `src/app`
- `main.py` como ponto de entrada
- `utils.py` como primeiro módulo auxiliar
- `README.md` já preenchido
- `requirements.txt` já existente
- `.vscode/settings.json` já configurado para a `.venv`
- foco em clareza, simplicidade e crescimento organizado
- uso intensivo de vibe coding, mas com controle estrutural humano

A LLM deve agir como uma força de aceleração disciplinada, e não como geradora de complexidade desnecessária.

---

# 20. INSTRUÇÃO FINAL PARA O CODEX / LLM

Ao criar ou modificar código neste projeto:

- respeite a estrutura atual
- mantenha `main.py` enxuto
- modularize apenas quando houver necessidade real
- use nomes claros
- considere type hints
- preserve compatibilidade com Windows e PowerShell
- evite dependências desnecessárias
- não versione `.venv`
- trate `requirements.txt` como fonte de verdade das dependências
- proponha mudanças incrementais e bem organizadas
- priorize legibilidade e manutenção por analistas Jr

Se precisar expandir o projeto, faça isso de forma gradual, coerente e explicitamente alinhada à arquitetura já estabelecida.
