from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler


from stocks.tasks import monitor_price_quote

def start_scheduled_tasks():
    scheduler = BackgroundScheduler()
    scheduler.add_job(monitor_price_quote, CronTrigger.from_crontab('*/3 10-18 * * MON-FRI'), args=[3])
    scheduler.add_job(monitor_price_quote, CronTrigger.from_crontab('*/5 10-18 * * MON-FRI'), args=[5], minutes=5)
    scheduler.add_job(monitor_price_quote, CronTrigger.from_crontab('*/15 10-18 * * MON-FRI'), args=[15], minutes=15)
    scheduler.add_job(monitor_price_quote, CronTrigger.from_crontab('*/30 10-18 * * MON-FRI'), args=[30], minutes=30)
    scheduler.add_job(monitor_price_quote, CronTrigger.from_crontab('0 10-18 * * MON-FRI'), args=[60], minutes=60)
    scheduler.start()