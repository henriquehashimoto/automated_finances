"""
ROADMAP DE MELHORIAS: 
    - Adicionar validação de insert, se o gasto já foi inserido anteriormente n permitir
    - Deixar em páginas separadas, não tudo no mesmo .py 
    - Adicionar PyDantic para as operações de CRUD
    - Parametrizar as selecoes de categoria, criador/gastador, etc. Ao invés de ser hardcoded vim de um arquivo
"""


from unicodedata import category
from datetime import datetime, timedelta
from numpy import integer
import streamlit as st
import pandas as pd
import sys

from traitlets import default
sys.path.append("src")
from database.connection import get_db, SessionLocal
from database.models import Expense
from crud_ops_aux import insert_expenses, delete_expense, get_all_expenses


st.set_page_config(page_title="Gerenciador de Gastos", layout="wide")


#============================
# MAIN - Info and display in homepage
#============================
def main():
    st.title("Gerenciador de Gastos Pessoais :moneybag: :money_with_wings:")
    
    # Sidebar para navegação
    menu = st.sidebar.selectbox(
        "Menu",
        ["Adicionar Gasto", "Editar Gastos", "Upload CSV"]
    )
    

    if menu == "Adicionar Gasto":
        with st.form("novo_gasto"):
            col1, col2 = st.columns(2)

            with col1:
                data = st.date_input("Data do gasto")
                valor = st.number_input("Valor do gasto ou da parcela R$", min_value=0.0, format="%.2f")
                descricao = st.text_input("Descricao do gasto")

            with col2:
                categoria = st.selectbox("Selecione a categoria do gasto",
                            ["Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", "Educação", "Outros"])
                categoria_grupo = st.selectbox("Grupo da categoria do gasto",
                                    ["Essencial", "Não essencial"])

                pagador = st.selectbox("Quem gastou", ["Henrique", "Keth"])                                
                recorrencia = st.checkbox("Gasto é recorrente / parcelado?")

                # If the recurrency is checked then it'll activate the option to pass how many installments
                qt_parcelas = 0
                # if st.session_state.show_parcelas:
                qt_parcelas = st.number_input("Quantas parcelas são? Coloque 100 se for recorrente mensal",step=1,min_value=0)


            if st.form_submit_button("Salvar gasto"):
                insert_expenses(data, valor, descricao, categoria, categoria_grupo, pagador, recorrencia, qt_parcelas)
                

    #================
    # If visualize expenses
    #================
    elif menu == 'Editar Gastos':
        st.header("Visualizar e Editar Gastos")
        
        # Input dates to visualize the expenses
        col1, col2 = st.columns(2)

        start_default = datetime.now() - timedelta(days=30)
        start_date = col1.date_input("Selecione data inicial", start_default)
        end_date = col2.date_input ("Selecione data final", datetime.now())


        #Loading all expenses 
        df = get_all_expenses(start_date, end_date)

        if not df.empty:
            st.dataframe(df)

            # Delete expenses if needed
            with st.expander("🗑️ Deletar Gastos"):
                expense_ids = df["ID"].tolist()
                selected_id = st.selectbox("Selecione o ID do gasto para deletar", expense_ids)

                if st.button("Deletar Gasto", type="primary"):
                    if delete_expense(selected_id):
                        # Rerun page after deleted
                        st.rerun()
        
        else:
            st.info("Nenhum gasto registrado/encontrado!")



if __name__ == "__main__":
    main()