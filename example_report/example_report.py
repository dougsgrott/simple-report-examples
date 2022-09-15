"""

"""

#%%
from pathlib import Path
import sys

# path = "/home/user/PythonProj/simple-report/simple_report/"
# sys.path.insert(0, path)
# path = "/home/user/PythonProj/simple-report/"
# sys.path.insert(0, path)

import datetime
from turtle import color
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import simple_report as sr

# from altair.vegalite.v4.api import Chart

#%%

# ########################################################
# Demonstrations
# ########################################################

# def create_example_report_demo():
current_time = datetime.datetime.now()
current_time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
report_directory = f"report_{current_time_str}"

page_names = ['Description', 'Text', 'Table', 'Matplotlib', 'Plotly', 'Altair', 'Collapse', 'Modal', 'Tabs', 'Alerts', 'Cards']
report_title = 'My report'

html = sr.HtmlReport(
    report_title=report_title,
    project_name='FinanceReport',
    # author='Douglas Macedo Sgrott',
    pages=page_names,
    background_color='#f47d30'
    )

html.add(sr.H1('Description'), page='Description')

# Text page
html.add(sr.H1("This is a Header 1 text"), page='Text')
html.add(sr.H2("This is a Header 2 text"), page='Text')
html.add(sr.H3("This is a Header 3 text"), page='Text')
# html.add(sr.H4("This is a Header 1 text"), page='Text')
html.add(sr.P("This is a Paragraph text"), page='Text')
html.add(sr.List([
    "This is a List of texts",
    "This is also in the List",
    "And this too!"
    ]), page='Text')


# Table page
planets_df = sns.load_dataset('planets')
healthexp_df = sns.load_dataset('healthexp')
mpg_df = sns.load_dataset('mpg')
dowjones_df = sns.load_dataset('dowjones')
df1 = mpg_df

df1_wide = pd.concat([df1]*10, axis=1)
html.add(sr.Table(dataframe=df1, title="This is a Table with a title", use_striped_style=True), page='Table')
# Styling the table
html.add(sr.Table(dataframe=df1.head(), title="This is a Table with a striped style", use_striped_style=True), page='Table')
html.add(sr.Table(dataframe=df1.head(), title="This is another table, without the striped style", use_striped_style=False), page='Table')

html.add(sr.Table(dataframe=df1_wide, title="This is a veeery wide table", use_striped_style=False), page='Table')


# %%
# Matplotlib page
fig1, axes1 = plt.subplots(figsize=(7,4))
axes1.plot(mpg_df['displacement'], mpg_df['horsepower'], 'o')
axes1.set_ylabel('Horsepower')
axes1.set_xlabel('Displacement')
axes1.set_title('A Matplotlib figure made with plt.subplots')

html.add(sr.Plot(axes1), page='Matplotlib')

# %%
axes2 = sns.kdeplot(x=mpg_df['acceleration'], hue=mpg_df['cylinders'], fill=True)
html.add(sr.Plot(axes2), page='Matplotlib')

# axes3 = sns.jointplot(x=mpg_df['displacement'], y=mpg_df['weight'], hue=mpg_df['origin'], kind='hist', palette="crest")
# html.add(sr.Plot(axes3), page='Matplotlib')

# %%

# Plotly page
fig2 = px.histogram(healthexp_df, x="Life_Expectancy", color="Country", opacity=0.8, color_discrete_sequence=px.colors.sequential.Viridis)
fig2.update_layout(barmode='overlay')
html.add(sr.Plot(fig2), page='Plotly')

# fig.show()

fig3 = px.scatter(healthexp_df, x='Life_Expectancy', y='Spending_USD', color='Country')
html.add(sr.Plot(fig3), page='Plotly')

# fig.show()
# %%
# Altair page

# %%
# Collapse page

html.add(sr.Collapse(
    use_panel=True,
    toggle_text='Collapse 1 (Panel)',
    content=[
        # sr.H3("Text and Plot inside Collapse 1"),
        # sr.Plot(figure=fig1),
        sr.H3("This is a Collapse component"),
        sr.P("You can show and hide content inside here in order to save space and add interactivity."),
    ]
), page='Collapse')

