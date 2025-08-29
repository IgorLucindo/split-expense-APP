# 💰 Expense Splitter

A simple web app that helps groups split expenses **fairly** and **minimize the number of transactions**.  
Built with **Flask (Python)** for the backend and **HTML/CSS/JS** for the frontend.  

The app takes the total payments made by each person, calculates who owes whom, and outputs the minimal set of transactions needed to settle the debts.

---

## ✨ Features
- Enter the number of people and their payments.
- Automatically compute who should pay whom.
- Minimizes the number of transactions using **Mixed Integer Programming (MIP)**.
- Clean and responsive interface.

---

## 🙏 Credits
- The optimization formulation is based on the work of **Dr. Validi**.  
- GitHub repo: [Dr.Validi’s repository](https://github.com/Validi)  

---

## 🚀 Execution

### Local setup
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/expense-splitter.git
   cd expense-splitter