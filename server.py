"""Stockbridge demo server: shop app, distributor dashboard and delivery route in one page.

Run:  uvicorn server:app --reload   then open http://localhost:8000
"""
from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from stockbridge import capture, checksum, demo_data, llm
from stockbridge.agent import RouteAgent, day_str
from stockbridge.catalogue import BY_ID

app = FastAPI(title="Stockbridge")
UI = Path(__file__).parent / "ui" / "index.html"

STATE: dict = {}


def reset() -> None:
    twin = demo_data.build()
    STATE.update(twin=twin, agent=RouteAgent(twin), pending_sales={}, bills=[])


reset()


@app.get("/")
def index() -> FileResponse:
    return FileResponse(UI)


@app.get("/api/state")
def state() -> dict:
    twin, agent = STATE["twin"], STATE["agent"]
    snap = twin.snapshot()
    for r in snap["at_risk"]:
        r["item"] = BY_ID[r["item_id"]].label
        r["shop"] = twin.shops[r["shop_id"]].name
        r["expiry"] = day_str(twin.today + r["days_to_expiry"])
    stock = [{"item_id": i, "item": BY_ID[i].label, "qty": twin.stock("sharma", i),
              "cover": None if twin.rate("sharma", i) == 0 else round(twin.days_of_cover("sharma", i), 1)}
             for i in sorted({l.item_id for l in twin.lots if l.shop_id == "sharma"})]
    return {**snap, "agent": agent.state(), "bills": STATE["bills"][-8:], "sharma_stock": stock,
            "llm": llm.available(), "samples": demo_data.SAMPLE_SALES,
            "whatif": {"no_action_30d": twin.simulate_expiry(30)}}


class Sale(BaseModel):
    transcript: str
    amount: int | None = None
    shop_id: str = "sharma"


@app.post("/api/sale")
def sale(s: Sale) -> dict:
    lines, parser = capture.parse(s.transcript)
    res = checksum.reconcile(lines, s.amount)
    sid = uuid.uuid4().hex[:8]
    STATE["pending_sales"][sid] = {"lines": lines, "amount": s.amount, "shop_id": s.shop_id, "transcript": s.transcript}
    out = {"sale_id": sid, "parser": parser, "lines": [ln.to_dict() for ln in lines], **res.to_dict()}
    if res.status == "match":
        out["saved"] = _save(sid, res.bill)
    return out


class Answer(BaseModel):
    sale_id: str
    line: int | None = None
    item_id: str | None = None
    confirm: bool = False


@app.post("/api/sale/answer")
def sale_answer(a: Answer) -> dict:
    p = STATE["pending_sales"].get(a.sale_id)
    if not p:
        raise HTTPException(404, "unknown sale")
    lines = p["lines"]
    if a.item_id is not None and a.line is not None:
        lines = checksum.apply_answer(lines, a.line, a.item_id)
        p["lines"] = lines
    res = checksum.reconcile(lines, p["amount"])
    out = {"sale_id": a.sale_id, "lines": [ln.to_dict() for ln in lines], **res.to_dict()}
    if res.status == "match" or (res.status == "cash_confirm" and a.confirm):
        out["saved"] = _save(a.sale_id, res.bill)
    return out


def _save(sid: str, bill: list[dict]) -> dict:
    p = STATE["pending_sales"].pop(sid)
    twin = STATE["twin"]
    for b in bill:
        twin.record_sale(p["shop_id"], b["item_id"], b["qty"])
    rec = {"sale_id": sid, "transcript": p["transcript"], "amount": p["amount"], "bill": bill,
           "total": sum(b["price"] * b["qty"] for b in bill)}
    STATE["bills"].append(rec)
    return rec


@app.post("/api/agent/cycle")
def cycle() -> dict:
    STATE["agent"].run_cycle()
    return state()


class Reply(BaseModel):
    request_id: str
    accept_qty: int


@app.post("/api/agent/respond")
def respond(r: Reply) -> dict:
    STATE["agent"].respond(r.request_id, r.accept_qty)
    return state()


class WhatIf(BaseModel):
    days: int = 30
    demand_multiplier: float = 1.0


@app.post("/api/whatif")
def whatif(w: WhatIf) -> dict:
    return STATE["twin"].simulate_expiry(w.days, w.demand_multiplier)


@app.post("/api/reset")
def do_reset() -> dict:
    reset()
    return state()
