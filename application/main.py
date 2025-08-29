from utils.solve_utils import *


def main():
    payments = [-15.0, 130.0, -125.0, 150.0, 20.0, -160.0]

    transactions = minimize_transactions(payments)
    print(transactions)


if __name__ == "__main__":
    main()