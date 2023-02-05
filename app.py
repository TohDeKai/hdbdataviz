import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title="HDB Resale Transactions")

# Load dataframe
csv_file = 'resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv'
df = pd.read_csv(csv_file)

# Selection
flat_type = df['flat_type'].unique().tolist()
town = df['town'].unique().tolist()
lease_commence_date = df['lease_commence_date'].unique().tolist()
filter = ['flat_type','town','lease_commence_date']


#Index(['month', 'town', 'flat_type', 'block', 'street_name', 
# 'storey_range','floor_area_sqm', 'flat_model', 
# 'lease_commence_date','remaining_lease', 'resale_price'],dtype='object')


filter_selection = st.selectbox('Select filtering criteria: ',
                      filter)

flat_type_container = st.container()
all_flat = st.checkbox(label="Select all flats",key='flat')
 
if all_flat:
    flat_type_selection = flat_type_container.multiselect("Select flat type:",
         flat_type, flat_type)
else:
    flat_type_selection =  flat_type_container.multiselect("Select flat type:",
        flat_type)
    
town_container = st.container()
all_town = st.checkbox(label="Select all towns",key='town')
 
if all_town:
    town_selection = town_container.multiselect("Select town:",
         town, town)
else:
    town_selection =  town_container.multiselect("Select town:",
        town)

lease_commence_date_selection = st.slider('Lease Commence Date:',
                                          min_value=min(lease_commence_date),
                                          max_value=max(lease_commence_date),
                                          value=(min(lease_commence_date),max(lease_commence_date)))

# Filtering based on selection
mask = (df['flat_type'].isin(flat_type_selection) & df['town'].isin(town_selection)&df['lease_commence_date'].between(*lease_commence_date_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

df_filtered = df[mask]

try:
    if filter_selection == "lease_commence_date":
        chart = px.line(df_filtered,
                        x=df_filtered.groupby(filter_selection).median()['resale_price'].index,
                        y=df_filtered.groupby(filter_selection).median()['resale_price'],
                        text=df_filtered.groupby(filter_selection).median()['resale_price']).update_layout(
            xaxis_title=filter_selection, yaxis_title="Median Resale Price")
    else:
        chart = px.bar(df_filtered,
                        x=df_filtered.groupby(filter_selection).median()['resale_price'].index,
                        y=df_filtered.groupby(filter_selection).median()['resale_price'],
                        text=df_filtered.groupby(filter_selection).median()['resale_price']).update_layout(
            xaxis_title=filter_selection, yaxis_title="Median Resale Price")
        
    st.plotly_chart(chart)
except ValueError:
    st.write("Please select the values")
# bar_chart = px.bar(df_grouped,
#                   x=df_grouped[filter_selection],
#                   y=df_grouped['resale_price'],
#                   color_discrete_sequence = ['#F63366']*len(df_grouped),
#                   template= 'plotly_white')
# st.plotly_chart(bar_chart)