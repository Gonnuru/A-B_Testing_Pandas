import pandas as pd

ad_clicks = pd.read_csv('ad_clicks.csv')

#Exploring first few rows of ad_clicks
print(ad_clicks.head())

# which ad Platoform is getting the most views?
views_count = ad_clicks.groupby('utm_source').user_id.count().reset_index()

# If the column ad_click_timestamp is not null, then someone actually clicked on the ad that was displayed.
ad_clicks['is_click'] = ~ad_clicks\
      .ad_click_timestamp\
      .isnull()

# We want to know the percent of people who clicked on ads from each utm_source.
click_by_source = ad_clicks.groupby(['utm_source', 'is_click']).user_id.count().reset_index()

#Pivot
clicks_pivot = click_by_source.pivot(
                columns = 'is_click',
                index = 'utm_source',
                values = 'user_id'
)

# Was there a difference in click rates for each source?
clicks_pivot['percent_clicked'] = clicks_pivot[True] / (clicks_pivot[True] + clicks_pivot[False])

print(clicks_pivot)
# The column experimental_group tells us whether the user was shown Ad A or Ad B.

# Were approximately the same number of people shown both adds?

print(ad_clicks.groupby('experimental_group').user_id.count().reset_index())

# check to see if a greater percentage of users clicked on Ad A or Ad B.
print(ad_clicks.groupby(['experimental_group','is_click'])
                .user_id.count().reset_index()
                .pivot(
                  index = 'experimental_group',
                  columns = 'is_click',
                  values = 'user_id'
                )
                .reset_index()
)   

# contain only the results for A group and B group, respectively.

a_clicks = ad_clicks[ad_clicks.experimental_group == 'A']
b_clicks = ad_clicks[ad_clicks.experimental_group == 'B']

a_clicks_pivot = a_clicks\
  .groupby(['is_click', 'day'])\
  .user_id.count()\
  .reset_index()\
  .pivot(
    index = 'day',
    columns = 'is_click',
    values = 'user_id'
  )\
  .reset_index()

# For each group (a_clicks and b_clicks), calculate the percent of users who clicked on the ad by day.
a_clicks_pivot['percent_clicked'] = a_clicks_pivot[True] / (a_clicks_pivot[True] + a_clicks_pivot[False])

print(a_clicks_pivot)

b_clicks_pivot = b_clicks\
  .groupby(['is_click', 'day'])\
  .user_id.count()\
  .reset_index()\
  .pivot(
    index = 'day',
    columns = 'is_click',
    values = 'user_id'
  )\
  .reset_index()

b_clicks_pivot['percent_clicked'] = b_clicks_pivot[True] / (b_clicks_pivot[True] + b_clicks_pivot[False])

print(b_clicks_pivot)














