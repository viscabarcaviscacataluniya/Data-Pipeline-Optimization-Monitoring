from datetime import datetime

def assess_day(execution_date):
    date = datetime.strptime(execution_date, "%Y-%m-%d") 

    if date.isoweekday() < 6:
        return ['submit_weekday_job_1', 'submit_weekday_job_2', 'submit_weekday_job_3']
    else:
        return 'submit_weekend_job'