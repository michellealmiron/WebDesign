
import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

from streamlit_option_menu import option_menu

# Add the Streamlit option menu
menu = option_menu(None, ["Globally", "Across Time", "Correlations", "Applications"],
                   icons=['globe', 'calendar', 'search', 'bullseye'], menu_icon="cast",
                   default_index=0, orientation="horizontal",
                   styles={
                       "container": {"padding": "3!important"},
                       "icon": {"color": "white", "font-size": "25px"},
                       "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px"},
                       "nav-link-selected": {"background-color": "skyblue"},
                   }
                   )
st.sidebar.markdown("# Globally")
menu





# Load the mental health disorder data
file_path = 'Mental health Depression disorder Data.csv'
data = pd.read_csv(file_path, low_memory=False)

# Select relevant columns for processing
columns_of_interest = ['Entity', 'Bipolar disorder (%)', 'Anxiety disorders (%)',
                         'Drug use disorders (%)', 'Depression (%)', 'Alcohol use disorders (%)']

# Convert columns to numeric after removing non-numeric entries
data[columns_of_interest[1:]] = data[columns_of_interest[1:]].apply(pd.to_numeric, errors='coerce')

# Drop rows with missing values
data.dropna(subset=columns_of_interest[1:], inplace=True)

# Find the country with the highest percentage for each health problem
max_percentage_countries = {}
for column in columns_of_interest[1:]:
    max_percentage_row = data.loc[data[column].idxmax()]
    country = max_percentage_row['Entity']
    percentage = max_percentage_row[column]
    max_percentage_countries[column] = {'Country': country, 'Percentage': percentage}

# Create a DataFrame from the dictionary
max_percentage_df = pd.DataFrame.from_dict(max_percentage_countries, orient='index').reset_index()
max_percentage_df.columns = ['Health Problem', 'Country', 'Percentage']


# Streamlit app
st.title('Mental Health')

# Agregar opción de menú "Globally"
if menu == "Globally":
    st.markdown("""Mental health is a global issue that profoundly impacts individuals and societies worldwide. The importance of mental well-being transcends geographical boundaries, affecting people of all ages, backgrounds, and cultures. Addressing mental health on a global scale is crucial for building resilient communities, fostering understanding, and promoting collective well-being. The recognition of mental health as a universal concern highlights the need for collaborative efforts to reduce stigma, increase access to mental health resources, and create supportive environments that prioritize the mental well-being of individuals across the world.""")

    # Plot the choropleth map using Plotly Express
    fig1 = px.choropleth(max_percentage_df,
                        locations='Country',
                        locationmode='country names',
                        color='Percentage',
                        hover_name='Health Problem',
                        title='Country with the Highest Percentage for Each Health Problem')


    # Display the choropleth map using Streamlit
    st.plotly_chart(fig1)






# Cargar los datos desde el archivo CSV
file_path = 'Mental health Depression disorder Data.csv'
data = pd.read_csv(file_path, low_memory=False)

# Convertir la columna 'Year' a numérica (ignorar errores para valores no numéricos)
data['Year'] = pd.to_numeric(data['Year'], errors='coerce')

# Filtrar datos para el año 2017 (puedes cambiar el año si es necesario)
data_2017 = data[data['Year'] == 2017]

# Seleccionar columnas relevantes para el mapa geoespacial
columns_of_interest = ['Entity', 'Bipolar disorder (%)', 'Anxiety disorders (%)',
                         'Drug use disorders (%)', 'Depression (%)', 'Alcohol use disorders (%)']

# Convertir columnas a numéricas (ignorar errores para valores no numéricos)
data_2017[columns_of_interest[1:]] = data_2017[columns_of_interest[1:]].apply(pd.to_numeric, errors='coerce')

# Cargar el shapefile del mundo
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Fusionar el shapefile del mundo con los datos
world = world.merge(data_2017[columns_of_interest], left_on='name', right_on='Entity', how='left')

# Definir función para la gráfica
def plot_geospatial_map():
    # Crear subgráficos para cada trastorno de salud mental
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Prevalencia de Trastornos de Salud Mental (2017)')

    for ax, disorder in zip(axes.flatten(), columns_of_interest[1:]):
        world.plot(column=disorder, ax=ax, legend=True, cmap='Blues', legend_kwds={'label': f'{disorder} (%)'})
        ax.set_title(disorder)
        ax.set_axis_off()

    return fig  # Return the Matplotlib figure

