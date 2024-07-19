import schedule
import time
from datetime import datetime, timedelta
import subprocess

def job():
    subprocess.run(['python', 'psi_link.py'])

# Время начала выполнения скрипта
start_time = datetime.now()
# Время окончания через 24 часа
end_time = start_time + timedelta(hours=24)

# Запуск первой задачи сразу
job()

# Планирование задачи каждые 20 минут
schedule.every(20).minutes.do(job)

# Запуск цикла планировщика
while datetime.now() < end_time:
    schedule.run_pending()
    time.sleep(1)

print("24 часа завершены, скрипт остановлен.")