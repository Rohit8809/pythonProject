from crontab import CronTab

# Initialize the cron tab using a file to simulate crontab in Windows
cron = CronTab(tabfile='my_cron.tab')  # Specify a tabfile instead of user

# Add a new cron job with corrected file path
job = cron.new(command=r'python D:\Project\pythonProject\news.py', comment='News scheduler')

# Set the job schedule (e.g., every day at 2 AM)
job.setall('0 2 * * *')

# Write the job to the tabfile
cron.write()

print("Cron job added successfully to the tabfile!")
