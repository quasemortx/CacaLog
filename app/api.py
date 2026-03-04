from fastapi import APIRouter, Depends, HTTPException, Request

from app.security import require_api_key

router = APIRouter(prefix="/api", dependencies=[Depends(require_api_key)])


def get_sheets_client(request: Request):
    client = getattr(request.app.state, "sheets_client", None)
    if not client:
        raise HTTPException(status_code=503, detail="Sheets connection not available")
    return client


@router.get("/inventory")
def list_inventory(
    request: Request, q: str | None = None, status: str | None = None, setor: str | None = None
):
    client = get_sheets_client(request)
    records = client.get_all_records()

    results = []
    for r in records:
        if q:
            searchable = f"{r.get('local_id', '')} {r.get('Sala', '')} {r.get('Modelo', '')} {r.get('Observacao', '')} {r.get('Setor', '')}".lower()
            if q.lower() not in searchable:
                continue
        if status and r.get("Status", "").lower() != status.lower():
            continue
        if setor and r.get("Setor", "").lower() != setor.lower():
            continue

        results.append(r)

    return {"items": results, "total": len(results)}


@router.get("/history")
def list_history(request: Request, q: str | None = None, local_id: str | None = None):
    client = get_sheets_client(request)
    records = client.get_all_history()

    results = []
    for r in records:
        if q:
            searchable = f"{r.get('local_id', '')} {r.get('observacao', '')} {r.get('responsavel', '')} {r.get('mensagem_original', '')}".lower()
            if q.lower() not in searchable:
                continue
        if local_id and r.get("local_id", "").lower() != local_id.lower():
            continue

        results.append(r)

    return {"items": results, "total": len(results)}


@router.get("/stats")
def get_stats(request: Request):
    client = get_sheets_client(request)
    records = client.get_all_records()

    by_status = {}
    by_setor = {}

    for r in records:
        st = r.get("Status", "NÃO AVALIADO")
        if not st:
            st = "NÃO AVALIADO"
        by_status[st] = by_status.get(st, 0) + 1

        setor_val = r.get("Setor", "Sem Setor")
        if not setor_val:
            setor_val = "Sem Setor"
        by_setor[setor_val] = by_setor.get(setor_val, 0) + 1

    return {"total": len(records), "by_status": by_status, "by_setor": by_setor}
