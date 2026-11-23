from stockbridge import capture, checksum


def parse(t):
    return capture.parse(t, use_llm=False)[0]


def test_number_words_and_items():
    lines = parse("bhaiya teen parle g ek surf dena")
    got = {tuple(l.candidates): l.qty for l in lines}
    assert len(lines) == 2
    assert any(q == 3 for q in got.values()) and any(q == 1 for q in got.values())


def test_multiword_alias_counts_once():
    lines = parse("ek dairy milk chocolate")
    assert len(lines) == 1 and lines[0].qty == 1


def test_amount_resolves_pack_size():
    res = checksum.reconcile(parse("bhaiya teen parle g ek surf dena"), 50)
    assert res.status == "match"
    assert sum(b["price"] * b["qty"] for b in res.bill) == 50


def test_ambiguous_amount_asks_one_question():
    res = checksum.reconcile(parse("ek good day ek surf de do"), 30)
    assert res.status == "ask"
    assert len(res.question["options"]) >= 2


def test_answer_then_match():
    lines = parse("ek good day ek surf de do")
    res = checksum.reconcile(lines, 30)
    q = res.question
    pick = q["options"][0]["item_id"]
    res2 = checksum.reconcile(checksum.apply_answer(lines, q["line"], pick), 30)
    assert res2.status == "match"


def test_mismatch_never_saves():
    res = checksum.reconcile(parse("do maggi aur ek lays"), 999)
    assert res.status == "mismatch"


def test_cash_needs_confirmation():
    res = checksum.reconcile(parse("tata namak ek packet"), None)
    assert res.status == "cash_confirm"


def test_nothing_heard():
    assert checksum.reconcile(parse("haan ji kitne hue"), 20).status == "empty"
