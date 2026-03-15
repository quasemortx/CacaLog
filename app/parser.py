import re
from typing import Any

from app.schemas.enums import Status, TipoAmbiente

# Regex compilado para Salas
# Prédio 1: 3 dígitos, Andar = 1º dígito.
# Prédio 2: 4 dígitos, Andar = 1º dígito.
# Final 01-29. Exceção 012.
REGEX_SALA = re.compile(r"\b(?:S-?)?(012|[1-9]\d{2,3})\b", re.IGNORECASE)

# Regex Labs: Exige "Lab" ou "L-" antes do número (Ex: Lab 01, L-21). "03" solto é ignorado.
REGEX_LAB = re.compile(r"\b(?:Lab(?:oratori[oa])?\.?\s*|L-)(\d{1,2})\b", re.IGNORECASE)


def validate_sala(numero_str: str) -> dict | None:
    # Regras de validacao de numero
    try:
        int(numero_str)
        # "012" -> int 12. Regra diz 3 digitos. Entao 012 deve ser tratado como string '012' se capturado assim.

        # Ajuste: passar a string original capturada pelo regex é melhor
        if len(numero_str) == 3:  # Predio 1
            if numero_str == "012":
                return {"sala": "012", "predio": 1, "andar": 1, "local_id": "S-012"}

            andar = int(numero_str[0])
            final = int(numero_str[1:])
            predio = 1
        elif len(numero_str) == 4:  # Predio 2
            andar = int(numero_str[0])
            final = int(numero_str[2:])
            predio = 2
        else:
            return None

        # VALIDAÇÃO FORTE: Índice deve ser 00..29 (Permitir "600", "700")
        if final < 0 or final > 29:
            return None

        # Montar ID
        return {"sala": numero_str, "predio": predio, "andar": andar, "local_id": f"S-{numero_str}"}

    except ValueError:
        return None


# Constants for Disambiguation
ALWAYS_MODELS = {"390", "5040", "7020", "7040"}
AMBIGUOUS_NUMBERS = {"3010", "3020"}

MODEL_KEYWORDS = {"optiplex", "dell", "modelo", "cpu", "pc", "máquina", "maquina", "desktop"}
ROOM_KEYWORDS = {
    "sala",
    "turma",
    "aula",
    "andar",
    "p1",
    "p2",
    "prédio",
    "predio",
    "laboratório",
    "lab",
}


def check_model_reference(text: str) -> bool:
    """
    Detects if message refers to a model or BIOS without room context.
    Now includes 3010/3020 if context is missing or ambiguous.
    """
    t = text.upper()

    # 1. BIOS A02-A14
    if re.search(r"\bA(?:0[2-9]|1[0-4])\b", t):
        return True

    # 2. Always Models
    for model in ALWAYS_MODELS:
        if model in t:
            return True

    # 3. Ambiguous (3010/3020)
    # If present, triggering "Qual sala?" is correct behavior if regex extraction skipped it.
    return any(n in t for n in AMBIGUOUS_NUMBERS)


def get_status_from_text(text: str) -> Status | None:
    """
    Centralized status extraction logic using keywords.
    """
    lower_text = text.lower()

    # Priority Order (Error/Incompatible > Updating > OK/Pending)
    # Check Incompatible
    if any(
        x in lower_text
        for x in ["nao suporta", "sem tpm", "incompativel", "incompatível", "390", "legado"]
    ):
        return Status.INCOMPATIVEL

    # Check Error
    if any(
        x in lower_text
        for x in [
            "erro",
            "falha",
            "defeito",
            "problema",
            "tela azul",
            "sem espaco",
            "sem espaço",
            "bug",
            "bugada",
            "bios",
            "boot",
            "travado",
            "driver",
        ]
    ):
        return Status.ERRO

    # Check Updating
    if any(
        x in lower_text
        for x in [
            "atualizando",
            "verificando",
            "subindo",
            "clonando",
            "fazendo",
            "formatando",
            "pancando",
            "pankando",
        ]
    ):
        return Status.ATUALIZANDO

    # Special Case: "Pendencias resolvidas" -> OK
    # Check this BEFORE Pendente check
    if any(x in lower_text for x in ["resolvido", "resolvidas", "resolvidos", "ok", "pronto"]):
        return Status.OK

    # Check Pendente
    if any(
        x in lower_text
        for x in [
            "pendente",
            "faltando",
            "sem",
            "instalar",
            "configurar",
            "hd",
            "sem net",
            "aguardando",
            "rever",
            "pendencia",
            "pendência",
        ]
    ):
        return Status.PENDENTE

    # Check OK
    if any(
        x in lower_text
        for x in [
            "ok",
            "pronto",
            "funcionando",
            "normal",
            "feito",
            "instalado",
            "concluido",
            "concluído",
            "resolvido",
            "resolvidos",
        ]
    ):
        return Status.OK

    return None


