# -*- coding: utf-8 -*-
"""Restaura acentuacao/cedilha em portugues no dataset (escrito sem diacriticos
para evitar problemas de encoding). Substituicao por palavra inteira (word
boundary), preservando a caixa original (maiuscula/minuscula/capitalizada).
"""
import re

# chave (sem acento, minuscula) -> valor correto (com acento, minuscula)
MAP = {
    "nao": "não", "sao": "são", "regiao": "região", "regioes": "regiões",
    "acao": "ação", "acoes": "ações", "infeccao": "infecção", "infeccoes": "infecções",
    "inflamacao": "inflamação", "inflamacoes": "inflamações",
    "destruicao": "destruição", "disseminacao": "disseminação",
    "formacao": "formação", "obstrucao": "obstrução", "duracao": "duração",
    "remocao": "remoção", "localizacao": "localização", "coloracao": "coloração",
    "tumefacao": "tumefação", "mastigacao": "mastigação",
    "radiografico": "radiográfico", "radiografica": "radiográfica",
    "radiograficas": "radiográficas", "radiograficos": "radiográficos",
    "histopatologico": "histopatológico", "histopatologica": "histopatológica",
    "histopatologicas": "histopatológicas", "histopatologicos": "histopatológicos",
    "patologico": "patológico", "patologica": "patológica",
    "odontologico": "odontológico", "odontologica": "odontológica",
    "odontogenico": "odontogênico", "odontogenica": "odontogênica",
    "evolucao": "evolução", "sequencia": "sequência",
    "prognostico": "prognóstico", "diagnostico": "diagnóstico",
    "diagnosticos": "diagnósticos", "unico": "único", "unica": "única",
    "dificil": "difícil", "possivel": "possível", "impossivel": "impossível",
    "predominancia": "predominância", "tendencia": "tendência",
    "incidencia": "incidência", "prevalencia": "prevalência",
    "rapida": "rápida", "rapido": "rápido", "unicas": "únicas",
    "varios": "vários", "varias": "várias", "tambem": "também",
    "atraves": "através", "alem": "além", "ate": "até",
    "proximo": "próximo", "proxima": "próxima", "medio": "médio", "media": "média",
    "genero": "gênero", "periosteo": "periósteo",
    "osseo": "ósseo", "ossea": "óssea", "osseos": "ósseos", "osseas": "ósseas",
    "imunossupressao": "imunossupressão", "supuracao": "supuração",
    "agudizacao": "agudização", "cicatrizacao": "cicatrização",
    "reabsorcao": "reabsorção", "expansao": "expansão", "extensao": "extensão",
    "extensoes": "extensões", "atencao": "atenção", "condicao": "condição",
    "condicoes": "condições", "complicacao": "complicação",
    "complicacoes": "complicações", "reacao": "reação", "relacao": "relação",
    "relacoes": "relações", "classificacao": "classificação",
    "eliminacao": "eliminação", "resolucao": "resolução", "avaliacao": "avaliação",
    "reavaliacao": "reavaliação", "indicacao": "indicação",
    "indicacoes": "indicações", "caracteristicas": "características",
    "caracteristica": "característica", "fistula": "fístula", "fistulas": "fístulas",
    "lamina": "lâmina", "apice": "ápice", "percussao": "percussão",
    "radiolucida": "radiolúcida", "radiolucido": "radiolúcido",
    "radiolucidas": "radiolúcidas", "radiolucidos": "radiolúcidos",
    "oftalmica": "oftálmica", "meningeas": "meníngeas", "mater": "máter",
    "anatomicas": "anatômicas", "retrograda": "retrógrada",
    "nauseas": "náuseas", "delirio": "delírio", "respiratoria": "respiratória",
    "historica": "histórica", "faringeo": "faríngeo",
    "retrofaringeo": "retrofaríngeo", "consequencias": "consequências",
    "claviculas": "clavículas", "elevacao": "elevação", "protrusao": "protrusão",
    "lingua": "língua", "restricao": "restrição", "inquietacao": "inquietação",
    "funcao": "função", "aspiracao": "aspiração", "antibiotico": "antibiótico",
    "antibioticos": "antibióticos", "obitos": "óbitos", "espacos": "espaços",
    "superficies": "superfícies", "sitio": "sítio", "litica": "lítica",
    "doencas": "doenças", "doenca": "doença", "sistemicas": "sistêmicas",
    "sistemicos": "sistêmicos", "sistemicamente": "sistemicamente",
    "vascularizacao": "vascularização", "malaria": "malária",
    "desnutricao": "desnutrição", "mandibula": "mandíbula",
    "necrotico": "necrótico", "espontanea": "espontânea",
    "espontaneamente": "espontaneamente", "biopsia": "biópsia",
    "predominio": "predomínio", "conteudo": "conteúdo", "liquido": "líquido",
    "ausencia": "ausência", "granulacao": "granulação", "capsula": "cápsula",
    "comeca": "começa", "mes": "mês", "apos": "após",
    "clindamincina": "clindamicina", "diminuicao": "diminuição",
    "medicacoes": "medicações", "areas": "áreas", "area": "área",
    "genero": "gênero", "clinico": "clínico", "clinica": "clínica",
    "clinicas": "clínicas", "clinicos": "clínicos", "podera": "poderá",
    "sera": "será", "portugues": "português", "raiz": "raiz",
    "silenciosa": "silenciosa", "quimica": "química", "quimicas": "químicas",
    "quimico": "químico", "mecanica": "mecânica", "mecanico": "mecânico",
    "termica": "térmica", "termico": "térmico", "termicos": "térmicos",
    "eletricos": "elétricos", "vertebra": "vértebra", "vertice": "vértice",
    "publico": "público", "publica": "pública", "familia": "família",
    "familiar": "familiar", "degenerativo": "degenerativo",
    "reparador": "reparador", "grafica": "gráfica", "grafico": "gráfico",
    "sensivel": "sensível", "sensiveis": "sensíveis", "visiveis": "visíveis",
    "possiveis": "possíveis", "niveis": "níveis", "nivel": "nível",
    "reversivel": "reversível", "irreversivel": "irreversível",
    "cronica": "crônica", "cronico": "crônico", "cronicas": "crônicas",
    "cronicos": "crônicos", "polipo": "pólipo",
    "calcificacoes": "calcificações", "calcificacao": "calcificação",
    "denticulos": "dentículos", "calculos": "cálculos", "osteite": "osteíte",
    "alveolo": "alvéolo", "garre": "garré",
    "trombose": "trombose", "traumaticas": "traumáticas",
    "traumatico": "traumático", "traumaticos": "traumáticos",
    "inexperientes": "inexperientes", "contraceptivos": "contraceptivos",
    "irrigacao": "irrigação", "orientacao": "orientação",
    "confirmacao": "confirmação", "transformacao": "transformação",
    "proliferacao": "proliferação", "producao": "produção",
    "estimulo": "estímulo", "estimulos": "estímulos", "subita": "súbita",
    "acido": "ácido", "acidos": "ácidos", "iatrogenicos": "iatrogênicos",
    "iatrogenico": "iatrogênico", "barometricas": "barométricas",
    "metamorfose": "metamorfose", "amarelada": "amarelada",
    "esteticos": "estéticos", "estetica": "estética",
    "endodontia": "endodontia", "endodontico": "endodôntico",
    "endodonticamente": "endodonticamente", "instrumento": "instrumento",
    "prematuro": "prematuro", "prematura": "prematura", "oclusao": "oclusão",
    "oclusal": "oclusal", "pericoronarite": "pericoronarite",
    "trismo": "trismo", "odor": "odor", "fetido": "fétido",
    "impactados": "impactados", "profundamente": "profundamente",
    "cirurgioes": "cirurgiões", "sucao": "sucção", "cuspindo": "cuspindo",
    "curetar": "curetar", "curetagem": "curetagem", "sondagem": "sondagem",
    "analgesicos": "analgésicos", "analgesico": "analgésico",
    "potentes": "potentes", "higienizado": "higienizado",
    "adjacentes": "adjacentes", "malignas": "malignas",
    "epidermoide": "epidermoide", "epitelio": "epitélio",
    "epiteliais": "epiteliais", "epitelial": "epitelial",
    "malassez": "Malassez", "sinusal": "sinusal",
    "trajeto": "trajeto", "revestimento": "revestimento",
    "residual": "residual", "edentulo": "edêntulo", "edentula": "edêntula",
    "enucleacao": "enucleação", "cirurgica": "cirúrgica",
    "cirurgico": "cirúrgico", "obrigatoria": "obrigatória",
    "obrigatorio": "obrigatório", "intravenosos": "intravenosos",
    "resseccao": "ressecção", "reconstrucao": "reconstrução",
    "imobilizados": "imobilizados", "enfraquecidos": "enfraquecidos",
    "sequestros": "sequestros", "sequestro": "sequestro",
    "uniforme": "uniforme", "adjacente": "adjacente",
    "diferencial": "diferencial", "hipercementose": "hipercementose",
    "displasia": "displasia", "cemento": "cemento", "cemento-ossea": "cemento-óssea",
    "avancada": "avançada", "avancado": "avançado", "avancados": "avançados",
    "periostite": "periostite", "proliferativa": "proliferativa",
    "duplicacao": "duplicação", "hiperplasia": "hiperplasia",
    "hiperplasico": "hiperplásico", "hiperplasica": "hiperplásica",
    "periostal": "periosteal", "faixa": "faixa", "etaria": "etária",
    "predilecao": "predileção", "unifocal": "unifocal",
    "secundariamente": "secundariamente", "cortical": "cortical",
    "laminacoes": "laminações", "tomografia": "tomografia",
    "computadorizada": "computadorizada", "neoformado": "neoformado",
    "neoformacao": "neoformação", "consolidam": "consolidam",
    "remodelam": "remodelam", "questionado": "questionado",
    "neoplasicas": "neoplásicas", "condensante": "condensante",
    "esclerose": "esclerose", "esclerosante": "esclerosante",
    "focal": "focal", "reacional": "reacional", "incidental": "incidental",
    "casual": "casual", "residuo": "resíduo", "cicatriz": "cicatriz",
    "diferenciar": "diferenciar", "confinada": "confinada",
    "compacta": "compacta", "aparencia": "aparência",
    "sensacao": "sensação", "toxemia": "toxemia",
    "cefaleia": "cefaleia", "malestar": "mal-estar",
    "linfoadenopatia": "linfoadenopatia", "linfadenopatia": "linfadenopatia",
    "taquicardia": "taquicardia", "meningite": "meningite",
    "septicemia": "septicemia", "mediastinite": "mediastinite",
    "pericardite": "pericardite", "pneumonia": "pneumonia",
    "obstrutiva": "obstrutiva", "torpor": "torpor",
    "delirios": "delírios", "rigidez": "rigidez",
    "endurecimento": "endurecimento", "flutuacao": "flutuação",
    "penicilina": "penicilina", "escolha": "escolha",
    "resistencia": "resistência", "difusao": "difusão", "difundir": "difundir",
    "medula": "medula", "medulares": "medulares",
    "corticais": "corticais", "estende": "estende",
    "predisponentes": "predisponentes", "imunocomprometimento": "imunocomprometimento",
    "gengivite": "gengivite", "pre-existente": "pré-existente",
    "deficiente": "deficiente", "leucocitose": "leucocitose",
    "esfoliados": "esfoliados", "predominio": "predomínio",
    "granulomatoso": "granulomatoso", "exsudativa": "exsudativa",
    "necrotica": "necrótica", "infectado": "infectado",
    "trepanacao": "trepanação", "desgaste": "desgaste",
    "atraso": "atraso", "atrasa": "atrasa",
    "imunossupressao": "imunossupressão", "imunocomprometidos": "imunocomprometidos",
    "diabetes": "diabetes", "malignas": "malignas",
    "carcinoma": "carcinoma", "epidermoide": "epidermoide",
    "regridem": "regridem", "regressao": "regressão", "regride": "regride",
    "prognostico": "prognóstico",
    # segunda leva (achados na revisao do PDF)
    "alteracao": "alteração", "alteracoes": "alterações",
    "coronaria": "coronária", "coronario": "coronário",
    "dentario": "dentário", "dentaria": "dentária",
    "emergencia": "emergência", "emergencias": "emergências",
    "extracao": "extração", "extracoes": "extrações",
    "fixacao": "fixação", "historia": "história",
    "indistinguivel": "indistinguível", "inervacao": "inervação",
    "inflamatoria": "inflamatória", "inflamatorio": "inflamatório",
    "inflamatorios": "inflamatórios", "inflamatorias": "inflamatórias",
    "irritacao": "irritação", "laminacao": "laminação",
    "medicacao": "medicação", "obliteracao": "obliteração",
    "observacao": "observação", "oftalmologica": "oftalmológica",
    "oftalmologico": "oftalmológico", "passivel": "passível",
    "periorbitario": "periorbitário", "periorbitaria": "periorbitária",
    "prioritaria": "prioritária", "prioritario": "prioritário",
    "provavel": "provável", "provaveis": "prováveis",
    "radioluscencia": "radioluscência", "virulencia": "virulência",
    "visivel": "visível", "carie": "cárie", "caries": "cáries",
    "camara": "câmara", "camaras": "câmaras",
    "lesao": "lesão", "lesoes": "lesões", "colecao": "coleção",
    "aerea": "aérea", "aereas": "aéreas",
    "assintomatico": "assintomático", "assintomatica": "assintomática",
    "hipotese": "hipótese", "hipoteses": "hipóteses",
    "crianca": "criança", "criancas": "crianças",
    "classica": "clássica", "classico": "clássico",
    "classicos": "clássicos", "classicas": "clássicas",
    "sistemico": "sistêmico", "distincao": "distinção",
    "fenix": "fênix", "trigemeo": "trigêmeo",
    "diabetica": "diabética", "diabetico": "diabético",
    "reducao": "redução", "solucao": "solução",
    "estagio": "estágio", "estagios": "estágios",
    "exposicao": "exposição", "deciduos": "decíduos",
    "amielinica": "amielínica", "calcica": "cálcica",
    "previa": "prévia", "previo": "prévio",
    "insercao": "inserção", "insercoes": "inserções",
    "manutencao": "manutenção", "porcao": "porção", "porcoes": "porções",
    "restauracao": "restauração", "restauracoes": "restaurações",
    # terceira leva
    "acessorio": "acessório", "diaria": "diária", "diario": "diário",
    "dilatacao": "dilatação", "esfoliacao": "esfoliação",
    "evidencia": "evidência", "evidencias": "evidências",
    "internacao": "internação", "intervencao": "intervenção",
    "necessaria": "necessária", "necessario": "necessário",
    "operatoria": "operatória", "operatorio": "operatório",
    "palpacao": "palpação", "perfuracao": "perfuração",
    "persistencia": "persistência", "radioluscencias": "radioluscências",
    "ressecao": "ressecção", "resseccao": "ressecção",
    "succao": "sucção", "variavel": "variável", "variaveis": "variáveis",
    "extrusao": "extrusão", "cistica": "cística", "cistico": "cístico",
    "coagulo": "coágulo",
    "assintomaticos": "assintomáticos", "assintomaticas": "assintomáticas",
}

