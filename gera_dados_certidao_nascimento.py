import csv
import random
from datetime import date, timedelta
from faker import Faker

UFs = [
    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA",
    "MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN",
    "RS","RO","RR","SC","SP","SE","TO"
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

def gerar_horario() -> str:
    h = random.randint(0, 23)
    m = random.randint(0, 59)
    return f"{h:02d}:{m:02d}"

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

    registros = []
    for _ in range(qtd):
        sexo = random.choice(['M', 'F'])
        raw_nome_pessoa = fake.name_male() if sexo == 'M' else fake.name_female()
        nome_completo = garantir_tres_nomes(raw_nome_pessoa, fake, sexo)

        # Genitor 1 (masculino ou feminino aleatório)
        sexo_genitor1 = random.choice(['M', 'F'])
        raw_nome_genitor1 = fake.name_male() if sexo_genitor1 == 'M' else fake.name_female()
        nome_genitor1 = garantir_tres_nomes(raw_nome_genitor1, fake, sexo_genitor1)
        avos_genitor1 = f"{garantir_tres_nomes(fake.name_male(), fake, 'M')} e {garantir_tres_nomes(fake.name_female(), fake, 'F')}"

        # Genitor 2 (sexo oposto ao genitor 1, para variar)
        sexo_genitor2 = 'F' if sexo_genitor1 == 'M' else 'M'
        raw_nome_genitor2 = fake.name_male() if sexo_genitor2 == 'M' else fake.name_female()
        nome_genitor2 = garantir_tres_nomes(raw_nome_genitor2, fake, sexo_genitor2)
        avos_genitor2 = f"{garantir_tres_nomes(fake.name_male(), fake, 'M')} e {garantir_tres_nomes(fake.name_female(), fake, 'F')}"

        try:
            cpf = fake_unique.unique.cpf()
        except Exception:
            cpf = fake.cpf()

        matricula = gerar_matricula()

        hoje = date.today()
        anos = random.randint(0, 90)
        dias_extras = random.randint(0, 364)
        data_nasc = hoje - timedelta(days=anos * 365 + dias_extras)
        data_ext = data_por_extenso(data_nasc)

        dia = f"{data_nasc.day:02d}"
        mes = f"{data_nasc.month:02d}"
        ano = f"{data_nasc.year:04d}"

        horario_nasc = gerar_horario()
        municipio = fake.city()
        uf = random.choice(UFs)

        tipo_local = random.choice(['Hospital', 'Maternidade', 'Domicílio', 'Clínica'])
        if tipo_local == 'Domicílio':
            local_nascimento = 'Domicílio'
        else:
            sobrenome_local = fake.last_name()
            local_nascimento = f"{tipo_local} {sobrenome_local}"

        gemeo = 'SIM' if random.random() < 0.05 else 'NÃO'

        registros.append({
            'nome_completo': nome_completo,
            'numero_cpf': cpf,
            'matricula': matricula,
            'data_por_extenso': data_ext,
            'dia': dia,
            'mes': mes,
            'ano': ano,
            'horario_nascimento': horario_nasc,
            'municipio': municipio,
            'uf': uf,
            'local_nascimento': local_nascimento,
            'sexo': sexo,
            'nome_genitor1': nome_genitor1,
            'avos_genitor1': avos_genitor1,
            'nome_genitor2': nome_genitor2,
            'avos_genitor2': avos_genitor2,
            'gemeo': gemeo
        })

    return registros

def salvar_csv(registros, nome_arquivo="dados_certidao_nascimento.csv"):
    campos = [
        'nome_completo', 'numero_cpf', 'matricula', 'dia', 'mes', 'ano',
        'data_por_extenso', 'horario_nascimento', 'municipio', 'uf',
        'local_nascimento', 'sexo', 'nome_genitor1', 'avos_genitor1',
        'nome_genitor2', 'avos_genitor2', 'gemeo'
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