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
@sched.scheduled_job('date', run_date='2019-7-17 10:20:00', misfire_grace_time=18000)
def date_job():
    print('Running at a specific date')
        

'''
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')
'''
sched.print_jobs()
sched.start()

