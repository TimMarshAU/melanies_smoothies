# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Tim is the best :white_check_mark:")
st.write(
    """choose the fruits you want in your smoothie
    """)

name_on_order = st.text_input('Name on smoothie:')
st.write('The name on the smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)

#if ingredients_list is NOT null then...
if ingredients_list: 
    #st.write (ingredients_list)
    #st.text (ingredients_list)

    #set new variable as empty
    ingredients_string=''

    #create counter X, for each row / X in...
    for x in ingredients_list:
        ingredients_string += x + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop

    time_to_insert = st.button ('Submit your order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+ name_on_order+'!', icon="✅")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())
fv_df=st.dataframe(data=fruitvice_response.json(), use_container_width=True)
