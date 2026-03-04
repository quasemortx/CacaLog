from datetime import datetime

import pytz


def get_current_timestamp() -> str:
    # ISO format or readable format for sheets
    tz = pytz.timezone("America/Sao_Paulo")
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")


def normalize_text(text: str) -> str:
    return text.strip().lower() if text else ""


def sanitize_for_sheets(text: str) -> str:
    return text.replace("\n", " | ").replace("\r", "").strip()


def classify_sector(status: str, observacao: str) -> str:
    """
    Determines responsible sector (TI vs Manutencao) based on observation keywords.
    Only applies if Status is NOT OK.
    """
    # Logic provided by user:
    # 1. Manutenção: projetor|datashow|áudio|audio|som|caixa de som|caixa|microfone|amplificador
    # 2. TI: ssd|hd|mem[oó]ria|ram|estabilizador|carrinho|cpu|pc|computador|gabinete|fonte|placa|monitor|teclado|mouse
    # 3. Else: Indefinido

    if status == "OK":
        return ""

    # Special Case: Status ATUALIZANDO -> TI
    # (User: "maquinas 'subindo' ou 'atualizando' ... são problemas da TI")
    if status == "ATUALIZANDO":
        return "TI"

    obs_lower = observacao.lower() if observacao else ""

    # Manutenção Keywords
    kw_manutencao = [
        "projetor",
        "datashow",
        "áudio",
        "audio",
        "som",
        "caixa de som",
        "caixa",
        "microfone",
        "amplificador",
        "ar condicionado",
        "ar-condicionado",
        "luz",
        "tomada",
        "tma",
        "video",
        "vídeo",
        "cabo",
        "hdmi",
        "cadeira",
    ]
    if any(k in obs_lower for k in kw_manutencao):
        return "Manutenção"

    # TI Keywords
    kw_ti = [
        "ssd",
        "hd",
        "memória",
        "memoria",
        "ram",
        "estabilizador",
        "carrinho",
        "cpu",
        "pc",
        "computador",
        "gabinete",
        "fonte",
        "placa",
        "monitor",
        "teclado",
        "mouse",
        "rede",
        "cabo",
        "internet",
        "wifi",
        "bios",
        "boot",
        "formatar",
        "windows",
        "falha de confiança",
        "sem maquina",
        "sem máquina",
        "subindo",
        "atualizando",
        "390",
        "lenovo",
        "optiplex",
        "dell",
        "adaptador",
    ]
    if any(k in obs_lower for k in kw_ti):
        return "TI"

    return "Indefinido"
