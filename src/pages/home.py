"""
ROADMAP DE MELHORIAS: 
    - Adicionar validação de insert, se o gasto já foi inserido anteriormente n permitir
    - Deixar em páginas separadas, não tudo no mesmo .py 
    - Adicionar PyDantic para as operações de CRUD
    - Parametrizar as selecoes de categoria, criador/gastador, etc. Ao invés de ser hardcoded vim de um arquivo
"""


from unicodedata import category
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import sys
sys.path.append("src")
from database.connection import get_db, SessionLocal
from database.models import Expense


st.set_page_config(page_title="Gerenciador de Gastos", layout="wide")

#============================
# Insert expenses
#============================
def insert_expenses(data, valor, descricao, categ, categ_grupo, criador):
    """
        This module will add a new expense in the database
    """
    db = SessionLocal()

    try: 
        novo_gasto = Expense(
            data=data,
            value_amount=valor,
            description=descricao,
            category = categ,
            category_group = categ_grupo,
            spender = criador,
            created_at = datetime.now()
        )

        db.add(novo_gasto)
        db.commit()
        st.success("Expense saved successfully")

    except Exception as e:
        db.rollback()
        st.error(f"Error on salving: {str(e)}")
        return False
    
    finally:
        db.close()


#============================
# Delete an expense
#============================
def delete_expense(expense_id):
    """
        Delete and expense from the database
    """
    db = SessionLocal()

    try:
        expense = db.query(Expense).filter(Expense.id == expense_id).first()
        if expense: 
            db.delete(expense)
            db.commit()
            st.success(f"Gasto do id {expense_id} deletado com sucesso!")
            return True        
        else:
            st.warning("Gasto não deletado/encontrado!")
            return False
    
    except Exception as e:
        db.rollback() # if any error, do a rollback on database
        st.error(f"Erro ao tentar deletar: {str(e)}")
        return False
    
    finally:
        db.close()



#============================
# Show expenses
#============================
def get_all_expenses():
    """
        Retriee all expenses from the last 30d from the database
    """
    db = SessionLocal()

    initial_date = datetime.now() - timedelta(days=30)

    expenses_table = db.query(Expense)\
                       .filter(Expense.data >= initial_date)\
                       .order_by(Expense.data.desc())\
                       .all()

    try:
        if expenses_table:
            # Converting to dataframe, each row
            expenses_data = []
            for expense in expenses_table: 
                expenses_data.append({
                    'ID': expense.id,
                    'Data': expense.data.strftime('%Y-%m-%d'),                    
                    'Descrição': expense.description,
                    'Categoria': expense.category,
                    'Grupo Categoria': expense.category_group,
                    'Pagador': expense.spender,
                    'Valor R$': f"R$ {expense.value_amount:.2f}",
                })
            return pd.DataFrame(expenses_data)
        return pd.DataFrame()
    
    except OperationalError as e:
        st.error("Erro de conexão com o banco de dados. Por favor, tente novamente em alguns instantes.")
        st.error(f"Detalhes técnicos: {str(e)}")
        return pd.DataFrame()
            
    except SQLAlchemyError as e:
        st.error("Erro ao consultar o banco de dados.")
        st.error(f"Detalhes técnicos: {str(e)}")
        return pd.DataFrame() 
    
    
    finally:
        db.close()


#============================
# MAIN - Info and display in homepage
#============================
def main():
    st.title("Gerenciador de Gastos Pessoais :moneybag: :money_with_wings:")
    
    # Sidebar para navegação
    menu = st.sidebar.selectbox(
        "Menu",
        ["Adicionar Gasto", "Visualizar Gastos", "Upload CSV", "Relatórios"]
    )
    

    if menu == "Adicionar Gasto":
        with st.form("novo_gasto"):
            col1, col2 = st.columns(2)

            with col1:
                data = st.date_input("Data do gasto")
                valor = st.number_input("Valor do gasto R$", min_value=0.0, format="%.2f")
                descricao = st.text_input("Descricao do gasto")

            with col2:
                categoria = st.selectbox("Selecione a categoria do gasto",
                            ["Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", "Educação", "Outros"])
                categoria_grupo = st.selectbox("Grupo da categoria do gasto",
                                    ["Essencial", "Não essencial"])

                pagador = st.selectbox("Quem gastou", ["Henrique", "Keth"])

            if st.form_submit_button("Salvar gasto"):
                if insert_expenses(data, valor, descricao, categoria, categoria_grupo, pagador):
                    st.success("Gasto resgistrado com sucesso!")

    #================
    # If visualize expenses
    #================
    elif menu == 'Visualizar Gastos':
        st.header("Visualizar e Editar Gastos")

        #Loading all expenses 
        df = get_all_expenses()

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