# Agregar opción de menú "Globally"
if menu == "Globally":
    # Call the plot_geospatial_map function to get the Matplotlib figure
    matplot_fig = plot_geospatial_map()

    # Show the Matplotlib figure in Streamlit
    st.pyplot(matplot_fig)






# Cargar los datos desde el archivo CSV
file_path = 'Mental health Depression disorder Data.csv'
data = pd.read_csv(file_path)

# Assuming the column for Depression percentage is named 'Depression (%)'
# If your column name is different, please replace it accordingly
depression_column = 'Depression (%)'

# Convert the 'Depression (%)' column to numeric
data[depression_column] = pd.to_numeric(data[depression_column], errors='coerce')

# Group by 'Entity' (country) and calculate the average depression percentage
average_depression = data.groupby('Entity')[depression_column].mean()

# Get the top 10 countries with the highest average depression percentage
top_10_countries = average_depression.sort_values(ascending=False).head(10)


# Agregar opción de menú "Globally"
if menu == "Globally":
    # Plot the bar graph
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    top_10_countries.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax2)
    plt.title('Top 10 Countries with the Highest Average Depression Percentage')
    plt.xlabel('Country')
    plt.ylabel('Average Depression Percentage')
    plt.xticks(rotation=45, ha='right')

    # Show the Matplotlib figure in Streamlit
    st.pyplot(fig2)





# Load the mental health disorder data
file_path = 'Mental health Depression disorder Data.csv'
data = pd.read_csv(file_path, low_memory=False)

# Select relevant columns for processing
columns_of_interest = ['Entity', 'Bipolar disorder (%)', 'Anxiety disorders (%)',
                         'Drug use disorders (%)', 'Depression (%)', 'Alcohol use disorders (%)']

# Convert columns to numeric after removing non-numeric entries
data[columns_of_interest[1:]] = data[columns_of_interest[1:]].apply(pd.to_numeric, errors='coerce')

# Drop rows with missing values
data.dropna(subset=columns_of_interest[1:], inplace=True)

# Agregar opción de menú "Globally"
if menu == "Globally":
    # Create basic choropleth map with year animation for Depression
    fig3 = px.choropleth(data,
                        locations='Entity',
                        locationmode='country names',
                        color='Depression (%)',  # Change this to the desired health problem
                        hover_name='Entity',
                        animation_frame='Year',
                        title='Depression Percentage by Country Over Time')

    # Set projection to natural earth
    fig3.update_geos(projection_type='natural earth')

    # Show the Plotly Express figure in Streamlit
    st.plotly_chart(fig3)




# Load the data from your CSV file
file_path = 'Mental health Depression disorder Data.csv'
data = pd.read_csv(file_path)

# Select relevant columns
columns_of_interest = ['Entity', 'Year', 'Schizophrenia (%)', 'Bipolar disorder (%)', 'Eating disorders (%)',
                        'Anxiety disorders (%)', 'Drug use disorders (%)', 'Depression (%)',
                        'Alcohol use disorders (%)']
selected_data = data[columns_of_interest]

# Convert percentage columns to numeric, handling 'coerce' to replace non-numeric values with NaN
percentage_columns = ['Schizophrenia (%)', 'Bipolar disorder (%)', 'Eating disorders (%)',
                       'Anxiety disorders (%)', 'Drug use disorders (%)', 'Depression (%)',
                       'Alcohol use disorders (%)']
selected_data[percentage_columns] = selected_data[percentage_columns].apply(pd.to_numeric, errors='coerce')

