from smart_algorithym import SmartAlgorithym
from apscheduler.schedulers.background import BackgroundScheduler
import time

# 1. Crear objeto algoritmo
al = SmartAlgorithym()

# 2. Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(al.bucle_normal, 'cron', hour='*')
scheduler.add_job(al.set_irradiance_next_hour, 'cron', hour='*', minute='58')
scheduler.add_job(al.charge_battery_night,'cron', minute='*', second='30')
scheduler.start()

print('Starting')
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

scheduler.shutdown()