# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

st.title('Smoothie Shoppee')

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """)

name_on_order = st.text_input('Name of the Smoothie:')
st.write("The name on the Smoothie will be", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert the snowpark Datafram to a Padas Datafram so can use the LOC function.
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
#st.stop()
                                                                                            
# Convert Snowpark DataFrame to a list of values
fruit_list = [row['FRUIT_NAME'] for row in my_dataframe.collect()]

#ingredients_list = st.multiselect(
 #   "choose up to 5 ingredients",     
  #   my_dataframe,
   #  #default=["Dragon Fruit", "Guava"],
#)
 
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients'
     , my_dataframe 
    , max_selections=5
 )
#st.write(ingredients_list)
#st.text(ingredients_list)

#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
#sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
 
if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        

        #smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon") 
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
 

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string +"""','"""+name_on_order +"""')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()  
        #works st.success('Your Smoothie is ordered!', icon="✅")
        #works st.success(f"Your Smoothie is ordered, {name_on_order}%", icon="✅")
        st.success("Your Smoothie is ordered, " + name_on_order + "!", icon="✅")