html.add(sr.Collapse(
    use_panel=False,
    toggle_text='Collapse 2 (Button)',
    content=[
        sr.H3("This is a Collapse component"),
        sr.P("A Collapse component can also be shown as a button, when the 'use_panel' attribute is set to False."),
        # sr.Plot(figure=axes1),
    ]
), page='Collapse')

html.add(sr.Collapse(
    use_panel=False,
    toggle_text='Collapse with a Plot and a Table',
    content=[
        sr.P("You can also add plots and tables here!"),
        sr.Plot(figure=axes1),
        sr.Table(planets_df.describe()),
    ]
), page='Collapse')

# %%
# Modal page

html.add(sr.Modal(
    toggle_text='Modal',
    content=sr.P('This is the content of the modal.')
    ), page='Modal'
)

html.add(sr.Modal(
    toggle_text='Modal',
    content=[
        sr.P("You can also add plots and tables here!"),
        sr.Plot(figure=axes1),
        sr.Table(planets_df.describe()),
    ]
    ), page='Modal'
)

# %%
# Tabs page
tab1 = sr.Tabs(
    content={
        'Tab 1': sr.P('Content of the first tab'),
        'Tab 2': sr.P('Content of the second tab'),
        'Tab 3': sr.P('Content of the third tab'),
    },
    use_tabs=True
)
html.add(tab1, page='Tabs')

tab2 = sr.Tabs(
    content={
        'Tab 1': [
            sr.P('Content of the first tab'),
            sr.Plot(figure=axes1),
        ],
        'Tab 2': [
            sr.P('Content of the second tab'),
            sr.Plot(figure=axes2),
        ],
    },
    use_tabs=True
)
html.add(tab2, page='Tabs')

tab3 = sr.Tabs(
    content={
        'MPG Data': [
            sr.P('Content of the first tab'),
            sr.Table(dataframe=mpg_df.describe()),
        ],
        'Health Expectancy Data': [
            sr.P('Content of the second tab'),
            sr.Table(dataframe=healthexp_df.describe()),
        ],
        'Planetary Data': [
            sr.P('Content of the third tab'),
            sr.Table(dataframe=planets_df.describe()),
        ],
    },
    use_tabs=False
)
html.add(tab3, page='Tabs')

# %%
# Alerts page


# %%
# Cards


# %%

print(report_directory)
os.makedirs(f"{report_directory}", exist_ok=True)
html.export(report_directory)

