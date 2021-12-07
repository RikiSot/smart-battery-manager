from smart_algorithym import SmartAlgorithym
from apscheduler.schedulers.background import BackgroundScheduler
import time

# 1. Crear objeto algoritmo
al = SmartAlgorithym()

# 2. Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(al.bucle_test, 'cron', hour='*')
scheduler.add_job(al.set_irradiance_next_hour, 'cron', hour='*', minute='55')
scheduler.add_job(al.charge_battery_night,'interval', minutes=15)
scheduler.start()

print('Starting')
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

scheduler.shutdown()