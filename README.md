# Automated Finances

Automated Finances

System for personal expense management using Streamlit and Neon (PostgreSQL).


# Functionalities

### Expenses input and managament 
- [x] Manual expense input
  - [x] Add new expense
  - [x] Add new expense by installments (or if is recurrent e.g. Facilities bills, internet, etc)
  - [ ] Iterate to not use form
  - [ ] Iterate to add informations as paramenters in variables. Eg.: Expense category, expenser, etc. Instead of hard code
- [] Delete of exepenses 
  - [x] Simple delete 
  - [ ] Message confirm deletion
- [ ] Editing of expenses
  - [ ] Edit installments and recurrency separetelly 
- [ ] Expense upload via CSV

### Incomes
- Add income and income type (salary, bonus, 13º, vacations, etc)

### Goals and savings
- How much we spare for each category each month
- How much we expect to spend on each month for each category 


### Data visualization and reports

**Current Month Report**
A MTD vision on how things are going

- Expense categorization
- Marking of essential/non-essential expenses
- Track on how much we are expending in recurrent expenses (such as streaming and subscriptions)
- MTD Real spend vs Month expectations 

**Historical comparison**

- A track on the historical spendings and savings for each category, group category, expense type, etc



---

# Technologies
- Python as base 
- Streamlit (Frontend)
- PostgreSQL/Neon (Database)
- SQLAlchemy (ORM) for CRUD
- Pandas (Data manipulation)
- Plotly (Visualizations)
- PyDantic and Pytest (data quality and validation)

--- 

## Project Structure

automated_finances/ 
├── src/ 
│   ├── database/ 
│   │   ├── init.py
│   │   ├── models.py
│   │   └── connection.py
│   ├── services/
│   │   ├── init.py
│   │   └── expense_service.py
│   └── pages/
│       ├── init.py
│       ├── home.py
│       ├── expenses.py
│       └── reports.py
├── data/
│   └── sample_data.csv
├── tests/
└── config/
    └── config.py


## Configuration
1. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```
NEON_DB_URL=sua_url_do_neon
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:
```bash
streamlit run src/pages/home.py
```

---

# Development

## Roadmap

[ ] CRUD of expenses with all functionalities 

[ ] CSV upload

[ ] Category reports

[ ] Monthly evolution graphs

[ ] Period filters

[ ] Export data