def extract_data_regex(message: str) -> list[dict[str, Any]]:
    results = []

    lower_msg = message.lower()

    # Context Detection
    has_model_kw = any(k in lower_msg for k in MODEL_KEYWORDS)
    has_room_kw = any(k in lower_msg for k in ROOM_KEYWORDS)
    has_bios_kw = bool(re.search(r"\ba(?:0[2-9]|1[0-4])\b", lower_msg))
    is_model_context = has_model_kw or has_bios_kw
    is_room_context = has_room_kw or "/status" in lower_msg

    # Machine Types Detection (Regex Fallback - Keywords only, counts hard to parsing regex)
    found_types = []
    if "xps" in lower_msg:
        found_types.append("XPS")
    if "optiplex" in lower_msg:
        found_types.append("OPTIPLEX")
    if "hp" in lower_msg:
        found_types.append("HP")
    if "alugada" in lower_msg or "locada" in lower_msg:
        found_types.append("ALUGADA")
    if "lenovo" in lower_msg:
        if "mini" in lower_msg:
            found_types.append("LENOVO_MINI")
        elif "lenovo" not in found_types:
            found_types.append("LENOVO")  # Avoid dupe if mini logic complex, simplified here

    types_str = f"Tipos: {', '.join(found_types)}" if found_types else ""

    # Determine Status
    status = get_status_from_text(lower_msg) or Status.NAO_AVALIADO

    # Process Rooms (Two-Pass Logic)

    # Pre-process message for consistent delimiters
    # 1. Comma separated lists: "719 ,720" -> "719 720" (commas are fine, but spacing helps)
    processed_msg = re.sub(r"(\d)\s*[,]\s*(\d)", r"\1 \2", message)
    # 2. Fix typos like "511e 512" -> "511 e 512" (only if numeric context)
    processed_msg = re.sub(r"(\d)e\s+(\d)", r"\1 e \2", processed_msg)

    matches_sala = REGEX_SALA.findall(processed_msg)
    strong_rooms_found = []
    ambiguous_matches = []

    # 1. Identification Pass
    for m in matches_sala:
        if m in ALWAYS_MODELS:
            continue
        if m in AMBIGUOUS_NUMBERS:
            ambiguous_matches.append(m)
        else:
            # It's a "Strong" room (712, 600, 202)
            strong_rooms_found.append(m)

    # 2. Decision Pass
    # If we found strong rooms (e.g. 712), then any ambiguous number (3020) in the same message
    # is almost certainly the MODEL of that room, not a second room.
    has_strong_room = len(strong_rooms_found) > 0

    # Deduplicate candidates while preserving order (optional, set is enough)
    final_room_candidates = list(set(strong_rooms_found))

    for m in ambiguous_matches:
        # Global Context Check
        if is_model_context and not is_room_context:
            continue  # Strict model context due to keywords

        # Proximity Check
        pattern_proximity = rf"(?:optiplex|dell|modelo|cpu|pc|maquina|desktop)[\s\S]{{0,20}}\b{m}\b"
        if re.search(pattern_proximity, lower_msg):
            continue  # Logic says Model

        # NEW: Strong Room Precedence
        if has_strong_room:
            # "712 3020 OK" -> 712 is strong. 3020 is likely model.
            continue

        # Fallback Logic (Stand-alone ambiguous)
        if is_room_context:
            final_room_candidates.append(m)
        else:
            # Ambiguous stand-alone -> Skip so check_model_reference asks user
            continue

    # 3. Validation & Result Generation
    detected_model = None

    # Check if we found any model-like numbers (either ambiguous ignored above, or in general)
    # Logic: If we found "Strong Rooms", likely any "Ambiguous Number" is the model.
    # We can just re-scan for them.
    for n in AMBIGUOUS_NUMBERS:
        if n in lower_msg:  # Simple scan
            detected_model = f"OptiPlex {n}"
            break
    if not detected_model:
        for n in ALWAYS_MODELS:
            if n in lower_msg:
                detected_model = f"OptiPlex {n}"
                break

    # Also check generic types to set as modelo if specific not found?
    # User Rules say: "3010, 3020... interpretar como MODELO".
    # We prioritize specific number.

    for m in final_room_candidates:
        info = validate_sala(m)
        if info:
            # Smart Segment Extraction (similar to Labs)
            # If message is multi-line, try to isolate the line relevant to this room

            # Normalize single-line reports (delimited by | or ;)
            normalized_msg = re.sub(r"[|;]", "\n", message)

            text_segment = message
            lines = normalized_msg.strip().split("\n")

            if len(lines) > 1:
                relevant_lines = []
                for line in lines:
                    # Check if this line mentions the room number 'm'
                    # But 'm' might be "012" or "727".

                    # Robust check:
                    # 1. "S-727" or "Sala 727" -> Explicit
                    # 2. "727" as standalone word -> \b727\b (Prevents 510 matching 3010)

                    pattern_room = rf"\b(?:S-?|Sala\s*)?{m}\b"
                    if re.search(pattern_room, line, re.IGNORECASE):
                        relevant_lines.append(line)

                if relevant_lines:
                    text_segment = " | ".join(relevant_lines)

            # Recalculate status based on segment ONLY
            # This prevents "712 OK" line affecting "713 ERRO" line if both in same msg
            segment_status = get_status_from_text(text_segment) or Status.NAO_AVALIADO

            # Detect Model in Segment (Overrides global detection if found)
            segment_model = None
            # (Optional: specialized model logic for segment?
            #  Global detected_model might suffice if msg is uniform,
            #  but in bulk list, models might differ per line.
            #  "712 Optiplex 3020\n713 Optiplex 7010")

            # Let's try to extract model from segment first
            for n in AMBIGUOUS_NUMBERS.union(ALWAYS_MODELS):
                if n in text_segment:
                    segment_model = f"OptiPlex {n}"
                    break

            final_model = segment_model if segment_model else detected_model
            final_status = segment_status if segment_status != Status.NAO_AVALIADO else status

            results.append(
                {
                    **info,
                    "tipo_ambiente": TipoAmbiente.SALA,
                    "status": final_status,
                    "modelo": final_model,
                    "observacao": text_segment,
                }
            )

    # Process Labs (Enhanced with Counts)
    matches_lab = REGEX_LAB.findall(message)

    # Clean message for processing (remove extra spaces, normalize newlines)
    re.sub(r"\s+", " ", message.strip()).lower()

    for m in matches_lab:
        val = int(m)
        if 0 <= val <= 29:
            lab_id = f"L-{val:02d}"

            # Extract counts specific to this message context
            # Enhanced Logic for Multi-line Lab Reports:
            # If multiple labs are found, we must try to isolate the text block for EACH lab.
            # But REGEX_LAB is global.
            # Workaround: If message has newlines, split by lines. If a line mentions "Lab X", parse that line.

            # Identify the segment relevant to this lab
            # If the lab match is part of a larger report, we might need windowing.
            # Simple approach: If lines > 1, assume line-based reporting.
            # Identify the segment relevant to this lab
            # If the lab match is part of a larger report, we might need windowing.
            # Simple approach: If lines > 1, assume line-based reporting.

            # NEW: Handle single-line multi-lab reports (delimited by | or ;)
            # "Lab 2 ... | Lab 1 ..."
            # We treat delimiters as newlines for splitting.
            normalized_msg = re.sub(r"[|;]", "\n", message)

            text_segment = lower_msg  # Use lower_msg for general parsing (fallback)
            lines = normalized_msg.strip().split("\n")  # Split by newline AND pipes now

            if len(lines) > 1:
                # Find the line (or lines) that mention this specific lab ID
                # This is heuristic but better than global search for "37 máquinas" which might appear once for all
                relevant_lines = []
                # Also include lines immediately following a lab header line (indented or bulleted)
                capture_mode = False

                for line in lines:
                    line_lower = line.lower()

            if len(lines) > 1:
                # Find the line (or lines) that mention this specific lab ID
                # and are NOT just mentioning the number as a count (e.g. "1 w11")

                relevant_lines = []
                capture_mode = False

                for line in lines:
                    line_lower = line.lower()

                    # Pattern for Lab Header on this line: "Lab 1", "L-01", "Lab 01", "L-1"
                    # Must match boundary or specific format
                    # RegEx: \b(lab\.?|l-)\s*0?1\b
                    header_pattern = rf"\b(?:lab(?:oratori[oa])?\.?\s*|l-)\s*{val:02d}\b|\b(?:lab(?:oratori[oa])?\.?\s*|l-)\s*{val}\b"

                    is_lab_header = bool(re.search(header_pattern, line_lower))

                    # Check for ANY lab header to stop capture
                    is_any_lab_header = bool(
                        re.search(r"\b(?:lab(?:oratori[oa])?\.?\s*|l-)\s*\d+\b", line_lower)
                    )

                    if is_lab_header:
                        capture_mode = True
                        relevant_lines.append(line_lower)
                        continue

                    if capture_mode:
                        # If we see another lab header effectively, we stop
                        if is_any_lab_header and not is_lab_header:
                            capture_mode = False
                        else:
                            relevant_lines.append(line_lower)

                    # If not in capture mode, we skip line.
                    # This avoids "Lab 2 has 1 w11" being picked up by "Lab 1" just because it has "1".

                text_segment = " | ".join(relevant_lines) if relevant_lines else lower_msg

            # Initialize item for this lab
            item = {
                "local_id": lab_id,
                "sala": None,
                "predio": (2 if val >= 20 else 1),  # Assign Predio based on Lab ID
                "andar": None,
                "tipo_ambiente": TipoAmbiente.LAB,
                "status": Status.NAO_AVALIADO,  # Default, will be updated
                "observacao": text_segment,  # FIXED: Use segment, not full message
                "concluidos": 0,
                "pendentes": 0,
                "erros": 0,
                "total_pcs": 0,
            }

            has_counts = False
            total_match = re.search(
                r"(\d+)\s*(?:m[aá]quinas|pcs|computadores)", text_segment, re.IGNORECASE
            )
            if total_match:
                item["total_pcs"] = int(total_match.group(1))
                has_counts = True

            # Extract specific counts (w11/pendentes)
            # Look for number followed by keyword in the segment

            # Quick Regex for counts in segment
            # Adjusted for formats like "1 - win 11", "12 - win 10"
            # (\d+) followed by optional separators/spaces then keyword
            ok_match = re.search(
                r"(\d+)\s*(?:[\-|]\s*)?(?:pcs?)?\s*(?:est[ãa]o)?\s*(?:ok|w11|win\s*11|concluid[oa]s?|feita?s?)",
                text_segment,
                re.IGNORECASE,
            )
            if ok_match:
                item["concluidos"] = int(ok_match.group(1))

            pend_match = re.search(
                r"(\d+)\s*(?:[\-|]\s*)?(?:pcs?)?\s*(?:est[ãa]o)?\s*(?:pendentes?|faltan?do|sem|a fazer|win\s*10)",
                text_segment,
                re.IGNORECASE,
            )
            if pend_match:
                item["pendentes"] = int(pend_match.group(1))
            else:
                # Infer pendentes if total and concluidos are known but pendentes is consistent with difference
                # Example: "13 PCs apenas 1 w11" -> Total 13, Concluidos 1 -> Pendentes 12
                # Only if text doesn't say "0 pendentes" explicitly (which regex handles if "0 pendentes" exists)
                if item["total_pcs"] > 0 and item["concluidos"] > 0:
                    remainder = item["total_pcs"] - item["concluidos"]
                    if remainder > 0:
                        item["pendentes"] = remainder

            erro_match = re.search(
                r"(\d+)\s*(?:[\-|]\s*)?(?:pcs?)?\s*(?:est[ãa]o)?\s*(?:erro|defeito|falha|tela azul|sem espaco|sem espaço)",
                text_segment,
                re.IGNORECASE,
            )
            if erro_match:
                item["erros"] = int(erro_match.group(1))

            if has_counts:
                # Infer status based on counts
                if item.get("pendentes", 0) > 0 or item.get("erros", 0) > 0:
                    item["status"] = Status.PENDENTE
                elif (
                    item.get("concluidos", 0) >= item.get("total_pcs", 0)
                    and item.get("total_pcs", 0) > 0
                ) or (item.get("concluidos", 0) > 0 and item.get("total_pcs", 0) == 0):
                    item["status"] = Status.OK
                else:
                    item["status"] = Status.ATUALIZANDO
            else:
                st = get_status_from_text(text_segment) or Status.NAO_AVALIADO
                if st != Status.NAO_AVALIADO:
                    item["status"] = st.value if hasattr(st, "value") else st
                else:
                    item["status"] = status.value if hasattr(status, "value") else status

            # If types_str exists, append to observation
            if types_str:
                item["observacao"] = f"{message} | {types_str}"

            results.append(item)

    return results


def normalize_status(status_raw: str) -> Status:
    s = status_raw.upper()
    if s in Status.__members__:
        return Status[s]
    # Mapeamentos adicionais se LLM retornar string fora do padrao
    if "OK" in s or "FEITO" in s or "RESOLVIDO" in s:
        return Status.OK
    if "PENDENTE" in s:
        return Status.PENDENTE
    if "ERRO" in s:
        return Status.ERRO
    if "INCOMPATIVEL" in s:
        return Status.INCOMPATIVEL
    if "ATUALIZANDO" in s or "🔄" in s:
        return Status.ATUALIZANDO
    return Status.NAO_AVALIADO
