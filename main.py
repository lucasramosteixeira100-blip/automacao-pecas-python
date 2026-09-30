"""
Desafio de Automação Digital: Gestão de Peças, Qualidade e Armazenamento
Disciplina: Algoritmos e Lógica de Programação

Sistema em terminal que:
  - cadastra peças (id, peso, cor e comprimento);
  - aprova ou reprova cada peça segundo critérios de qualidade;
  - armazena peças aprovadas em caixas de 10 unidades;
  - gera relatório consolidado.
"""

import unicodedata

# ----------------------------------------------------------------------
# CONSTANTES (critérios de qualidade) - alterar aqui muda todo o sistema
# ----------------------------------------------------------------------
PESO_MIN = 95.0          # gramas (inclusivo)
PESO_MAX = 105.0         # gramas (inclusivo)
CORES_VALIDAS = ("azul", "verde")
COMPRIMENTO_MIN = 10.0   # centímetros (inclusivo)
COMPRIMENTO_MAX = 20.0   # centímetros (inclusivo)
CAPACIDADE_CAIXA = 10    # peças por caixa

MOTIVO_PESO = f"Peso fora da faixa ({PESO_MIN:g}g a {PESO_MAX:g}g)"
MOTIVO_COR = "Cor inválida (aceitas: azul ou verde)"
MOTIVO_COMPRIMENTO = f"Comprimento fora da faixa ({COMPRIMENTO_MIN:g}cm a {COMPRIMENTO_MAX:g}cm)"

# Base de dados em memória: lista de dicionários (uma peça = um dicionário)
pecas = []


# ----------------------------------------------------------------------
# FUNÇÕES AUXILIARES DE ENTRADA (com validação)
# ----------------------------------------------------------------------
def normalizar_texto(texto):
    """Remove espaços, acentos e converte para minúsculas ('Azúl ' -> 'azul')."""
    texto = texto.strip().lower()
    decomposto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in decomposto if unicodedata.category(c) != "Mn")


def buscar_peca(id_peca):
    """Retorna a peça com o id informado ou None se não existir."""
    for peca in pecas:
        if peca["id"].lower() == id_peca.lower():
            return peca
    return None


def ler_id():
    """Lê um id não vazio e que ainda não exista no sistema."""
    while True:
        id_peca = input("ID da peça: ").strip()
        if id_peca == "":
            print("  [ERRO] O ID não pode ser vazio.")
        elif buscar_peca(id_peca) is not None:
            print(f"  [ERRO] Já existe uma peça com o ID '{id_peca}'.")
        else:
            return id_peca


def ler_numero_positivo(mensagem):
    """Lê um número > 0. Aceita vírgula ou ponto como separador decimal."""
    while True:
        entrada = input(mensagem).strip().replace(",", ".")
        try:
            valor = float(entrada)
        except ValueError:
            print("  [ERRO] Digite um número válido (ex.: 100 ou 98,5).")
            continue
        if valor <= 0:
            print("  [ERRO] O valor deve ser maior que zero.")
        else:
            return valor


def ler_cor():
    """Lê a cor (texto não vazio). Cor fora do padrão é motivo de reprovação, não de erro."""
    while True:
        cor = normalizar_texto(input("Cor da peça: "))
        if cor == "":
            print("  [ERRO] A cor não pode ser vazia.")
        else:
            return cor


# ----------------------------------------------------------------------
# REGRAS DE NEGÓCIO
# ----------------------------------------------------------------------
def avaliar_peca(peso, cor, comprimento):
    """
    Aplica os critérios de qualidade.
    Retorna a lista de motivos de reprovação (lista vazia = peça aprovada).
    """
    motivos = []
    if not (PESO_MIN <= peso <= PESO_MAX):
        motivos.append(MOTIVO_PESO)
    if cor not in CORES_VALIDAS:
        motivos.append(MOTIVO_COR)
    if not (COMPRIMENTO_MIN <= comprimento <= COMPRIMENTO_MAX):
        motivos.append(MOTIVO_COMPRIMENTO)
    return motivos


def criar_peca(id_peca, peso, cor, comprimento):
    """Avalia a peça e devolve o dicionário pronto para ser armazenado."""
    motivos = avaliar_peca(peso, cor, comprimento)
    return {
        "id": id_peca,
        "peso": peso,
        "cor": cor,
        "comprimento": comprimento,
        "status": "REPROVADA" if motivos else "APROVADA",
        "motivos": motivos,
    }


