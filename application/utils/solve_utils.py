import pulp
import numpy as np


def minimize_transactions(payments):
    M = sum(abs(p) for p in payments)

    # Separate debtors and creditors
    debtors = [(i, -p+np.mean(payments)) for i, p in enumerate(payments) if p < 0]
    creditors = [(i, p-np.mean(payments)) for i, p in enumerate(payments) if p > 0]

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