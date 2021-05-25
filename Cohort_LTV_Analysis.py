# This Method Calculates ARPU = (Total Revenue) / (Number of Customers for a chosen Time Period)
# ARPU = Average Revenue per User

def method1(clean_set_base, start_ym, end_ym):
    '''Returns ARPU for a chosen time period'''
    dfs = clean_set_base.copy()
    dfs.UniqueCustomerID = dfs.UniqueCustomerID.astype(str)
    dfs.Postdate = pd.to_datetime(dfs.Postdate).dt.normalize()
    dfs['ym'] = list(zip(dfs.Postdate.dt.year, dfs.Postdate.dt.month))

    # Number of Customers for Chosen Period
    dfs = dfs[(dfs.ym >= start_ym) & (dfs.ym <= end_ym)]
    numberOfCustomers = len(dfs.UniqueCustomerID.unique().tolist())

    # Total Revenue
    totalRevenue = dfs['PaymentAmount'].sum()

    ARPU = totalRevenue/numberOfCustomers

    return ARPU


# This method calculates Average Revenue per Cohort rather than User/Customer level
# Cohort = a group of customers with similar characteristics
# In this usage we define a cohort by customers who made their first purchase during the same month

def cohort_signups_pyramid(settled_data, adds_data, signup_data):
    '''Calculates and Computes a Cohort Pyramid Table for # of Signups by Month'''
    def do_function(yearmon, settled_data, adds_data, signup_data):

        ck_list = []
        ck_dict = {}

        settled_data = settled_data[settled_data.pym >=  yearmon]

        signups = set(signup_data[signup_data.pym == yearmon].UniqueCustomerID)
        adds = set(adds_data[adds_data.pym == yearmon].UniqueCustomerID)
        settleds = set(settled_data[settled_data.pym == yearmon].UniqueCustomerID)
        start_ck = signups
#         print(len(start_ck))
#         print('Initial for ', yearmon, ': ', len(start_ck))
        ck_list.append(len(start_ck))
        ck_dict[yearmon] = len(start_ck)

        settled_data = settled_data[settled_data.pym > yearmon]
        pymlist = list(settled_data.pym.unique())
        for pym in pymlist:
            settleds = set(settled_data[settled_data.pym == pym].UniqueCustomerID)
            next_ck = start_ck.intersection(settleds)
            ck_list.append(len(next_ck))
            ck_dict[pym] = len(next_ck)

        df = pd.DataFrame(ck_dict, index=['Active Subscribers:'], columns=list(ck_dict.keys()))
        return df

    settled_data['pym'] = settled_data['pym'].astype(str)
    adds_data['pym'] = adds_data['pym'].astype(str)
    signup_data['pym'] = signup_data['pym'].astype(str)

    pymlist = list(settled_data.pym.unique())
    dflist = []
    for pym in pymlist:
#         print('processed: ', pym)
        codf = do_function(pym, settled_data, adds_data, signup_data)
        dflist.append(codf)

    df_all = pd.concat(dflist)
    return df_all


def cohort_revenue_pyramid(settled_data, adds_data, signup_data):
    '''Calculates and Computes a Cohort Pyramid Table for Revenue $ by Month'''
    def do_function(yearmon, settled_data, adds_data, signup_data):

        ck_list = []
        rev_dict = {}
        settled_data = settled_data[settled_data.pym >=  yearmon]

        signups = set(signup_data[signup_data.pym == yearmon].UniqueCustomerID)
        start_ck = signups
#         print('Initial for ', yearmon, ': ', len(start_ck))
        num_signups = len(start_ck)

        rev = settled_data[settled_data.UniqueCustomerID.isin(start_ck)]['PaymentAmount'].sum()
        rev_dict[yearmon] = rev

        settled_data = settled_data[settled_data.pym > yearmon]
        pymlist = list(settled_data.pym.unique())
        for pym in pymlist:
            settleds = set(settled_data[settled_data.pym == pym].UniqueCustomerID)
            next_ck = start_ck.intersection(settleds)
            rev = settled_data[settled_data.UniqueCustomerID.isin(next_ck)]['PaymentAmount'].sum()
            rev_dict[pym] = rev

        df = pd.DataFrame(rev_dict, index=['Revenue:'], columns=list(rev_dict.keys()))
        return df, num_signups

    settled_data['pym'] = settled_data['pym'].astype(str)
    adds_data['pym'] = adds_data['pym'].astype(str)
    signup_data['pym'] = signup_data['pym'].astype(str)

    pymlist = list(settled_data.pym.sort_values().unique())
    dflist = []
    sulist = []
    for pym in pymlist:
        codf, nsignups = do_function(pym, settled_data, adds_data, signup_data)
        dflist.append(codf)
        sulist.append(nsignups)

    df_revenue = pd.concat(dflist)

    return df_revenue

#######################################################################################################################

import pandas as pd
import datetime
import warnings
import math
import sys
import numpy as np
import os
warnings.filterwarnings('ignore')

# Load Data
sample_payment_data = pd.read_pickle(os.getcwd() + '/sample_data/sample_settled_data.pkl')
sample_adds_data = pd.read_pickle(os.getcwd() + '/sample_data/sample_adds_data.pkl')
sample_signups_data = pd.read_pickle(os.getcwd() + '/sample_data/sample_signup_data.pkl')

# Example Usage
method1(sample_payment_data, (2021,1), (2021,12))

# Expand above usage for ARPU's over full year by month
x = 1
while x <= 12:
    print('ARPU From (2021, {}) to (2021, 12): '.format(x), '$', method1(sample_payment_data, (2021, x), (2021, 12)).round(2))
    x += 1
print('\n\n')

# Calculating Cohort Lifetime Value Tables
active_subscribers_pyramid = cohort_signups_pyramid(sample_payment_data, sample_adds_data, sample_signups_data).fillna(0)
revenue_pyramid = cohort_revenue_pyramid(sample_payment_data, sample_adds_data, sample_signups_data).fillna(0)
ARPU_pyramid = revenue_pyramid.div(signups_pyramid.values).fillna(0)
ARPU_pyramid.rename(index={'Revenue:':'ARPU:'}, inplace=True)

print(active_subscribers_pyramid, '\n\n')
print(revenue_pyramid, '\n\n')
print(ARPU_pyramid)