def organizar_caixas():
    """
    Distribui as peças aprovadas (na ordem de cadastro) em caixas.
    Quando uma caixa chega a CAPACIDADE_CAIXA peças, ela é FECHADA e uma nova é iniciada.
    Retorna (caixas_fechadas, caixa_aberta).
    """
    caixas_fechadas = []
    caixa_aberta = []
    for peca in pecas:
        if peca["status"] == "APROVADA":
            caixa_aberta.append(peca["id"])
            if len(caixa_aberta) == CAPACIDADE_CAIXA:
                caixas_fechadas.append(caixa_aberta)
                caixa_aberta = []
    return caixas_fechadas, caixa_aberta


def contar_caixas_usadas():
    """Caixas usadas = fechadas + a caixa aberta (se tiver ao menos uma peça)."""
    fechadas, aberta = organizar_caixas()
    return len(fechadas) + (1 if aberta else 0)


# ----------------------------------------------------------------------
# FORMATAÇÃO
# ----------------------------------------------------------------------
def linha(titulo=""):
    print("\n" + "=" * 60)
    if titulo:
        print(titulo.center(60))
        print("=" * 60)


def formatar_numero(valor):
    """Formata número no padrão brasileiro (97.5 -> '97,5')."""
    return f"{valor:g}".replace(".", ",")


def descrever_peca(peca):
    peso = formatar_numero(peca["peso"]) + "g"
    comprimento = formatar_numero(peca["comprimento"]) + "cm"
    return (f"ID: {peca['id']:<6} | {peso:<7} | {peca['cor'].capitalize():<8} "
            f"| {comprimento:<7} | {peca['status']}")


def pausar():
    input("\nPressione ENTER para voltar ao menu...")


# ----------------------------------------------------------------------
# OPÇÕES DO MENU
# ----------------------------------------------------------------------
def cadastrar_peca():
    linha("1 - CADASTRAR NOVA PEÇA")
    id_peca = ler_id()
    peso = ler_numero_positivo("Peso (g): ")
    cor = ler_cor()
    comprimento = ler_numero_positivo("Comprimento (cm): ")

    fechadas_antes, _ = organizar_caixas()
    peca = criar_peca(id_peca, peso, cor, comprimento)
    pecas.append(peca)
    fechadas_depois, aberta = organizar_caixas()

    print()
    if peca["status"] == "APROVADA":
        print(f">>> Peça {id_peca} APROVADA.")
        if len(fechadas_depois) > len(fechadas_antes):
            print(f">>> Caixa {len(fechadas_depois)} atingiu {CAPACIDADE_CAIXA} peças e foi FECHADA. "
                  f"Uma nova caixa foi iniciada.")
        else:
            numero = len(fechadas_depois) + 1
            print(f">>> Armazenada na Caixa {numero} ({len(aberta)}/{CAPACIDADE_CAIXA}).")
    else:
        print(f">>> Peça {id_peca} REPROVADA. Motivo(s):")
        for motivo in peca["motivos"]:
            print(f"    - {motivo}")
    pausar()


def listar_pecas():
    linha("2 - LISTAR PEÇAS")
    print("1 - Aprovadas\n2 - Reprovadas\n3 - Todas")
    escolha = input("Escolha: ").strip()
    if escolha not in ("1", "2", "3"):
        print("  [ERRO] Opção inválida.")
        pausar()
        return

    if escolha == "1":
        filtradas = [p for p in pecas if p["status"] == "APROVADA"]
        titulo = "PEÇAS APROVADAS"
    elif escolha == "2":
        filtradas = [p for p in pecas if p["status"] == "REPROVADA"]
        titulo = "PEÇAS REPROVADAS"
    else:
        filtradas = pecas
        titulo = "TODAS AS PEÇAS"

    linha(f"{titulo} ({len(filtradas)})")
    if not filtradas:
        print("Nenhuma peça encontrada.")
    for peca in filtradas:
        print(descrever_peca(peca))
        for motivo in peca["motivos"]:
            print(f"      ↳ {motivo}")
    pausar()


