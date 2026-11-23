from stockbridge import demo_data
from stockbridge.agent import RouteAgent
from stockbridge.planner import plan


def fresh():
    twin = demo_data.build()
    return twin, RouteAgent(twin)


def test_plan_respects_budget_and_capacity():
    twin, _ = fresh()
    moves, refusals = plan(twin)
    spend = {}
    for m in moves:
        spend[m.to_shop] = spend.get(m.to_shop, 0) + m.qty * m.unit_price
        sell_days = m.days_to_expiry - twin.policy.lead_days
        assert m.qty <= twin.extra_capacity(m.to_shop, m.item_id, sell_days)
    for sid, s in spend.items():
        assert s <= twin.shops[sid].budget_left


def test_short_dated_stock_is_refused_not_moved():
    twin, agent = fresh()
    agent.run_cycle()
    claims = [d for d in agent.documents if d["type"] == "brand_claim"]
    assert claims, "bread with 2 days left should become a brand claim"
    assert all(m.item_id != "bread_400" for m in agent.moves)


def test_receivers_never_see_giver_sales():
    twin, agent = fresh()
    reqs = agent.run_cycle()
    for r in reqs:
        if r.kind == "take":
            giver = twin.shops[agent.moves[r.move_index].from_shop].name
            assert giver not in r.message


def test_decline_is_remembered_and_replanned():
    twin, agent = fresh()
    reqs = agent.run_cycle()
    take = next(r for r in reqs if r.kind == "take")
    for r in reqs:
        agent.respond(r.id, 0 if r.id == take.id else r.qty)
    assert (take.shop_id, take.item_id) in agent.declined
    assert agent.round >= 2
    later = [r for r in agent.requests.values() if r.round > 1 and r.kind == "take"]
    assert all((r.shop_id, r.item_id) != (take.shop_id, take.item_id) for r in later)


def test_giver_not_asked_twice_after_partial():
    twin, agent = fresh()
    reqs = agent.run_cycle()
    # find a lot with a take; accept the give fully, take partially
    take = next(r for r in reqs if r.kind == "take" and r.qty > 1)
    for r in reqs:
        agent.respond(r.id, r.qty // 2 if r.id == take.id else r.qty)
    later_gives = [r for r in agent.requests.values() if r.round > 1 and r.kind == "give" and r.lot_id == take.lot_id]
    assert all(r.status == "accepted" for r in later_gives)  # auto-accepted from memory, never pending


def test_committed_moves_produce_documents_and_route():
    twin, agent = fresh()
    agent.run_cycle()
    agent.auto_answer(lambda r: r.qty)
    assert agent.committed
    types = {d["type"] for d in agent.documents}
    assert "credit_note" in types and "invoice" in types
    assert agent.route()[0]["action"] == "pick up"


def test_stock_is_conserved():
    twin, agent = fresh()
    before = sum(l.qty for l in twin.lots)
    agent.run_cycle()
    agent.auto_answer(lambda r: r.qty)
    assert sum(l.qty for l in twin.lots) == before
