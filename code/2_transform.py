import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here

survey_data = pd.read_csv('cache/survey.csv')

states_data = pd.read_csv('cache/states.csv')

years = survey_data['year'].unique()

cols=[]

for year in years:
    col = pd.read_csv(f'cache/col_{year}.csv')
    cols.append(col)

col_data = pd.concat(cols, ignore_index=False)

# create a new column with cleaned USA values
survey_data['_country'] = survey_data['What country do you work in?'].apply(pl.clean_country_usa)

# convert the states into state codes
survey_states_combined = pd.merge(left = survey_data, right = states_data, how = 'inner', left_on = "If you're in the U.S., what state do you work in?", right_on = "State")

# combine city, state code, and country into new column
survey_states_combined['_full_city'] = survey_states_combined["If you're in the U.S., what state do you work in?"] + ', ' + survey_states_combined['Abbreviation'] + ', ' + survey_states_combined['_country']

# merge the survey data with the cost of living data
combined = pd.merge(survey_states_combined, col_data, how = 'inner', left_on = ['year', '_full_city'], right_on = ['year', 'City'])

# clean the salary column for further processing
combined['__annual_salary_cleaned'] = combined["What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"].apply(pl.clean_currency)

# standardize annual salary based on COL
combined['_annual_salary_adjusted'] = combined.apply(lambda row: (100/row['Cost of Living Index']) * row['__annual_salary_cleaned'], axis = 1)

# output combined df to a CSV file
combined.to_csv('cache/survey_dataset.csv')

# create and export pivot table of cities, ages, and the means of average salaries
annual_salary_adjusted_by_location_and_age = combined.pivot_table(index = '_full_city', columns = 'How old are you?', values = '_annual_salary_adjusted', aggfunc = 'mean')
annual_salary_adjusted_by_location_and_age.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')

# create and export pivot table of cities, education, and means of average salaries
annual_salary_adjusted_by_location_and_education = combined.pivot_table(index = '_full_city', columns = 'What is your highest level of education completed?', values = '_annual_salary_adjusted', aggfunc = 'mean')
annual_salary_adjusted_by_location_and_education.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')