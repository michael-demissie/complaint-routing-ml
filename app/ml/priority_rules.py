import re

def _count(keywords: list, text: str, weight: int) -> int:
    return sum(weight for kw in keywords if kw in text)

def _amounts(text: str, cap: int) -> int:
    return min(len(re.findall(r"\$[\d,]+", text)), cap)

def _length_score(text: str, high: int, low: int) -> int:
    n = len(text.split())
    if n > high: return 2
    if n > low:  return 1
    return 0

def _persistence(text: str) -> int:
    signals = ["months","years","multiple times","still","ongoing","repeatedly"]
    return sum(1 for kw in signals if kw in text)

def _score_credit_reporting(text: str) -> int:
    s  = _count(["identity theft","fraud","fraudulent","not mine","unauthorized","accounts opened","stolen identity"], text, 4)
    s += _count(["credit score","denied","loan denied","hurting my credit","affecting my score"], text, 2)
    s += _count(["incorrect","inaccurate","duplicate","wrong","misreported","error"], text, 2)
    s += _count(["dispute","no response","not investigated","failed to investigate","30 days","no results","still remains"], text, 2)
    s += _count(["fcra","fair credit reporting","section 609","section 611","violation","law","legal action"], text, 2)
    s += _count(["inquiry","hard pull","unauthorized inquiry"], text, 2)
    s += _amounts(text, 4)
    s += _length_score(text, 250, 120)
    s += _persistence(text)
    return s

def _score_debt_collection(text: str) -> int:
    s  = _count(["lawsuit","court","sued","legal action","summons","wage garnishment","arrest","identity theft","fraud","not mine"], text, 4)
    s += _count(["harass","harassment","calling repeatedly","multiple calls","spam","threatening","abusive","calling my family","calling work"], text, 3)
    s += _count(["dispute","not valid","not my debt","paid already","no proof","validation","verification"], text, 2)
    s += _count(["credit report","credit score","reported","negative","collections account"], text, 2)
    s += _count(["fdcpa","fair debt collection","rights","violation","illegal"], text, 2)
    s += _amounts(text, 4)
    s += _length_score(text, 250, 120)
    s += _persistence(text)
    return s

def _score_card_services(text: str) -> int:
    s  = _count(["unauthorized","fraud","fraudulent","not authorized","did not make","identity theft","hacked","compromised"], text, 4)
    s += _count(["dispute","claim denied","denied","chargeback","investigation","refused","not resolved"], text, 2)
    s += _amounts(text, 5)
    s += _count(["interest","late fee","fee","charged","incorrect charge","overcharged"], text, 2)
    s += _count(["card not received","cannot activate","locked","restricted","closed","blocked"], text, 2)
    s += _count(["not received","never received","package","delivery","merchant","product"], text, 1)
    s += _length_score(text, 250, 120)
    s += _persistence(text)
    return s

def _score_bank_accounts(text: str) -> int:
    s  = _count(["unauthorized","fraud","fraudulent","stolen","identity theft","not mine","hacked","compromised"], text, 3)
    s += _count(["frozen","restricted","locked","cannot access","no access","account closed","closure","terminated relationship"], text, 3)
    s += _count(["reversed","debited","withdrawn","taken","overdraft","fees","charged","deducted"], text, 2)
    s += _amounts(text, 5)
    s += _count(["no response","not resolved","denied","claim denied","ignored","refused","investigation"], text, 2)
    s += _count(["deposit hold","hold","direct deposit","unable to pay","bills","rent"], text, 1)
    s += _length_score(text, 250, 120)
    s += _persistence(text)
    return s

def _score_mortgage(text: str) -> int:
    s  = _count(["foreclosure","foreclosed","eviction","auction","sheriff sale","bankruptcy","legal action","default notice","notice of sale"], text, 4)
    s += _count(["misapplied payment","not applied","incorrect balance","wrong amount","escrow","insurance","taxes","fees","late fee"], text, 2)
    s += _count(["credit report","credit score","negative reporting","delinquent"], text, 2)
    s += _count(["loan modification","modification","forbearance","hardship","covid","loss mitigation"], text, 2)
    s += _count(["no response","not resolved","lost documents","ignored","run around","multiple times","submitted documents"], text, 2)
    s += _amounts(text, 5)
    s += _length_score(text, 250, 120)
    s += _persistence(text)
    return s