# Agregar opción de menú "Across Time"
if menu == "Across Time":
    # Create a selection box for choosing the country
    selected_country = st.selectbox('Select a country:', selected_data['Entity'].unique())

    # Filter data for the selected country
    country_data = selected_data[selected_data['Entity'] == selected_country]

    # Plot the time series line plot with different colors for each disorder
    fig5, ax5 = plt.subplots(figsize=(12, 6))

    for disorder in percentage_columns:
        ax5.plot(country_data['Year'], country_data[disorder], marker='o', linestyle='-', label=disorder)

    plt.title(f'Time Series Line Plot for Mental Health Disorders in {selected_country} (1990-2017)')
    plt.xlabel('Year')
    plt.ylabel('Percentage')
    plt.legend()
    plt.grid(True)

    # Show the Matplotlib figure in Streamlit
    st.pyplot(fig5)




# Load the data from your CSV file
file_path = 'Mental health Depression disorder Data.csv'
data = pd.read_csv(file_path)

# Agregar opción de menú "Across Time"
if menu == "Across Time":
    # Create a selection box for choosing the health problem
    selected_health_problem = st.selectbox('Select a health problem:', data.columns[3:])

    # Calculate the global percentage for the selected health problem for each year
    global_percentage = data.groupby('Year')[selected_health_problem].mean()

    # Plotting the line chart
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    ax4.plot(global_percentage.index, global_percentage, marker='o', linestyle='-', color='b')
    plt.title(f'Global Percentage of {selected_health_problem} Over the Years (1990-2017)')
    plt.xlabel('Year')
    plt.ylabel(f'{selected_health_problem} (%)')
    plt.grid(True)

    # Show the Matplotlib figure in Streamlit
    st.pyplot(fig4)





# Load the data from your CSV file
file_path = 'Mental health Depression disorder Data.csv'
data = pd.read_csv(file_path, low_memory=False)

