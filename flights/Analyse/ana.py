import pandas as pd
from util import globalvar as gv
import numpy as np
from util import util
import matplotlib.pyplot as plt
import seaborn as sns


file_name = 'Clean/ready_to_analyse.csv'
dtype_dict = {gv.ORI_STATE: 'category',\
                   gv.DEST_STATE: 'category',\
                    gv.DEP_DELAY_15: 'boolean', gv.ARR_DELAY_15: 'boolean', gv.CANCELLED: 'boolean', gv.CANCELLATION_CODE: 'category',\
                    gv.DIVERTED: 'boolean', gv.SCHEDULED_ELAPSED_TIME: 'int64', gv.DISTANCE: 'int64',\
                    gv.DIV_AIRPORT_LANDINGS: 'category',  gv.DIV_REACH_DEST: 'boolean'}

df = pd.read_csv(file_name, dtype=dtype_dict,parse_dates=[gv.FLIGHT_DATE])

df[gv.SCHEDULED_DEP_TIME]=pd.to_datetime(df[gv.SCHEDULED_DEP_TIME],format='%H:%M:%S')
df[gv.SCHEDULED_ARR_TIME]=pd.to_datetime(df[gv.SCHEDULED_ARR_TIME], format='%H:%M:%S')

total_flights = df.shape[0]
no_of_flights_for_each_airline = df.groupby(gv.REPORTING_AIRLINE).count().sort_values(gv.FLIGHT_DATE, ascending=False)[gv.FLIGHT_DATE]
#print(no_of_flights_for_each_airline)
#competitor is WN, AA ranked as 2nd 
#df[gv.WEATHER_DELAY] = df[gv.WEATHER_DELAY].replace(0, np.nan)

#Assume 15mins can be counted as delay
#45mins can be counted as long delay, 180mins can be counted as very long delay
SHORT_DELAY = 15
LONG_DELAY = 45
VERY_LONG_DELAY = 180
# Industry-wide rates
ind_rates = list(util.calculate_delay_rates(df))
ind_ttl_rate = ind_rates[0]
ind_detailed_rates = ind_rates[1:]
print(ind_detailed_rates)
# AA rates
aa_rates = list(util.calculate_delay_rates(df, 'AA'))
aa_ttl_rate = aa_rates[0]
aa_detailed_rates = aa_rates[1:]
# WN rates
wn_rates = list(util.calculate_delay_rates(df, 'WN'))
wn_ttl_rate = wn_rates[0]
wn_detailed_rates = wn_rates[1:]
print('Industry-wide delay rate: {:.2%}'.format(ind_ttl_rate), 'aa delay rate: {:.2%}'.format(aa_ttl_rate), 'wn delay rate: {:.2%}'.format(wn_ttl_rate))

# Data preparation


delay_rates_data = [ind_detailed_rates, aa_detailed_rates, wn_detailed_rates]
delay_rates_categories = ['<=45 mins', '<= 180 mins', '>=180 mins']
util.create_bar_chart(delay_rates_data, delay_rates_categories, 'Delay Rates Comparison', 'Delay Categories', 'Rates', ['Industry', 'AA', 'WN'])

'---------------------------------'

ind_delayed_causes_rates = list(util.calculate_delay_cause_rates(df))
aa_delayed_causes_rates = list(util.calculate_delay_cause_rates(df, 'AA'))
wn_delayed_causes_rates = list(util.calculate_delay_cause_rates(df, 'WN'))
#print(ind_delayed_causes_rates, aa_delayed_causes_rates, wn_delayed_causes_rates)

delay_causes_data = [ind_delayed_causes_rates, aa_delayed_causes_rates, wn_delayed_causes_rates]
delay_causes_categories = ['Late Aircraft', 'Carrier','NAS', 'Weather','Diverted','Security']
util.create_bar_chart(delay_causes_data, delay_causes_categories, 'Delay Causes Rates Comparison', 'Delay Causes', 'Rates', ['Industry', 'AA', 'WN'])

'---------------------------------'
aa_dealy_cause_hours = util.calculate_hours_lost_under_each_cause(df, 'AA')
'---------------------------------'


print(util.most_delayed_route(df,'AA'))