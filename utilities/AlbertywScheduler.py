#! /usr/bin/python -O
"""
This program runs on albertyw.mit.edu and
1.  Receives jobs from the main Scheduler.py on coyote
2.  Runs the jobs on albertyw
"""
import subprocess
import time
import os

base_directory = "/home/albertyw/crank_jobs/"

class AlbertywScheduler:
    
    def __init__(self, base_directory):
        self.base_directory = base_directory
        self.status_file = self.base_directory+'status'
        self.currently_running = dict({})
        self.max_running = 4
        
    def run(self):
        """
        Continuously look for new jobs and update the node status
        """
        self.write_status()
        while True:
            self.find_new_runs()
            time.sleep(5)
            
    def find_new_runs(self):
        """
        Loop through the runs in /base_directory/* to find_new_jobs
        """
        runs = os.listdir(self.base_directory)
        runs = [self.base_directory+run+'/' for run in runs]
        if self.status_file+'/' in runs:
            runs.remove(self.status_file+'/')
        for run in runs:
            self.find_new_jobs(run)
        
    def find_new_jobs(self, run):
        """
        Loop through jobs and check whether they've finished running/need to be 
        submitted
        """
        jobs = os.listdir(run)
        if 'GenesFile' in jobs:
            jobs.remove('GenesFile')
        jobs = [run+job+'/' for job in jobs]
        for job in jobs:
            files = os.listdir(job)
            if job in self.currently_running and 'submitted' in files and 'output' in files:
                self.currently_running[job].communicate()
                del self.currently_running[job]
                self.write_status()
            if len(self.currently_running) < self.max_running and 'submitted' not in files:
                runner = self.submit_job(job)
                if runner != None:
                    self.currently_running[job] = runner
                self.write_status()
            
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
            
            command = ['nice','-n','19','sh', input_shell_location]
            runner = subprocess.Popen(command)
            return runner
        else:
            return None
            
    def write_status(self):
        """
        Write the current status of the jobs
        """
        status_file_handle = open(self.status_file,'w')
        status_file_handle.write(str(self.max_running - len(self.currently_running)))
        status_file_handle.close()


if __name__ == "__main__":
    print 'AlbertywScheduler'
    scheduler = AlbertywScheduler(base_directory)
    scheduler.run()
    
