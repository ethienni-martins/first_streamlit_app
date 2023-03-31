#importing all the libraries
import pandas
import requests
import snowflake.connector
import streamlit
from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu') 
streamlit.text('🥣 Omega 3 & Bleberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Har-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#streamlit.dataframe(my_fruit_list)
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
# Choice of few fruits
# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# streamlit.dataframe(my_fruit_list) // Changed 
streamlit.dataframe(fruits_to_show)

#New Section to display fruityvice api response
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response)

#New section to display fruityvice api response
#changes to the api response section
try:
  fruit_choice = streamlit.text_input('What fruit would like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please, select a fruit to receive information about.")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
    # Take the json version of the response and normalize it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # Output it to the screen as a table
    streamlit.dataframe(fruityvice_normalized)
    
  except URLError as e:
    streamlit.error()

 streamlit.header('Fruityvice Fruit Advice')
      
 streamlit.write('The user entered', fruit_choice)


#Stopping the app from adding rows to the fruit_load_list table
streamlit.stop()

# importing libraries
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)
# Let the end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would like to add to the list?','Jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

#including the add_my_fruit to the load list
my_cur.execute("Insert into fruit_load_list values ('from streamlit')")
