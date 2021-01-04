
# importing the module 
import pandas as pd 
  
# creating the DataFrame 
my_df = {'Name': ['Rutuja', 'Anuja'],  
         'ID': [1, 2],  
         'Age': [20, 19]} 
df = pd.DataFrame(my_df) 
  
# displaying the DataFrame 
print('DataFrame:\n', df) 
   
# saving the DataFrame as a CSV file 
gfg_csv_data = df.to_csv('GfG.csv', index = True) 
print('\nCSV String:\n', gfg_csv_data) 



