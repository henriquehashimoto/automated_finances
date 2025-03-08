# Automated Finances

Automated Finances

System for personal expense management using Streamlit and Neon (PostgreSQL).


## Functionalities
- Manual expense input
- Expense upload via CSV
- Editing and removal of expenses
- Data visualization and reports
- Expense categorization
- Marking of essential/non-essential expenses

## Technologies
- Python
- Streamlit (Frontend)
- PostgreSQL/Neon (Database)
- SQLAlchemy (ORM)
- Pandas (Data manipulation)
- Plotly (Visualizations)
- PyDantic and Pytest (data quality and validation)


## Project Structure

automated_finances/
├── src/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── connection.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── expense_service.py
│   └── pages/
│       ├── __init__.py
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

[ ] CRUD of expenses
[ ] CSV upload
[ ] Category reports
[ ] Monthly evolution graphs
[ ] Period filters
[ ] Export data