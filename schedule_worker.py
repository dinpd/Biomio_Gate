from biomio.worker.scheduler_interface import SchedulerInterface

if __name__ == '__main__':
    scheduler_interface = SchedulerInterface.instance()
    scheduler = scheduler_interface.get_scheduler_instance()
    scheduled_jobs = scheduler.get_jobs()
    for scheduled_job in scheduled_jobs:
        scheduler.cancel(scheduled_job)
    scheduler_interface.schedule_required_jobs()
    scheduler.run()
