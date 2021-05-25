# Cohort-Lifetime-Analysis
Several methods for counting and computing cohorts by month via signups, revenue, and average revenue per user.


### Features

- Several different methods to calculate average revenue per user as well as total revenue and signup counts.
- Monthly cohort revenue table as well as monthly cohort survivor table

#### Notes:
- ARPU = Average Revenue Per User
- This model uses three datasets: payment data, signup data, and netadd data.
- The model can be used with any date range and tables dynamically refresh to ordered set of months found in data. (Ideal for Cronjobs)
- While the production model uses a rolling archetype such that it predicts the next week out each day. 
- All data has been mutated such that it is not representative of any real-world company's value.

### Example Demo Outputs

![Raw Output to console:](https://github.com/kanerhee/Cohort-Lifetime-Analysis/blob/main/static/raw_output.png)
![Signups Pyramid](https://github.com/kanerhee/Cohort-Lifetime-Analysis/blob/main/static/Signups_dataframe.png)
![Revenue Pyramid](https://github.com/kanerhee/Cohort-Lifetime-Analysis/blob/main/static/Revenue_dataframe.png)
![ARPU Pyramid](https://github.com/kanerhee/Cohort-Lifetime-Analysis/blob/main/static/ARPU_dataframe.png)
