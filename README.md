# Desafio de Automação Digital: Gestão de Peças, Qualidade e Armazenamento

Protótipo em **Python** (terminal) que automatiza a inspeção de qualidade de peças de uma linha de montagem, o armazenamento das peças aprovadas em caixas e a geração de relatórios consolidados.

> Trabalho da disciplina **Algoritmos e Lógica de Programação** — UniFECAF.
> Autor: **Lucas Ramos Teixeira** | RA: **252815**

---

## 1. O que o sistema faz

- Recebe os dados de cada peça: **id, peso, cor e comprimento**.
- Avalia automaticamente se a peça está **APROVADA** ou **REPROVADA**:

| Critério | Regra de aprovação |
|---|---|
| Peso | entre **95 g e 105 g** (limites incluídos) |
| Cor | **azul** ou **verde** (aceita maiúsculas/minúsculas e acentos) |
| Comprimento | entre **10 cm e 20 cm** (limites incluídos) |

- Uma peça é aprovada **somente se cumprir os três critérios**. Se falhar em qualquer um, é reprovada e o sistema registra **todos** os motivos.
- Armazena as peças aprovadas em **caixas de 10 peças**. Ao atingir 10, a caixa é **fechada** e uma nova é iniciada.
- Gera relatório com: total de aprovadas, total de reprovadas **com motivos**, e quantidade de caixas utilizadas.

## 2. Como rodar (passo a passo)

1. Instale o **Python 3.8 ou superior** (https://www.python.org/downloads/). No Windows, marque **"Add Python to PATH"** durante a instalação.
2. Baixe este repositório (botão **Code → Download ZIP**) e extraia, ou clone:
   ```bash
   git clone https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git
   cd NOME-DO-REPOSITORIO
   ```
3. No terminal, dentro da pasta do projeto, execute:
   ```bash
   python main.py
   ```
   (No Linux/macOS, se `python` não funcionar, use `python3 main.py`.)
4. Use o menu digitando o número da opção e pressionando **ENTER**.

Não há bibliotecas externas: o programa usa apenas a biblioteca padrão do Python.

## 3. Menu

| Opção | Função |
|---|---|
| 1 | Cadastrar nova peça (avalia e armazena automaticamente) |
| 2 | Listar peças aprovadas / reprovadas / todas (com motivos) |
| 3 | Remover peça cadastrada (pede confirmação e reorganiza as caixas) |
| 4 | Listar caixas fechadas (mostra também a caixa em aberto) |
| 5 | Gerar relatório final |
| 6 | *Extra:* carregar 12 peças de exemplo para demonstração |
| 0 | Sair |

## 4. Exemplos de entradas e saídas

**Peça aprovada**
```
ID da peça: P001
Peso (g): 100
Cor da peça: azul
Comprimento (cm): 15

>>> Peça P001 APROVADA.
>>> Armazenada na Caixa 1 (1/10).
```

**Peça reprovada com múltiplos motivos**
```
ID da peça: P002
Peso (g): 110
Cor da peça: vermelho
Comprimento (cm): 25

>>> Peça P002 REPROVADA. Motivo(s):
    - Peso fora da faixa (95g a 105g)
    - Cor inválida (aceitas: azul ou verde)
    - Comprimento fora da faixa (10cm a 20cm)
```

**Validação de entrada**
```
ID da peça:   [ERRO] Já existe uma peça com o ID 'P001'.
Peso (g):   [ERRO] Digite um número válido (ex.: 100 ou 98,5).
```

**Fechamento de caixa**
```
>>> Peça P004 APROVADA.
>>> Caixa 1 atingiu 10 peças e foi FECHADA. Uma nova caixa foi iniciada.
```

**Listar caixas fechadas (opção 4)**
```
Caixa 1 - FECHADA (10/10)
  Peças: P001, P003, D01, D02, D03, D04, D05, D06, D07, D08
```

**Relatório final (opção 5)**
```
Total de peças cadastradas : 15
Total de peças aprovadas   : 10
Total de peças reprovadas  : 5
Taxa de aprovação          : 66,7%

--- Motivos de reprovação ---
  3x Peso fora da faixa (95g a 105g)
  3x Cor inválida (aceitas: azul ou verde)
  3x Comprimento fora da faixa (10cm a 20cm)

--- Caixas ---
Caixas fechadas            : 1
Peças na caixa em aberto   : 0
Total de caixas utilizadas : 1
```

## 5. Estrutura do código

| Elemento | Descrição |
|---|---|
| Constantes no topo do arquivo | Critérios de qualidade e capacidade da caixa (alterar em um só lugar) |
| `pecas` (lista de dicionários) | Base de dados em memória; cada peça guarda id, peso, cor, comprimento, status e motivos |
| `avaliar_peca()` | Regras de negócio: devolve a lista de motivos de reprovação (vazia = aprovada) |
| `organizar_caixas()` | Distribui as aprovadas em caixas de 10, fechando cada caixa cheia |
| `ler_id()`, `ler_numero_positivo()`, `ler_cor()` | Leitura com validação (laços `while` até a entrada ser válida) |
| `cadastrar_peca()`, `listar_pecas()`, `remover_peca()`, `listar_caixas_fechadas()`, `gerar_relatorio()` | Uma função por opção do menu |
| `main()` | Laço principal do menu (dicionário de opções → funções) |

## 6. Decisões de projeto e limitações

- **Limites inclusivos:** 95 g, 105 g, 10 cm e 20 cm são considerados aprovados.
- **Cor fora do padrão** não é erro de digitação: é motivo de reprovação.
- **Remoção de peça:** funciona como desfazer um cadastro. As caixas são recalculadas como se a peça nunca tivesse sido registrada; por isso, remover uma peça aprovada de uma caixa fechada pode reabri-la (o sistema avisa).
- **Sem persistência:** os dados ficam apenas em memória e são perdidos ao encerrar o programa. Uma evolução natural é salvar em arquivo (CSV/JSON) ou banco de dados.
- **Entrada manual:** o protótipo simula a leitura de sensores por digitação.