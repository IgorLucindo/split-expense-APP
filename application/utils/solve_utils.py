import pulp
import numpy as np


def minimize_transactions(payments):
    """
    This function minimizes the number of transactions required to settle debts among a group of people.
    It takes a list of payments (amounts paid by each person) and returns a list of transactions.
    Each transaction specifies who pays whom and the amount.
    """
    balances = [p - np.mean(payments) for p in payments]
    debtors = [(i, -b) for i, b in enumerate(balances) if b < 0]
    creditors = [(i, b) for i, b in enumerate(balances) if b > 0]
    M = max(max((d for _, d in debtors), default=0),
        max((c for _, c in creditors), default=0))

    if not debtors and not creditors:
        return []  # Already settled

    # PuLP model
    prob = pulp.LpProblem("Min_Transactions", pulp.LpMinimize)

    # Variables
    x = {}
    y = {}
    for i, (d, debt) in enumerate(debtors):
        for j, (c, credit) in enumerate(creditors):
            x[(i, j)] = pulp.LpVariable(f"x_{d}_{c}", lowBound=0)
            y[(i, j)] = pulp.LpVariable(f"y_{d}_{c}", cat="Binary")

    # Objective: minimize number of transactions
    prob += pulp.lpSum(y.values())

    # Debt satisfaction
    for i, (_, debt) in enumerate(debtors):
        prob += pulp.lpSum(x[(i, j)] for j in range(len(creditors))) == debt

    # Credit satisfaction
    for j, (_, credit) in enumerate(creditors):
        prob += pulp.lpSum(x[(i, j)] for i in range(len(debtors))) == credit

    # Linking constraint
    for i in range(len(debtors)):
        for j in range(len(creditors)):
            prob += x[(i, j)] <= M * y[(i, j)]

    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    # Extract transactions
    transactions = []
    for d_idx, (d, _) in enumerate(debtors):
        for c_idx, (c, _) in enumerate(creditors):
            amount = pulp.value(x[(d_idx, c_idx)])
            if amount > 1e-6:
                transactions.append({
                    "from": d + 1,  # 1-indexed
                    "to": c + 1,
                    "amount": round(amount, 2)
                })

    return transactions