# ordena por tamanho decrescente para casar palavras compostas antes das simples
_KEYS = sorted(MAP.keys(), key=len, reverse=True)
_PATTERN = re.compile(r"\b(" + "|".join(re.escape(k) for k in _KEYS) + r")\b", re.IGNORECASE)


def _match_case(original, replacement):
    if original.isupper():
        return replacement.upper()
    if original[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def _sub(m):
    word = m.group(0)
    key = word.lower()
    return _match_case(word, MAP[key])


def fix_text(s):
    return _PATTERN.sub(_sub, s)


def fix(obj):
    """Aplica fix_text recursivamente em strings dentro de dict/list/tuple."""
    if isinstance(obj, str):
        return fix_text(obj)
    if isinstance(obj, list):
        return [fix(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(fix(v) for v in obj)
    if isinstance(obj, dict):
        return {k: fix(v) for k, v in obj.items()}
    return obj


# campos que NAO devem ser tocados (ids/keys tecnicas usadas em codigo)
_DISEASE_SKIP_KEYS = {"id", "categoria", "diagram"}
_QUIZ_SKIP_KEYS = {"id", "kind", "disease", "options_ids", "categoria"}


def patch_pathdata(pd):
    """Corrige acentuacao apenas nos campos de texto (preserva ids/keys)."""
    for d in pd.DISEASES:
        for k in list(d.keys()):
            if k in _DISEASE_SKIP_KEYS:
                continue
            d[k] = fix(d[k])
    pd.DISEASE_BY_ID = {d["id"]: d for d in pd.DISEASES}

    for q in pd.QUIZ:
        for k in list(q.keys()):
            if k in _QUIZ_SKIP_KEYS:
                continue
            q[k] = fix(q[k])

    pd.CATEGORIES = [(cid, fix_text(label)) for cid, label in pd.CATEGORIES]
    pd.CAT_LABEL = dict(pd.CATEGORIES)
