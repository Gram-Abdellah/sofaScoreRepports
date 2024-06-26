import pandas as pd
import plotly.express as px
import streamlit as st

def load_data():
    return pd.read_csv('reports/team_stats_latest.csv')

def main():
    st.title("Soccer Team Reports Dashboard")

    df = load_data()
    st.dataframe(df)

    fig = px.bar(df, x='team', y='goalsScored', title='Goals Scored by Team')
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
