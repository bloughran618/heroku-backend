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
print("configured")

'''
@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every minute.')
'''

def my_job(text):
    print(text)

def add_jobs():
    print("scheduling")
    sched.add_job(my_job, 'date', run_date='2019-7-17 17:41:00', args=['date job firing'], id = "Job3", misfire_grace_time = 18000)
    sched.add_job(my_job, 'date', run_date='2019-7-17 17:42:00', args=['date to run'], id = "Job4", misfire_grace_time=18000)
    sched.add_job(my_job, 'date', run_date='2019-7-17 17:43:00', args=['job after shutdown'], id = 'Job5', misfire_grace_time = 18000)
    
'''
@sched.scheduled_job('date', run_date='2019-7-17 10:40:00', misfire_grace_time=18000)
def date_job():
    print('Running at a specific date')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=13, misfire_grace_time = 18000)
def scheduled_job():
    print('This job is run every weekday at 5pm.')
'''

if __name__ == '__main__':
    add_jobs()
    sched.start()
    sched.print_jobs()

