import csv
import random
from datetime import date, timedelta
from faker import Faker

profissoes = [
    "Professor", "Motorista", "Vendedor", "Padeiro", "Pedreiro",
    "Garçom", "Cozinheiro", "Estudante", "Advogado",
    "Enfermeiro", "Designer", "Programador"
]

MESES_PT = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro",
}

UNIDADES = [
    "zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove",
    "dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove"
]

DEZENAS = [
    "", "dez", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"
]

CENTENAS = [
    "", "cem", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos", "seiscentos", "setecentos", "oitocentos", "novecentos"
]

def numero_por_extenso(n):
    if n < 20:
        return UNIDADES[n]
    elif n < 100:
        dez, un = divmod(n, 10)
        if un == 0:
            return DEZENAS[dez]
        return f"{DEZENAS[dez]} e {UNIDADES[un]}"
    elif n < 1000:
        cen, resto = divmod(n, 100)
        if n == 100:
            return "cem"
        if resto == 0:
            return CENTENAS[cen]
        return f"{CENTENAS[cen]} e {numero_por_extenso(resto)}"
    elif n < 2000:
        return f"mil {numero_por_extenso(n % 1000)}" if n % 1000 != 0 else "mil"
    elif n < 10000:
        mil, resto = divmod(n, 1000)
        if resto == 0:
            return f"{UNIDADES[mil]} mil"
        return f"{UNIDADES[mil]} mil {numero_por_extenso(resto)}"
    else:
        milhar, resto = divmod(n, 1000)
        texto_milhar = f"{numero_por_extenso(milhar)} mil"
        if resto == 0:
            return texto_milhar
        else:
            return f"{texto_milhar} e {numero_por_extenso(resto)}"


PREFIXOS = {"dr", "dra", "sr", "sra", "srta"}

def garantir_tres_nomes(nome: str, fake: Faker, sexo: str) -> str:
    # Remove prefixos tipo "Dr.", "Sr.", etc
    partes = [p for p in nome.replace('.', '').split() if p.lower() not in PREFIXOS and p.isalpha()]

    while len(partes) < 3:
        novo_nome = fake.first_name_male() if sexo == 'M' else fake.first_name_female()
        partes.insert(1, novo_nome)

    partes = partes[:3]
    return ' '.join(p for p in partes)

