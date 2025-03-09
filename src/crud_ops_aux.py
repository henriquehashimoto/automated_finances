from unicodedata import category
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import sys
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy import and_
sys.path.append("src")
from database.connection import get_db, SessionLocal
from database.models import Expense


#============================
# Insert expenses
#============================
def insert_expenses(data, valor, descricao, categ, categ_grupo, criador, recorrencia, qt_parcelas):
    """
        This module will add a new expense in the database
    """
    db = SessionLocal()

    try: 
        # Verify if expense already included
        verify_exist_expense = db.query(Expense).filter(and_(
            Expense.data == data,
            Expense.value_amount == valor,
            Expense.description == descricao,
            Expense.category == categ,
            Expense.spender == criador
        )).first()

        if verify_exist_expense:
            st.warning(":warning: Este gasto já foi adicionado anteriormente :warning:")
            return False

        novo_gasto = Expense(
            data=data,
            value_amount=valor,
            description=descricao,
            category = categ,
            category_group = categ_grupo,
            spender = criador,
            created_at = datetime.now(),
            is_recurrent = recorrencia,
            installment_amounts = qt_parcelas
        )

        db.add(novo_gasto)

        #--------------
        # Add installments in the next months
        #--------------
        if qt_parcelas > 1:
            current_date = data
            for i in range(1, qt_parcelas):
                next_month = current_date.replace(day=28) + timedelta(days=4)
                next_month = next_month.replace(day=1)
                db.add(Expense(
                        data = next_month,
                        value_amount = valor,
                        description = descricao,
                        category = categ,
                        category_group = categ_grupo,
                        spender = criador,
                        created_at = datetime.now(),
                        is_recurrent = recorrencia,
                        installment_amounts = qt_parcelas
                ))
                current_date = next_month
            

        db.commit()
        st.success(f"Gasto {'parcelado' if qt_parcelas > 1 else ''} registrado com sucesso!")
        return True

    except Exception as e:
        db.rollback()
        st.error(f"Error on salving: {str(e)}")
        return False
    
    #--------------
    # If is the first expense in the month, it'll add the recurrent expenses
    #--------------
    

    finally:
        db.close()


#============================
# Delete an expense
#============================
def delete_expense(expense_id):
    """
        Delete and expense from the database
    
    ADICIONAR
        - Exibir o gasto que foi selecionado para deletar 
        - Ao clicar perguntar se tem certeza
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
def get_all_expenses(start_date, end_date):
    """
    Retrieve expenses within a date range from the database
    
    Args:
        start_date: datetime.date object for the start of the range
        end_date: datetime.date object for the end of the range
    """
    db = SessionLocal()
    

    try:
        # Convert date to datetime for proper comparison
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        expenses_table = db.query(Expense)\
                         .filter(Expense.data.between(start_datetime, end_datetime))\
                         .order_by(Expense.data.desc())\
                         .all()

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
                    'Gasto recorrente?': 'Sim' if expense.is_recurrent else 'Nao',
                    'Quantidades de Parcelas': expense.installment_amounts,
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