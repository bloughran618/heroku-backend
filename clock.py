'''Testing APScheduler as a seperate file for heroku'''


from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
job_defaults = {
    'coalesce': False,
    'max_instances': 1
}

sched = BlockingScheduler()
sched.configure(jobstores=jobstores, job_defaults=job_defaults, timezone='America/New_York')
'''
@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every minute.')
'''

def my_job(text):
    print(text)

sched.add_job(my_job, 'date', run_date='2019-7-17 11:15:00', args=['date job firing'], misfire_grace_time = 18000)
sched.add_job(my_job, 'date', run_date='2019-7-17 12:30:00', args=['date to run after sleeping'], misfire_grace_time=18000)

'''
@sched.scheduled_job('date', run_date='2019-7-17 10:40:00', misfire_grace_time=18000)
def date_job():
    print('Running at a specific date')
'''        
print("scheduled date job")

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=13)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()

