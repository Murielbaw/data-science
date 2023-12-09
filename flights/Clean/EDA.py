
import pandas as pd
from ydata_profiling import ProfileReport
from util import globalvar as gl



file_name = 'flights.csv'
#df_sample = pd.read_csv(file_name, nrows=10000)
#print(df_sample.iloc[:,48].unique())
#print(df_sample.iloc[:,77].unique())
#print(df_sample.iloc[:,84].unique())
#print(df_sample[df_sample.iloc[:,77].isna()].shape)
#print(df_sample[df_sample.iloc[:,84].isna()].shape)
dtype_dict = {48: 'str', 77: 'str', 84: 'str'}
#print(df_sample.iloc[:, [48, 77, 84]].dtypes)
df= pd.read_csv(file_name, dtype=dtype_dict)
#profil = ProfileReport(df, minimal=True)
#profil.to_file('df_profile.html')


df_columns = df.columns.to_list()
'''index = df.columns.get_loc('div1airport')
df_columns = df_columns[:index]
df_columns.append('div2airport')'''
print(len(df_columns))

'''list_to_drop = ['year','quarter','month','dayofmonth','dayofweek','dot_id_reporting_airline','iata_code_reporting_airline','tail_number',\
     'originairportseqid','origincitymarketid','originairportid','originstatefips','originstate','originwac','destairportid',\
        'destairportseqid','destcitymarketid','deststatefips','deststate','destwac','depdelayminutes','departuredelaygroups',\
        'deptimeblk','taxiout','taxiin','arrdelayminutes','arrivaldelaygroups','arrtimeblk','actualelapsedtime','airtime','flights',\
        'firstdeptime','totaladdgtime','longestaddgtime','divreacheddest','divactualelapsedtime','divdistance']'''

columns_to_keep=['flightdate', 'reporting_airline', 'flight_number_reporting_airline', 'origin', 'origincityname', 'originstatename',\
                   'dest', 'destcityname', 'deststatename', 'crsdeptime', 'depdelay', 'taxiout', 'taxiin', \
                        'crsarrtime', 'arrdelay', 'cancelled', 'cancellationcode', 'diverted', 'crselapsedtime',\
                        'distance', 'carrierdelay', 'weatherdelay', 'nasdelay', 'securitydelay', 'lateaircraftdelay', \
                                'divairportlandings','divreacheddest', 'divarrdelay']



df_filtered = df[columns_to_keep]

dic_new_col_name={'flightdate':gl.FLIGHT_DATE, 'airline':'airline', 'flight_number_reporting_airline':'flight_number',\
                    'origin':'ori_airport', 'origincityname':'ori_city', 'originstatename':'ori_state',\
                    'dest':'dest_airport', 'destcityname':'dest_city', 'deststatename':'dest_state',\
                    'crsdeptime':'scheduled_dep_time', 'depdelay':'dep_delay_time(mins)',\
                    'taxiout':'gate_takeoff_gap(mins)', 'taxiin':'land_gate_gap(mins)', \
                    'crsarrtime':'scheduled_arr_time', 'arrdelay':'arr_delay_time(mins)',\
                    'cancelled':'cancelled', 'cancellationcode':'cancellation_code',\
                    'diverted':'diverted', 'crselapsedtime':'scheduled_elapsed_time(mins)',\
                    'distance':'distance(miles)', 'carrierdelay':'carrier_delay(mins)', 'weatherdelay':'weather_delay(mins)',\
                    'nasdelay':'nas_delay(mins)', 'securitydelay':'security_delay(mins)',\
                    'lateaircraftdelay':'late_aircraft_delay(mins)', 'divairportlandings':'div_airport_landings',\
                    'divarrdelay':'diverted_delay(mins)', 'divreacheddest':'div_reach_dest'}

df_filtered = df_filtered.rename(columns=dic_new_col_name)

df_filtered.to_csv('Clean/feature_filtered.csv', index=False)