def gerar_dados(qtd: int, seed: int | None = None):
    fake = Faker('pt_BR')
    if seed is not None:
        random.seed(seed)
        Faker.seed(seed)

    fake_unique = Faker('pt_BR')
    fake_unique.seed_instance(random.randint(1, 10**6))
    fake_unique.unique.clear()

    registros = []
    for _ in range(qtd):

        numero_casamento = random.randint(10000, 99999)
        folhas = random.randint(1, 999)
        livro = random.randint(1, 999)
        ato = 'lavrado'

        # Nome conjugue 1
        sexo1 = random.choice(['M', 'F'])
        raw_nome_genitor1 = fake.name_male() if sexo1 == 'M' else fake.name_female()
        nome_completo1 = garantir_tres_nomes(raw_nome_genitor1, fake, sexo1)

        # Nome conjugue 2
        sexo2 = random.choice(['M', 'F'])
        raw_nome_genitor1 = fake.name_male() if sexo2 == 'M' else fake.name_female()
        nome_completo2 = garantir_tres_nomes(raw_nome_genitor1, fake, sexo2)

        sexo_juiz = random.choice(['M', 'F'])
        raw_nome_juiz = fake.name_male() if sexo_juiz == 'M' else fake.name_female()
        juiz = garantir_tres_nomes(raw_nome_juiz, fake, sexo_juiz)

        #Testemunhas
        testemunhas = f"{garantir_tres_nomes(fake.name_male(), fake, 'M')} e {garantir_tres_nomes(fake.name_female(), fake, 'F')}"

        # Genitor 1 (masculino ou feminino aleatório)
        sexo_genitor1 = 'M'
        raw_nome_genitor1 = fake.name_male() if sexo_genitor1 == 'M' else fake.name_female()
        nome_genitor1 = garantir_tres_nomes(raw_nome_genitor1, fake, sexo_genitor1)

        # Genitor 2 (sexo oposto ao genitor 1, para variar)
        sexo_genitor2 = 'F'
        raw_nome_genitor2 = fake.name_male() if sexo_genitor2 == 'M' else fake.name_female()
        nome_genitor2 = garantir_tres_nomes(raw_nome_genitor2, fake, sexo_genitor2)

        sexo_genitor3 = 'M'
        raw_nome_genitor3 = fake.name_male() if sexo_genitor3 == 'M' else fake.name_female()
        nome_genitor3 = garantir_tres_nomes(raw_nome_genitor3, fake, sexo_genitor1)

        # Genitor 4 (sexo oposto ao genitor 1, para variar)
        sexo_genitor4 = 'F'
        raw_nome_genitor4 = fake.name_male() if sexo_genitor4 == 'M' else fake.name_female()
        nome_genitor4 = garantir_tres_nomes(raw_nome_genitor4, fake, sexo_genitor4)

        municipio = fake.city()

        #data1
        hoje = date.today()
        anos1 = random.randint(0, 90)
        dias_extras = random.randint(0, 364)

        data_nasc1 = hoje - timedelta(days=anos1 * 365 + dias_extras)

        dia1 = f"{data_nasc1.day:02d}"
        mes1 = f"{data_nasc1.month:02d}"
        ano1 = f"{data_nasc1.year:04d}"

        # data2
        anos2 = random.randint(0, 90)
        data_nasc2 = hoje - timedelta(days=anos2 * 365 + dias_extras)

        dia2 = f"{data_nasc2.day:02d}"
        mes2 = f"{data_nasc2.month:02d}"
        ano2 = f"{data_nasc2.year:04d}"

        profissao = random.choice(profissoes)
        domicilio = f"{fake.street_name()}, {fake.building_number()}"
        residencia = domicilio

        registros.append({
            'numero_casamento': numero_casamento,
            'folhas': folhas,
            'livro': livro,
            'ato': ato,
            'nome_completo1': nome_completo1,
            'nome_completo2': nome_completo2,
            'juiz': juiz,
            'testemunhas': testemunhas,
            'municipio': municipio,
            'dia1': dia1,
            'mes1': mes1,
            'ano1': ano1,
            'dia2': dia2,
            'mes2': mes2,
            'ano2': ano2,
            'profissao': profissao,
            'domicilio': domicilio,
            'residencia': residencia,
            'nome_genitor1': nome_genitor1,
            'nome_genitor2': nome_genitor2,
            'nome_genitor3': nome_genitor3,
            'nome_genitor4': nome_genitor4
        })

    return registros

def salvar_csv(registros, nome_arquivo="dados_certidao_casamento_antiga.csv"):
    campos = [
        'numero_casamento', 'folhas', 'livro', 'ato',
        'nome_completo1', 'nome_completo2',
        'juiz', 'testemunhas', 'municipio','dia1',
        'mes1', 'ano1', 'dia2', 'mes2', 'ano2',
        'profissao', 'domicilio', 'residencia',
        'nome_genitor1', 'nome_genitor2', 'nome_genitor3', 'nome_genitor4'
    ]
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        for r in registros:
            escritor.writerow(r)
    print(f"{len(registros)} registros salvos em '{nome_arquivo}'")

if __name__ == '__main__':
    qtd = int(input("Quantos registros deseja gerar? "))
    seed_input = input("Semente (seed) opcional para reprodutibilidade (enter para pular): ")
    seed = int(seed_input) if seed_input.strip() != '' else None
    regs = gerar_dados(qtd, seed)
    salvar_csv(regs)