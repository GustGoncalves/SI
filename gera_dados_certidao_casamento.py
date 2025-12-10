import csv
import random
from datetime import date, timedelta
from faker import Faker

UFs = [
    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA",
    "MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN",
    "RS","RO","RR","SC","SP","SE","TO"
]

nacionalidades  = [
    "brasileira", "estrangeira"
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

def data_por_extenso(dt: date) -> str:
    dia_ext = numero_por_extenso(dt.day)
    mes_ext = MESES_PT[dt.month]
    ano_ext = numero_por_extenso(dt.year)
    return f"{dia_ext} de {mes_ext} de {ano_ext}".lower()

def gerar_matricula() -> str:
    grupos = [6, 2, 2, 4, 1, 5, 3, 7, 2]
    partes = []
    for g in grupos:
        num = ''.join(str(random.randint(0, 9)) for _ in range(g))
        partes.append(num)
    return ' '.join(partes)

PREFIXOS = {"dr", "dra", "sr", "sra", "srta"}

def garantir_tres_nomes(nome: str, fake: Faker, sexo: str) -> str:
    # Remove prefixos tipo "Dr.", "Sr.", etc
    partes = [p for p in nome.replace('.', '').split() if p.lower() not in PREFIXOS and p.isalpha()]

    while len(partes) < 3:
        novo_nome = fake.first_name_male() if sexo == 'M' else fake.first_name_female()
        partes.insert(1, novo_nome)

    partes = partes[:3]
    return ' '.join(p.upper() for p in partes)

def gerar_dados(qtd: int, seed: int | None = None):
    fake = Faker('pt_BR')
    if seed is not None:
        random.seed(seed)
        Faker.seed(seed)

    fake_unique = Faker('pt_BR')
    fake_unique.seed_instance(random.randint(1, 10**6))
    fake_unique.unique.clear()

    regimes_bens = [
        "Comunhão parcial de bens",
        "Comunhão universal de bens",
        "Separação total de bens",
        "Participação final nos aquestos"
    ]

    registros = []
    for _ in range(qtd):

        # Nome conjugue 1
        sexo = random.choice(['M', 'F'])
        raw_nome_genitor1 = fake.name_male() if sexo == 'M' else fake.name_female()
        nome_completo1 = garantir_tres_nomes(raw_nome_genitor1, fake, sexo)

        # Nome conjugue 2
        sexo = random.choice(['M', 'F'])
        raw_nome_genitor1 = fake.name_male() if sexo == 'M' else fake.name_female()
        nome_completo2 = garantir_tres_nomes(raw_nome_genitor1, fake, sexo)

        # Genitor 1 (masculino ou feminino aleatório)
        sexo_genitor1 = random.choice(['M', 'F'])
        raw_nome_genitor1 = fake.name_male() if sexo_genitor1 == 'M' else fake.name_female()
        nome_genitor1 = garantir_tres_nomes(raw_nome_genitor1, fake, sexo_genitor1)
        genitores1 = f"{garantir_tres_nomes(fake.name_male(), fake, 'M')} e {garantir_tres_nomes(fake.name_female(), fake, 'F')}"

        # Genitor 2 (sexo oposto ao genitor 1, para variar)
        sexo_genitor2 = 'F' if sexo_genitor1 == 'M' else 'M'
        raw_nome_genitor2 = fake.name_male() if sexo_genitor2 == 'M' else fake.name_female()
        nome_genitor2 = garantir_tres_nomes(raw_nome_genitor2, fake, sexo_genitor2)
        genitores2 = f"{garantir_tres_nomes(fake.name_male(), fake, 'M')} e {garantir_tres_nomes(fake.name_female(), fake, 'F')}"

        try:
            cpf1 = fake_unique.unique.cpf()
        except Exception:
            cpf1 = fake.cpf()

        try:
            cpf2 = fake_unique.unique.cpf()
        except Exception:
            cpf2 = fake.cpf()

        matricula = gerar_matricula()

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

        # data3
        anos3 = random.randint(0, 60)
        data_casamento = hoje - timedelta(days=anos3 * 365 + dias_extras)
        data_ext = data_por_extenso(data_casamento)

        dia3 = f"{data_casamento.day:02d}"
        mes3 = f"{data_casamento.month:02d}"
        ano3 = f"{data_casamento.year:04d}"

        municipio = fake.city()
        uf = random.choice(UFs)
        nacionalidade = random.choice(nacionalidades)

        estado_civil = 'Casado'
        regime_bens = random.choice(regimes_bens)

        registros.append({
            'nome_completo1': nome_completo1,
            'nome_completo2': nome_completo2,
            'numero_cpf1': cpf1,
            'numero_cpf2': cpf2,
            'matricula': matricula,
            'dia1': dia1,
            'mes1': mes1,
            'ano1': ano1,
            'dia2': dia2,
            'mes2': mes2,
            'ano2': ano2,
            'nacionalidade': nacionalidade,
            'estado_civil': estado_civil,
            'municipio': municipio,
            'uf': uf,
            'nome_genitor1': nome_genitor1,
            'nome_genitor2': nome_genitor2,
            'genitores1': genitores1,
            'genitores2': genitores2,
            'data_por_extenso': data_ext,
            'dia3': dia3,
            'mes3': mes3,
            'ano3': ano3,
            'regime_de_bens': regime_bens
        })

    return registros

def salvar_csv(registros, nome_arquivo="dados_certidao_casamento.csv"):
    campos = [
        'nome_completo1', 'nome_completo2', 'numero_cpf1', 'numero_cpf2', 'matricula', 'dia1',
        'mes1', 'ano1', 'dia2', 'mes2', 'ano2','nacionalidade', 'estado_civil', 'municipio', 'uf',
        'nome_genitor1', 'nome_genitor2', 'genitores1', 'genitores2', 'data_por_extenso',
        'dia3', 'mes3', 'ano3','regime_de_bens'
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