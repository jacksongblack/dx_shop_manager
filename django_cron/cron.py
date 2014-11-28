#coding=utf-8

from django_cron import CronJobBase, Schedule

class TestCronJob(CronJobBase):
    """
    10分钟清理一次
    """
    RUN_EVERY_MINS = 10*60

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'django_cron.TestCronJob'

    def do(self):
        print 'do test cron job!'
  
