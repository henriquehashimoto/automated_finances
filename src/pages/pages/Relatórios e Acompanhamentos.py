import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from sqlalchemy.exc import OperationalError, SQLAlchemyError
sys.path.append("src")
from database.connection import SessionLocal
from database.models import Expense

st.set_page_config(page_title="Acompanhar Gastos", layout="wide")

def get_expenses_by_date_range(start_date, end_date):
    """Busca gastos em um intervalo de datas usando o padrão correto do SQLAlchemy"""
    db = SessionLocal()
    try:
        # Converter date para datetime
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        expenses = db.query(Expense)\
                    .filter(Expense.data.between(start_datetime, end_datetime))\
                    .order_by(Expense.data.desc())\
                    .all()
        
        if not expenses:
            return pd.DataFrame()
        
        expenses_data = [{
            'Data': expense.data.strftime('%d/%m/%Y'),  # Formato BR
            'Valor': expense.value_amount,
            'Descrição': expense.description,
            'Categoria': expense.category,
            'Grupo': expense.category_group,
            'Pagador': expense.spender
        } for expense in expenses]
        
        return pd.DataFrame(expenses_data)
    
    except OperationalError as e:
        st.error("Erro de conexão com o banco de dados. Por favor, tente novamente em alguns instantes.")
        return pd.DataFrame()
    
    except SQLAlchemyError as e:
        st.error("Erro ao consultar o banco de dados.")
        return pd.DataFrame()
    
    finally:
        db.close()

def plot_expenses_by_category(df):
    """Gráfico de gastos por categoria"""
    category_sum = df.groupby('Categoria')['Valor'].sum().reset_index()
    fig = px.pie(
        category_sum,
        values='Valor',
        names='Categoria',
        title='Distribuição de Gastos por Categoria',
        hole=0.4
    )
    return fig

def plot_expenses_timeline(df):
    """Gráfico de linha temporal dos gastos"""
    daily_expenses = df.groupby('Data')['Valor'].sum().reset_index()
    fig = px.line(
        daily_expenses,
        x='Data',
        y='Valor',
        title='Evolução dos Gastos ao Longo do Tempo'
    )
    return fig

def plot_expenses_by_group(df):
    """Gráfico de barras por grupo de categoria"""
    group_sum = df.groupby(['Grupo', 'Categoria'])['Valor'].sum().reset_index()
    fig = px.bar(
        group_sum,
        x='Grupo',
        y='Valor',
        color='Categoria',
        title='Gastos por Grupo e Categoria',
        barmode='group'
    )
    return fig

def main():
    st.title("Acompanhar gastos :chart_with_upwards_trend: :bar_chart:")
    
    # Seletor de período
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Data Inicial",
            value=datetime.now() - timedelta(days=30)
        )
    with col2:
        end_date = st.date_input(
            "Data Final",
            value=datetime.now()
        )
    
    # Buscar dados
    df = get_expenses_by_date_range(start_date, end_date)
    
    if not df.empty:
        # Métricas principais
        total_gasto = df['Valor'].sum()
        media_diaria = total_gasto / (end_date - start_date).days
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Gasto", f"R$ {total_gasto:.2f}")
        with col2:
            st.metric("Média Diária", f"R$ {media_diaria:.2f}")
        with col3:
            st.metric("Número de Gastos", len(df))
        
        # Visualizações
        tab1, tab2, tab3 = st.tabs(["Categorias", "Timeline", "Grupos"])
        
        with tab1:
            st.plotly_chart(plot_expenses_by_category(df), use_container_width=True)
            
            # Tabela detalhada por categoria
            category_details = df.groupby('Categoria').agg({
                'Valor': ['sum', 'mean', 'count']
            }).round(2)
            category_details.columns = ['Total', 'Média', 'Quantidade']
            st.dataframe(category_details)
        
        with tab2:
            st.plotly_chart(plot_expenses_timeline(df), use_container_width=True)
        
        with tab3:
            st.plotly_chart(plot_expenses_by_group(df), use_container_width=True)
            
            # Tabela detalhada por grupo
            group_details = df.groupby('Grupo').agg({
                'Valor': ['sum', 'mean', 'count']
            }).round(2)
            group_details.columns = ['Total', 'Média', 'Quantidade']
            st.dataframe(group_details)
    
    else:
        st.info("Nenhum gasto encontrado no período selecionado.")

if __name__ == "__main__":
    main()