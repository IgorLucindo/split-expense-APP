import pulp

def minimize_transactions(num_people, payments):
    total = sum(payments)
    average = total / num_people
    nets = [p - average for p in payments]

    # Separate debtors and creditors
    debtors = [(i, -net) for i, net in enumerate(nets) if net < 0]
    creditors = [(i, net) for i, net in enumerate(nets) if net > 0]

    if not debtors and not creditors:
        return []  # Already settled

    # PuLP model to minimize number of payments
    prob = pulp.LpProblem("Min_Transactions", pulp.LpMinimize)

    # Variables
    x = {}
    y = {}
    for d_idx, (d, debt) in enumerate(debtors):
        for c_idx, (c, credit) in enumerate(creditors):
            x[(d_idx, c_idx)] = pulp.LpVariable(f"x_{d}_{c}", lowBound=0)
            y[(d_idx, c_idx)] = pulp.LpVariable(f"y_{d}_{c}", cat=pulp.LpBinary)

    # Objective: minimize number of transactions
    prob += pulp.lpSum(y.values())

    # Constraints
    for d_idx, (d, debt) in enumerate(debtors):
        prob += pulp.lpSum(x[(d_idx, c_idx)] for c_idx in range(len(creditors))) == debt
    for c_idx, (c, credit) in enumerate(creditors):
        prob += pulp.lpSum(x[(d_idx, c_idx)] for d_idx in range(len(debtors))) == credit

    # Link x and y
    M = max(total, 1)
    for d_idx in range(len(debtors)):
        for c_idx in range(len(creditors)):
            prob += x[(d_idx, c_idx)] <= M * y[(d_idx, c_idx)]

    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    # Extract results
    transactions = []
    for d_idx, (d, debt) in enumerate(debtors):
        for c_idx, (c, credit) in enumerate(creditors):
            amount = pulp.value(x[(d_idx, c_idx)])
            if amount > 1e-6:
                transactions.append({
                    "from": d + 1,  # 1-indexed
                    "to": c + 1,
                    "amount": round(amount, 2),
                })

    return transactions