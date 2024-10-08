# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas
#import streamlit_pandas as sp

# Write directly to the app
st.title("Tim is the best :white_check_mark:")
st.write(
    """choose the fruits you want in your smoothie
    """)

name_on_order = st.text_input('Name on smoothie:')
st.write('The name on the smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#convert snowpark df to a pandas df so we can use the loc function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop

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
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        #st.text(fruityvice_response.json())
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop

    time_to_insert = st.button ('Submit your order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+ name_on_order+'!', icon="✅")



