from unicodedata import category
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import sys
sys.path.append("src")
from database.connection import get_db, SessionLocal
from database.models import Expense
from crud_ops_aux import insert_expenses, delete_expense, get_all_expenses



db = SessionLocal()
expenses_table = db.query(Expense).filter(Expense.id >= 1).all()

if expenses_table:
    # Converting to dataframe, each row
    expenses_data = []
    for expense in expenses_table: 
        expenses_data.append({
            'ID': expense.id,
            'Data': expense.data.strftime('%d/%m/%Y'),  # Formato BR                    
            'Descrição': expense.description,
            'Categoria': expense.category,
            'Grupo Categoria': expense.category_group,
            'Pagador': expense.spender,
            'Valor R$': f"R$ {expense.value_amount:.2f}",
        })
    df = pd.DataFrame(expenses_data)

print(df)