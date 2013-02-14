#! /usr/bin/python -O
"""
This program runs on the Darwin cluster and
1.  Receives jobs from the main Scheduler.py on coyote
2.  Runs the jobs on Darwin
"""
import subprocess
import time
import os

base_directory = "/home/albertyw/crank_jobs/"

class DarwinScheduler:
    
    def __init__(self, base_directory):
        self.base_directory = base_directory
        
    def find_new_runs(self):
        runs = os.listdir(self.base_directory)
        runs = [self.base_directory+run+'/' for run in runs]
        for run in runs:
            self.find_new_jobs(run)
        
    def find_new_jobs(self, run):
        jobs = os.listdir(run)
        jobs = [run+job+'/' for job in jobs]
        for job in jobs:
            if 'GenesFile' in job:
                continue
            files = os.listdir(job)
            if 'submitted' not in files:
                self.submit_job(job)
        
    def run(self):
        while True:
            self.find_new_runs()
            time.sleep(10)
        
    def submit_job(self, job_location):
        print time.strftime("%Y-%m-%d %H:%M:%S  ") + job_location
        files = os.listdir(job_location)
        input_shell_location = ''
        for file_name in files:
            if '.sh' in file_name:
                input_shell_location = job_location + file_name
                break
        if input_shell_location != '':
            submitted = open(job_location+'submitted','w')
            submitted.write(' ')
            submitted.close()
            
            qsuber = ['qsub', input_shell_location, '-o', \
                input_shell_location+'o', '-e', input_shell_location+'e']
            qsuber = subprocess.Popen(qsuber, stdout=subprocess.PIPE)
            qsuber.wait()


if __name__ == "__main__":
    print 'DarwinScheduler'
    scheduler = DarwinScheduler(base_directory)
    scheduler.run()
    
