
import pandas as pd
from ydata_profiling import ProfileReport
import numpy as np
from util import globalvar as gv
from util import util


pd.set_option('display.max_columns', 33)
file_name = 'Clean/feature_filtered.csv'
df = pd.read_csv(file_name)

profile = ProfileReport(df, minimal=True)   
profile.to_file('Clean/feature_filtered_df_profile.html')

abonormal_div_airport_landings =df[df['div_airport_landings']==9]
#print(abonormal_div_airport_landings.info())
#landing time all empty, cancellation code all non empty, so dim these are actually all cancelled flights
df['div_airport_landings']=df['div_airport_landings'].replace(9,0)
df['flight_date']=pd.to_datetime(df['flight_date'])



columns_to_convert_time = ['scheduled_dep_time', 'scheduled_arr_time']

for column in columns_to_convert_time:
    df = util.convert_to_time(df, column)

columns_to_convert_int = ['flight_number','dep_delay_time(mins)', 'arr_delay_time(mins)',\
                          'scheduled_elapsed_time(mins)', 'distance(miles)', 'carrier_delay(mins)', 'weather_delay(mins)',\
                            'nas_delay(mins)', 'security_delay(mins)', 'late_aircraft_delay(mins)', 'div_airport_landings',\
                            'diverted_delay(mins)','gate_takeoff_gap(mins)','land_gate_gap(mins)', 'distance(miles)']
                          
for column in columns_to_convert_int:
    df = util.convert_to_int(df, column)

df['div_reach_dest']=df['div_reach_dest'].astype(pd.BooleanDtype())

column_to_extract = ['ori_city','dest_city']
for column in column_to_extract:
    df= util.split_str(df,column,',')

column_0_to_na = ['carrier_delay(mins)', 'weather_delay(mins)','nas_delay(mins)', 'security_delay(mins)', 'late_aircraft_delay(mins)']
for column in column_0_to_na:
    df = util.convert_z_to_na(df, column)


column_datatypes = df.dtypes.to_dict()
dic_convert_type={'reporting_airline': str, 'ori_airport': str, 'ori_city': str, 'ori_state': 'category', 'dest_airport': str,\
                'dest_city': str, 'dest_state': 'category', 'cancelled': 'bool', 'cancellation_code': 'category','diverted': 'bool'}

df = df.astype(dic_convert_type)

print(df.dtypes)

#copy value from diverted delayed mins to arr_delay_time(mins)
df['arr_delay_time(mins)'] = np.where(df['arr_delay_time(mins)'].isna(), df['diverted_delay(mins)'], df['arr_delay_time(mins)'])


df['diverted_delay(mins)']=df['diverted_delay(mins)'].fillna(0)

df['diverted_delay(mins)'] = np.where(df['diverted_delay(mins)'] < 0, 0, df['diverted_delay(mins)'])
df['diverted_delay(mins)'].replace(0, np.nan, inplace=True)

df.to_csv('Clean/ready_to_analyse.csv', index=False)

profile = ProfileReport(df, minimal=True)   
profile.to_file('Clean/ready_to_analyse_profile.html')