# %%
def create_finance_report_demo():
    # Creating data for the report (tables, texts, plots...)
    current_time = datetime.datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    report_directory = f"report_{current_time_str}"

    # Load historical data in the past 10 years
    sp500_history = pd.read_csv('./finance stocks report/fin_data.csv')

    # Remove unnecessary columns
    # sp500_history = sp500_history#.drop(columns=['Dividends', 'Stock Splits'])

    # Create a new column as Close 200 days moving average
    sp500_history['Close_200ma'] = sp500_history['Close'].rolling(200).mean()

    # Create a summary statistics table
    sp500_history_summary = sp500_history.describe()

    # Create a veeeery wide table
    sp500_wide_table = pd.concat([sp500_history_summary]*5, axis=1)

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    fig1 = sns.relplot(data=sp500_history[['Close', 'Close_200ma']], kind='line', height=3, aspect=2.0)

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.histplot(data=sp500_history['Volume'], ax=ax2)

    # https://plotly.com/python-api-reference/generated/plotly.io.to_html.html
    lineplot1 = px.line(sp500_history, y="Close")


    page_names = ['Home', 'Data']
    report_title = 'My report'

    html = sr.HtmlReport(
        report_title=report_title,
        project_name='FinanceReport',
        # author='Douglas Macedo Sgrott',
        pages=page_names,
        background_color='#f47d30'
        )

    html.add(sr.H1('Daily S&P 500 prices report', id='foo'))
    html.add(sr.Tabs(content={
        'Home': sr.P('Home'),
        'Menu 1': sr.P('Menu 1'),
        'Menu 2': sr.P('Menu 2'),
        },
        use_tabs=True
    ))
    html.add(sr.List(text_list="This is a simple list"))
    html.add(sr.Tabs(content={
        'Home': sr.P('Home'),
        'Menu 1': sr.P('Menu 1'),
        'Menu 2': sr.P('Menu 2'),
        },
        use_tabs=False
    ))
    html.add(sr.P('Daily S&P 500 prices report'))
    html.add(sr.P("This is a more complex list:"))
    html.add(sr.List(text_list=["Banana", "Apple", "Orange"]))
    html.add(sr.Collapse(
        use_panel=False,
        toggle_text='Toggle button',
        content=sr.P('This is the content of the toggle button.')
    ))
    html.add(sr.Row(
            sr.P('This is on the left side.'),
            sr.P('This is on the right side.')
        )
    )
    html.add(sr.Collapse(
        use_panel=True,
        toggle_text='Toggle Panel',
        content=sr.P('This is the content of the toggle button.')
    ))

    html.add(sr.Modal(
        toggle_text='Modal',
        content=sr.P('This is the content of the modal.')
    ))
    
    html.add(sr.Card(
        header_name="Card's Header",
        children=[
            sr.H3('Special title treatment'),
            sr.P("With supporting text below as a natural lead-in to additional content."),
        ]
    ))

    html.add(sr.Alert(
        text="This is a text",
        color='primary'
    ))

    html.add(sr.Alert(
        text="This is a Text",
        title="This is a Title",
        color='secondary'
    ))

    html.add(sr.Alert(
        text="This is a Text",
        title="This is a Title",
        subtitle="This is a Sub title",
        color='success'
    ))

    html.add(sr.Modal(
        toggle_text='Modal',
        content=[
            sr.P('This is the content #1 of the modal.'),
            sr.P('This is the content #2 of the modal.'),
            sr.P('This is the content #3 of the modal.'),
            sr.P('This is the content #4 of the modal.'),
        ]
    ))

    html.add(sr.H2('Historical prices of S&P 500'), page='Data')
    html.add(sr.Table(dataframe=sp500_history.head(), title="This is a table title", use_striped_style=True), page='Data')
    html.add(sr.Table(dataframe=sp500_history.head(), use_jquery=True), page='Data')
    html.add(sr.Table(dataframe=sp500_history.tail(3)), page='Data')
    html.add(sr.H2('Historical prices summary statistics'), page='Data')
    html.add(sr.Table(dataframe=sp500_history_summary, title='Summary statistics'), page='Data')
    html.add(sr.Table(dataframe=sp500_wide_table, title='A veeeeeery wide table', caption='This is a caption. This table was generated by repeatedly and horizontally concatenating a table several times.'), page='Data')

    html.add_new_page('Plots')
    html.add(sr.Plot(figure=fig1, id='plot1'), page='Plots')
    html.add(sr.Plot(figure=ax2), page='Plots')
    html.add(sr.Collapse(
        use_panel=True,
        toggle_text='Experiment Foo-31817',
        content=[
            sr.Plot(figure=fig1),
            sr.Plot(figure=ax2)
        ]
    ), page='Plots')
    html.add(sr.Collapse(
        use_panel=True,
        toggle_text='Experiment Foo-46295',
        content=[
            sr.Plot(figure=fig1),
            sr.Plot(figure=ax2)
        ]
    ), page='Plots')
    html.add(sr.Collapse(
        use_panel=True,
        toggle_text='Experiment Foo-52841',
        content=[
            sr.Plot(figure=fig1),
            sr.Plot(figure=ax2)
        ]
    ), page='Plots')
    html.add(sr.Plot(figure=lineplot1), page='Plots')


    os.makedirs(f"{report_directory}", exist_ok=True)
    html.export(report_directory)


# if __name__ == "__main__":
#     # create_finance_report_demo()
#     create_example_report_demo()
#     print("EOL")