def remover_peca():
    linha("3 - REMOVER PEÇA CADASTRADA")
    if not pecas:
        print("Não há peças cadastradas.")
        pausar()
        return

    id_peca = input("ID da peça a remover: ").strip()
    peca = buscar_peca(id_peca)
    if peca is None:
        print(f"  [ERRO] Peça '{id_peca}' não encontrada.")
        pausar()
        return

    print("\nPeça encontrada:")
    print(descrever_peca(peca))
    confirmacao = input("Confirmar remoção? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("Remoção cancelada.")
        pausar()
        return

    fechadas_antes, _ = organizar_caixas()
    pecas.remove(peca)
    fechadas_depois, aberta = organizar_caixas()

    print(f"\n>>> Peça {peca['id']} removida com sucesso.")
    if peca["status"] == "APROVADA":
        print(">>> Caixas reorganizadas automaticamente.")
        if len(fechadas_depois) < len(fechadas_antes):
            print(f">>> ATENÇÃO: uma caixa que estava fechada voltou a ficar ABERTA "
                  f"({len(aberta)}/{CAPACIDADE_CAIXA} peças).")
    pausar()


def listar_caixas_fechadas():
    linha("4 - CAIXAS FECHADAS")
    fechadas, aberta = organizar_caixas()
    if not fechadas:
        print("Nenhuma caixa fechada até o momento.")
    for numero, caixa in enumerate(fechadas, start=1):
        print(f"\nCaixa {numero} - FECHADA ({len(caixa)}/{CAPACIDADE_CAIXA})")
        print("  Peças: " + ", ".join(caixa))
    print("\n" + "-" * 60)
    if aberta:
        print(f"Caixa {len(fechadas) + 1} - EM ABERTO ({len(aberta)}/{CAPACIDADE_CAIXA}): "
              + ", ".join(aberta))
    else:
        print("Nenhuma caixa em aberto no momento.")
    pausar()


def gerar_relatorio():
    linha("5 - RELATÓRIO FINAL")
    aprovadas = [p for p in pecas if p["status"] == "APROVADA"]
    reprovadas = [p for p in pecas if p["status"] == "REPROVADA"]
    fechadas, aberta = organizar_caixas()

    print(f"Total de peças cadastradas : {len(pecas)}")
    print(f"Total de peças aprovadas   : {len(aprovadas)}")
    print(f"Total de peças reprovadas  : {len(reprovadas)}")
    if pecas:
        taxa = len(aprovadas) / len(pecas) * 100
        print(f"Taxa de aprovação          : {taxa:.1f}%".replace(".", ","))

    print("\n--- Motivos de reprovação ---")
    if not reprovadas:
        print("Nenhuma peça reprovada.")
    else:
        contagem = {}
        for peca in reprovadas:
            for motivo in peca["motivos"]:
                contagem[motivo] = contagem.get(motivo, 0) + 1
        for motivo, qtd in contagem.items():
            print(f"  {qtd}x {motivo}")
        print("  (uma peça pode ter mais de um motivo)")
        print("\nDetalhe por peça reprovada:")
        for peca in reprovadas:
            print(f"  {peca['id']}: " + "; ".join(peca["motivos"]))

    print("\n--- Caixas ---")
    print(f"Caixas fechadas            : {len(fechadas)}")
    print(f"Peças na caixa em aberto   : {len(aberta)}")
    print(f"Total de caixas utilizadas : {len(fechadas) + (1 if aberta else 0)}")
    pausar()


def carregar_dados_exemplo():
    """Opção extra para demonstração: carrega 12 peças (8 aprovadas e 4 reprovadas)."""
    linha("6 - CARREGAR DADOS DE EXEMPLO")
    exemplos = [
        ("D01", 95, "azul", 10),        # limite inferior de tudo (aprovada)
        ("D02", 105, "verde", 20),      # limite superior de tudo (aprovada)
        ("D03", 100, "azul", 15),
        ("D04", 98.5, "verde", 12),
        ("D05", 101, "azul", 18),
        ("D06", 99, "verde", 14.5),
        ("D07", 103, "azul", 11),
        ("D08", 97, "verde", 19),
        ("D09", 108, "azul", 15),       # reprovada: peso
        ("D10", 100, "vermelho", 15),   # reprovada: cor
        ("D11", 90, "verde", 25),       # reprovada: peso + comprimento
        ("D12", 100, "amarelo", 8),     # reprovada: cor + comprimento
    ]
    carregadas = 0
    for id_peca, peso, cor, comprimento in exemplos:
        if buscar_peca(id_peca) is None:
            pecas.append(criar_peca(id_peca, float(peso), cor, float(comprimento)))
            carregadas += 1
    print(f">>> {carregadas} peças de exemplo carregadas.")
    pausar()


# ----------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ----------------------------------------------------------------------
def exibir_menu():
    linha("CONTROLE DE QUALIDADE DE PEÇAS")
    print("1 - Cadastrar nova peça")
    print("2 - Listar peças aprovadas/reprovadas")
    print("3 - Remover peça cadastrada")
    print("4 - Listar caixas fechadas")
    print("5 - Gerar relatório final")
    print("6 - Carregar dados de exemplo (demonstração)")
    print("0 - Sair")


def main():
    acoes = {
        "1": cadastrar_peca,
        "2": listar_pecas,
        "3": remover_peca,
        "4": listar_caixas_fechadas,
        "5": gerar_relatorio,
        "6": carregar_dados_exemplo,
    }
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            print("\nEncerrando o sistema. Até logo!")
            break
        elif opcao in acoes:
            acoes[opcao]()
        else:
            print("  [ERRO] Opção inválida. Digite um número de 0 a 6.")


if __name__ == "__main__":
    main()