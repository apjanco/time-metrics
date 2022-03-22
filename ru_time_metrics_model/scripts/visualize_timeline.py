import typer
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import datetime



def main():
    @st.cache(allow_output_mutation=True)
    def get_data():
        return pd.read_csv("corpus/timeline_output.csv")


    df = get_data()
    start_date = st.sidebar.date_input('start date', datetime.date(1800,1,1))
    end_date = st.sidebar.date_input('end date', datetime.date(2018,1,1))
    empire_threshold = st.sidebar.slider('empire threshold',value=0.9, min_value=0.0, max_value=1.0)
    soviet_threshold = st.sidebar.slider('soviet threshold',value=0.9, min_value=0.0, max_value=1.0)
    post_threshold = st.sidebar.slider('post threshold',value=0.9, min_value=0.0, max_value=1.0)
    
    
    
    #author = st.sidebar.multiselect('author', df['author'].unique())
    #diary = st.sidebar.multiselect('diary', df['diary'].unique())
    df['date']= pd.to_datetime(df['date'], format="%Y-%m-%d", errors = 'coerce')
    df = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]

    #if author:
    #    df = df[df['author'].isin(author)]
    #if diary:
    #    df = df[df['diary'].isin(diary)]
    df['empire'] = df['empire'].apply(lambda x: x if x >= empire_threshold else None)
    df['soviet'] = df['soviet'].apply(lambda x: x if x >= soviet_threshold else None)
    df['post'] = df['post'].apply(lambda x: x if x >= post_threshold else None)
    

    fig = px.scatter(
        df, 
        x="date", 
        y=df.columns[4:], 
        
        
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Predictions",
    )

    st.write(fig)
    

if __name__ == "__main__":
    try:
        typer.run(main)
    except SystemExit:
        pass
