import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html


df = pd.read_csv('my_expenses_clean.csv')
df['Started Date'] = pd.to_datetime(df['Started Date'])
df['Month'] = df['Started Date'].dt.month
df['Year'] = df['Started Date'].dt.year
df['DayOfWeek'] = df['Started Date'].dt.day_name()



exclude = ['Transfer', 'Currency Exchange', 'Sent money', 'Sent Money']
df_clean = df[~df['Category'].isin(exclude)]

category_fig = px.bar(
    df_clean.groupby('Category')['Amount'].sum().reset_index().sort_values('Amount', ascending=False),
    x='Amount', y='Category', orientation='h',
    title='Total Spending by Category (2021-2024)',
    color='Amount', color_continuous_scale='viridis',
    height=600
)


monthly = df.groupby(['Year', 'Month'])['Amount'].sum().reset_index()
monthly['Date'] = pd.to_datetime(monthly[['Year', 'Month']].assign(day=1))
trend_fig = px.line(
    monthly, x='Date', y='Amount', markers=True,
    title='Monthly Spending Trend'
)


yearly_fig = px.bar(
    df.groupby('Year')['Amount'].sum().reset_index(),
    x='Year', y='Amount',
    title='Total Spending Per Year',
    color='Year', color_continuous_scale='blues'
)


category_year_fig = px.bar(
    df.groupby(['Year', 'Category'])['Amount'].sum().reset_index(),
    x='Year', y='Amount', color='Category',
    title='Spending by Category Per Year', barmode='stack'
)


total_spent = df['Amount'].sum()
avg_transaction = df['Amount'].mean()
top_category = df.groupby('Category')['Amount'].sum().idxmax()
total_transactions = len(df)


app = Dash(__name__)

app.layout = html.Div([
    html.H1('My Personal Finance Dashboard',
            style={'textAlign': 'center', 'fontFamily': 'Arial', 'color': '#2c3e50'}),
    html.P('Spending analysis — 2021-2025',
           style={'textAlign': 'center', 'color': 'gray', 'fontFamily': 'Arial'}),

   
    html.Div([
        html.Div([html.H3(f'HUF {total_spent:,.0f}'), html.P('Total Spent')],
                 style={'textAlign':'center', 'background':'#3498db', 'color':'white',
                        'padding':'20px', 'borderRadius':'10px', 'flex':'1', 'margin':'10px'}),
        html.Div([html.H3(f'HUF {avg_transaction:,.0f}'), html.P('Avg Transaction')],
                 style={'textAlign':'center', 'background':'#2ecc71', 'color':'white',
                        'padding':'20px', 'borderRadius':'10px', 'flex':'1', 'margin':'10px'}),
        html.Div([html.H3(f'{total_transactions}'), html.P('Total Transactions')],
                 style={'textAlign':'center', 'background':'#e74c3c', 'color':'white',
                        'padding':'20px', 'borderRadius':'10px', 'flex':'1', 'margin':'10px'}),
        html.Div([html.H3(f'{top_category}'), html.P('Top Category')],
                 style={'textAlign':'center', 'background':'#9b59b6', 'color':'white',
                        'padding':'20px', 'borderRadius':'10px', 'flex':'1', 'margin':'10px'}),
    ], style={'display':'flex', 'justifyContent':'center', 'margin':'20px'}),

    dcc.Graph(figure=trend_fig),
    dcc.Graph(figure=category_fig),
    dcc.Graph(figure=yearly_fig),
    dcc.Graph(figure=category_year_fig),
])

server = app.server  

if __name__ == '__main__':
    app.run(debug=True)