# Agregar opción de menú "Correlations"
if menu == "Correlations":
    # Create a selection box for choosing the country
    selected_country = st.selectbox('Select a country:', data['Entity'].unique())

    # Filter data for the selected country
    data_selected_country = data[data['Entity'] == selected_country]

    # Select relevant columns for the correlation heatmap
    columns_of_interest = ['Schizophrenia (%)', 'Bipolar disorder (%)', 'Eating disorders (%)',
                             'Anxiety disorders (%)', 'Drug use disorders (%)', 'Depression (%)',
                             'Alcohol use disorders (%)']

    # Drop rows with missing values in the selected columns
    data_selected_country_filtered = data_selected_country.dropna(subset=columns_of_interest)

    # Calculate the correlation matrix
    correlation_matrix = data_selected_country_filtered[columns_of_interest].corr()

    # Plot the Heatmap
    fig6, ax6 = plt.subplots(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title(f'Correlation Heatmap of Mental Health Disorders in {selected_country}')
    plt.show()

    # Show the Matplotlib figure in Streamlit
    st.pyplot(fig6)



# Load the data from your CSV file
file_path = 'Mental health Depression disorder Data.csv'
data = pd.read_csv(file_path, low_memory=False)

# Select relevant columns for the correlation heatmap
columns_of_interest = ['Schizophrenia (%)', 'Bipolar disorder (%)', 'Eating disorders (%)',
                         'Anxiety disorders (%)', 'Drug use disorders (%)', 'Depression (%)',
                         'Alcohol use disorders (%)']

# Drop rows with missing values in the selected columns
data_filtered = data.dropna(subset=columns_of_interest)

# Calculate the correlation matrix
correlation_matrix = data_filtered[columns_of_interest].corr()

# Plot the Heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Heatmap of Mental Health Disorders Across All Countries')
plt.show()


# Load the data from your CSV file
file_path = 'Mental health Depression disorder Data.csv'
data = pd.read_csv(file_path, low_memory=False)

# Agregar opción de menú "Correlations"
if menu == "Correlations":
    # Select relevant columns for the correlation heatmap
    columns_of_interest = ['Schizophrenia (%)', 'Bipolar disorder (%)', 'Eating disorders (%)',
                             'Anxiety disorders (%)', 'Drug use disorders (%)', 'Depression (%)',
                             'Alcohol use disorders (%)']

    # Drop rows with missing values in the selected columns
    data_filtered = data.dropna(subset=columns_of_interest)

    # Calculate the correlation matrix
    correlation_matrix = data_filtered[columns_of_interest].corr()

    # Plot the Heatmap
    fig7, ax7 = plt.subplots(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title(f'Correlation Heatmap of Mental Health Disorders Accross All Countries')
    plt.show()

    # Show the Matplotlib figure in Streamlit
    st.pyplot(fig7)






# Assuming your data is stored in a CSV file named 'mental_health_data.csv'
# Adjust the file name and path accordingly

file_path = 'Mental health Depression disorder Data.csv'
data = pd.read_csv(file_path)

# Select only the columns of interest
columns_of_interest = ['Schizophrenia (%)', 'Bipolar disorder (%)', 'Eating disorders (%)',
                        'Anxiety disorders (%)', 'Drug use disorders (%)', 'Depression (%)',
                        'Alcohol use disorders (%)']
selected_data = data[columns_of_interest]

# Remove rows with missing values
selected_data = selected_data.dropna()

# Calculate the mean percentage for each mental health disorder
mean_percentage_across_all_data = selected_data.mean()

# Agregar opción de menú "Correlations"
if menu == "Correlations":
    # Plotting the bar chart
    fig8, ax8 = plt.subplots(figsize=(12, 8))
    mean_percentage_across_all_data.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Mean Percentage of Mental Health Disorders (1990-2017)')
    plt.xlabel('Mental Health Disorder')
    plt.ylabel('Mean Percentage')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # Show the Matplotlib figure in Streamlit
    st.pyplot(fig8)




# Load the data
file_path = 'Mental health Depression disorder Data.csv'
data = pd.read_csv(file_path, low_memory=False)

# Your existing code for other menu options...

# Agregar opción de menú "Applications"
if menu == "Applications":
    st.markdown("## Applications of Mental Health Data")

    st.markdown("### 1. Healthcare and Mental Health Organizations:")
    st.markdown("- **Insights for Intervention:** Visualizing the prevalence of different mental health disorders over time "
                "and across countries can provide insights into trends. This information can guide healthcare professionals "
                "and organizations in developing targeted interventions and mental health programs.")
    st.markdown("- **Resource Allocation:** Understanding the distribution of mental health disorders in different regions "
                "helps in allocating resources effectively. For example, areas with a high prevalence of certain disorders "
                "may require more mental health facilities, professionals, and support services.")

    st.markdown("### 2. Pharmaceutical Industry:")
    st.markdown("- **Drug Development:** Insights into the prevalence of specific mental health disorders can inform "
                "pharmaceutical companies about the demand for treatments. This information may guide research and "
                "development efforts toward creating medications for prevalent disorders.")

    st.markdown("### 3. Government and Policy Makers:")
    st.markdown("- **Public Health Policies:** Governments can use the data to formulate mental health policies and allocate "
                "budgets for mental health programs. Visualizations can highlight areas that need more attention and resources.")
    st.markdown("- **Regional Disparities:** Identify regions with higher mental health burdens, helping policymakers address "
                "disparities and implement targeted interventions.")

    st.markdown("### 4. Global Organizations and NGOs:")
    st.markdown("- **Advocacy and Awareness:** Organizations focused on mental health advocacy can use visualizations to raise "
                "awareness about the global burden of mental health disorders. This can contribute to reducing stigma and promoting understanding.")

    st.markdown("### 5. Insurance Companies:")
    st.markdown("- **Risk Assessment:** Insurance companies may benefit from understanding the prevalence of mental health disorders "
                "in different regions. This knowledge can inform risk assessments and the development of mental health coverage policies.")

    st.markdown("### 6. Researchers and Academia:")
    st.markdown("- **Academic Research:** Researchers can use the data to conduct studies on the factors influencing mental health, "
                "contributing to academic research and literature.")
    st.markdown("- **Longitudinal Studies:** Time series analyses can help researchers identify patterns and changes in mental health "
                "trends over the years.")

    st.markdown("### 7. Technology and Telehealth:")
    st.markdown("- **Digital Mental Health Solutions:** Companies developing digital mental health solutions, apps, and telehealth "
                "services can use the information to target regions with high prevalence and tailor their services accordingly.")

    st.markdown("Understanding the mental health landscape globally and over time is crucial for creating effective strategies, "
                "policies, and interventions. The visualizations provide a powerful tool for stakeholders to make informed decisions "
                "and contribute to the improvement of mental health on a global scale.")