def _score_money_transfer(text: str) -> int:
    s  = _count(["fraud","scam","scammed","unauthorized","compromised","hacked","security breach","identity","stolen","fake"], text, 3)
    s += _count(["lost","not received","missing","never received","taken out","withdrawn","chargeback"], text, 3)
    s += _count(["locked","restricted","limited","frozen","deactivated","unable to access","can not access"], text, 2)
    s += _amounts(text, 5)
    s += _count(["no response","not resolved","ignored","refused","could not help","investigation","claim denied"], text, 2)
    s += _count(["urgent","immediately","please help","stress","emotional","need money","rent","business harmed"], text, 1)
    s += _length_score(text, 200, 100)
    return s

def _score_student_loan(text: str) -> int:
    s  = _count(["fraud","forgery","identity","not mine","without consent","illegal","violated","lawsuit","court","forgiveness ordered","bankruptcy"], text, 3)
    s += _count(["credit report","credit score","collections","default","late","negative","garnish","wage"], text, 2)
    s += _count(["wrong","incorrect","misreported","not applied","not updated","error","mistake","changed terms"], text, 2)
    s += _count(["forgiveness","pslf","idr","income driven","deferment","forbearance"], text, 2)
    s += _count(["harassing","calls","calling","threatening","voicemail","stress","litigation"], text, 1)
    s += _count(["cant afford","hardship","struggling","financial","impossible","desperate"], text, 1)
    s += _amounts(text, 4)
    s += _length_score(text, 200, 100)
    s += _count(["multiple times","no response","not resolved","still","ongoing","hours on the phone"], text, 2)
    return s

def _score_consumer_loans(text: str) -> int:
    s  = _count(["fraud","fraudulent","identity","forgery","unauthorized","without consent","repossession","repo","stolen","lawsuit","legal action","violated","rights","15 usc"], text, 3)
    s += _count(["credit report","credit score","negative","collections","balance","owed","charged off"], text, 2)
    s += _amounts(text, 4)
    s += _count(["no response","not resolved","refuse","run around","never","ignored","incorrect","wrong","misreported"], text, 2)
    s += _count(["harassing","calls","calling","threatening","voicemail"], text, 1)
    s += _count(["misled","not disclosed","contract","agreement","terms","lied"], text, 2)
    s += _length_score(text, 200, 100)
    return s

def _score_payday_loans(text: str) -> int:
    s  = _count(["fraud","fraudulent","scam","identity theft","unauthorized","without my consent","illegal","police","attorney","lawsuit","forgery"], text, 3)
    s += _count(["harassment","collections","late fee","incorrect","wrong","denied","misleading","dispute"], text, 2)
    s += _count(["credit report","credit score","repossession","charged","taken from my account","negative report"], text, 3)
    s += _count(["still","continuing","every day","constantly","repeatedly","ongoing"], text, 1)
    s += _count(["called multiple times","no response","they refuse","not resolved","ignored"], text, 2)
    s += _amounts(text, 3)
    s += _length_score(text, 150, 75)
    s += _count(["financial hardship","cant afford","desperate","struggling","hardship"], text, 1)
    return s

DEPT_THRESHOLDS = {
    "credit reporting":        (13, 6),
    "debt collection":         (11, 5),
    "card services":           (12, 6),
    "bank accounts":           (11, 6),
    "mortgage":                (11, 6),
    "money transfer services": (10, 5),
    "student loan":            (10, 5),
    "consumer loans":          (13, 7),
    "payday / personal loans": (9,  5),
}

DEPT_SCORERS = {
    "credit reporting":        _score_credit_reporting,
    "debt collection":         _score_debt_collection,
    "card services":           _score_card_services,
    "bank accounts":           _score_bank_accounts,
    "mortgage":                _score_mortgage,
    "money transfer services": _score_money_transfer,
    "student loan":            _score_student_loan,
    "consumer loans":          _score_consumer_loans,
    "payday / personal loans": _score_payday_loans,
}

def rule_based_priority(text: str, department: str) -> str:
    text = text.lower()
    dept = department.lower()
    scorer = DEPT_SCORERS.get(dept)
    if scorer is None:
        return "standard"
    score = scorer(text)
    critical_thresh, high_thresh = DEPT_THRESHOLDS[dept]
    if score >= critical_thresh:
        return "critical"
    elif score >= high_thresh:
        return "high_priority"
    else:
        return "standard"
