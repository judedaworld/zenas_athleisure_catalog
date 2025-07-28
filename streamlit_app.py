# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import pandas as pd

# Write directly to the app
st.title(f"Zena's Amazing Athleisure Catalog")

# Get the current credentials
session = get_active_session()

# Get a list of colors for a drop list selection
table_colors = session.sql("select color_or_style from catalog_for_website")
pd_colors = table_colors.to_pandas()

# Put the list of colors into a drop list selector
option = st.selectbox('Pick a sweatsuit color or style:', pd_colors)

# Build the image caption
product_caption = 'Our warm, comfortable, ' + option + ' sweatsuit!'

# Use the color selected to go back and get all the info from the database
table_prod_data = session.sql("\
    select file_name, price, size_list, \
        upsell_product_desc, file_url \
    from catalog_for_website \
    where color_or_style = '" + option + "';\
")
pd_prod_data = table_prod_data.to_pandas()

# Assign each column of the row returned to its own variable
price = '$' + str(pd_prod_data['PRICE'].iloc[0])+'0'
file_name = pd_prod_data['FILE_NAME'].iloc[0]
size_list = pd_prod_data['SIZE_LIST'].iloc[0]
upsell = pd_prod_data['UPSELL_PRODUCT_DESC'].iloc[0]
url = pd_prod_data['FILE_URL'].iloc[0]

# Display the info on the page
st.image(image=file_name, width=400, caption=product_caption)
st.markdown('**Price:** ' + price)
st.markdown('**Sizes Available:** ' + size_list)
st.markdown('**Also Consider:** ' + upsell)

st.write(url)
