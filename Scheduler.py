"""
Submit Jobs To The Queue

Albert Wang
December 27, 2010
"""
import os
import subprocess
import random
import tempfile
import time

class Scheduler:
    """
    This class is used to submit jobs to the job queue.  Other classes should 
    submit jobs through this class instead of implementing their own job 
    submission code
    """
    def __init__(self, queue_name, shell_file_directory, use_darwin=False, \
            use_albertyw=False, use_mitmunc=False, genes_file_location=None, \
            species_trees_per_job=1):
        """
        Initialize some variables used with job submission
        """
        self.internal_queue_list  = []
        self.queue_name           = queue_name
        self.queue_dict           = dict({'speedy':30*60,\
                                          'quick':3*60*60,\
                                          'short':12*60*60,\
                                          'long':48*60*60,\
                                          'ultra':336*60*60})
        self.file_number = 0
        self.job_script_location   = os.path.dirname(__file__)+"/Job.py"
        self.shell_file_directory  = shell_file_directory
        self.use_darwin            = use_darwin
        self.use_albertyw          = use_albertyw
        self.use_mitmunc           = use_mitmunc
        self.use_local_node        = False
        self.species_trees_per_job = species_trees_per_job
        self.darwin_directory      = '/home/albertyw/crank_jobs/'
        self.albertyw_directory    = '/home/albertyw/crank_jobs/'
        self.mitmunc_directory     = '/home/albertyw/crank_jobs/'
        if self.use_darwin:
            self.setup_darwin(genes_file_location)
        if self.use_albertyw:
            self.setup_albertyw(genes_file_location)
        if self.use_mitmunc:
            self.setup_mitmunc(genes_file_location)
    
    def submit_job(self, input_file_location):
        """
        Submit a job to the internal queue.  Scheduler will keep the jobs until 
        run_job is called.  shell_file_location is the actuall shell command to 
        be run.  
        """
        self.internal_queue_list.append(input_file_location)
        
    def run_job(self):
        """
        Submit all the internally queued jobs to the outside queue to be run
        """
        old_files = self.file_number
        darwin_empty_spots = -999999
        albertyw_empty_spots = -9999999
        mitmunc_empty_spots = -9999999
        local_node_empty_spots = -999999
        while self.file_number - old_files < len(self.internal_queue_list):
            local_empty_spots = 128 - self.local_queue_status()
            if self.use_darwin:
                darwin_empty_spots = 484 - self.darwin_queue_status()
            if self.use_albertyw:
                albertyw_empty_spots = self.albertyw_node_status()
            if self.use_mitmunc:
                mitmunc_empty_spots = self.mitmunc_node_status()
            if self.use_local_node:
                local_node_empty_spots = 4 - self.local_node_status()
                
            queue_id = self.file_number - old_files
            input_file_locations = self.internal_queue_list[queue_id:min(len(self.internal_queue_list), queue_id+self.species_trees_per_job)]
            if self.use_local_node and local_node_empty_spots > 0:
                self.submit_local_node(input_file_locations)
            elif self.use_albertyw and albertyw_empty_spots > 0:
                self.submit_albertyw_node(input_file_locations)
            elif self.use_mitmunc and mitmunc_empty_spots > 0:
                self.submit_mitmunc_node(input_file_locations)
            elif local_empty_spots > 0:
                self.submit_local_queue(input_file_locations)
            elif self.use_darwin and darwin_empty_spots > 0:
                self.submit_darwin_queue(input_file_locations)
            else:
                time.sleep(10)
                continue
            self.file_number += self.species_trees_per_job
            time.sleep(1)
        self.internal_queue_list = []
        
    def submit_local_queue(self, input_file_locations, submit_to_queue = 'local'):
        """
        This method will submit jobs to the local queue to run
        """
        # Create the shell file to be submitted
        finished_directory = self.shell_file_directory+'/finished/'
        shell_file_location = self.shell_file_directory+'/'+str(self.file_number)+'.sh'
        finished_location = finished_directory+'/'+str(self.file_number)+'.sh'
        finished_output_location = 'coyote.mit.edu:'+finished_directory+'/'+str(self.file_number)+'o.sh'
        finished_error_location = 'coyote.mit.edu:'+finished_directory+'/'+str(self.file_number)+'e.sh'
        input_file_text = "#! /bin/sh\n"
        input_file_text += "# Submitted to "+submit_to_queue+"\n"
        input_file_text += "set -e\n"
        for input_file_location in input_file_locations:
            input_file_text += "python "+self.job_script_location+" "+input_file_location+"\n"
        input_file_text += "mv "+shell_file_location+' '+finished_location+"\n"
        input_file_handle = open(shell_file_location,'w')
        input_file_handle.write(input_file_text)
        input_file_handle.close()
        
        if submit_to_queue == 'local':
            # Submit to queue
            qstat = ['qsub', '-q', self.queue_name, '-o', finished_output_location,\
                '-e', finished_error_location, '-m', 'n', '-M', 'albertyw@mit.edu', shell_file_location]
            job = subprocess.Popen(qstat, stdout=subprocess.PIPE)
            job.wait()
        return shell_file_location
    
    def submit_darwin_queue(self, input_file_locations):
        address = 'beagle.darwinproject.mit.edu'
        submit_external_node(input_file_locations, address, self.darin_directory)
        
    def submit_albertyw_node(self, input_file_locations):
        address = 'albertyw.mit.edu'
        submit_external_node(input_file_locations, address, self.albertyw_directory)
        
    def submit_mitmunc_node(self, input_file_locations):
        address = 'mitmunc.mit.edu'
        submit_external_node(input_file_locations, address, self.mitmunc_directory)
        
    def submit_external_node(self, input_file_locations, address, external_directory):
        """
        This method will run the job on an external node without qsub
        """
        # Make local shell file
        local_shell_location = self.submit_local_queue(input_file_location, address)
        job_directory_locations = []
        for i in range(len(input_file_locations)):
            input_file_location = input_file_locations[i]
            # Make job directory
            job_directory_location = external_directory+str(self.file_number+i)+'/'
            command = ['ssh',address,'mkdir '+job_directory_location]
            output = subprocess.Popen(command, stdout = subprocess.PIPE)
            output = output.stdout.read()
            # Modify input file
            input_file_handle = open(input_file_location,'r')
            input_file = input_file_handle.readlines()
            input_file_handle.close()
            coyote_output_location = input_file[4]
            input_file[1] = external_directory+"GenesFile\n"
            input_file[4] = job_directory_location+"output\n"
            # Copy input file to external node
            temp = tempfile.NamedTemporaryFile()
            temp.write(''.join(input_file))
            temp.seek(0)
            command = ['scp',temp.name,address+':'+job_directory_location+'input']
            output = subprocess.Popen(command, stdout = subprocess.PIPE)
            output = output.stdout.read()
            temp.close()
            
            job_directory_locations.append((job_directory_location, coyote_output_location))
        # Make remote shell file
        shell_file_location = job_directory_location+'crank'+str(self.file_number)+'.sh'
        shell_file_text = "#! /bin/sh\n"
        shell_file_text += "set -e\n"
        for job_directory_location, coyote_output_location in job_directory_locations:
            shell_file_text += "python /home/albertyw/crank/Job.py "+job_directory_location+"input\n"
            shell_file_text += "scp "+job_directory_location+"output coyote.mit.edu:"+coyote_output_location+"\n"
        shell_file_text += "ssh coyote.mit.edu 'rm "+local_shell_location+"'\n"
        # Copy shell file to external node
        temp = tempfile.NamedTemporaryFile()
        temp.write(shell_file_text)
        temp.seek(0)
        command = ['scp',temp.name,address+':'+shell_file_location]
        output = subprocess.Popen(command, stdout = subprocess.PIPE)
        output = output.stdout.read()
        temp.close()
    
    def submit_local_node(self, input_file_locations):
        """
        This method will run the job on the current node without qsub
        This may not be a good idea
        """
        shell_file_location = self.submit_local_queue(input_file_locations, submit_to_queue="local_node")
        
        finished_directory = self.shell_file_directory+'/finished/'
        shell_file_location = self.shell_file_directory+'/'+str(self.file_number)+'.sh'
        finished_location = finished_directory+'/'+str(self.file_number)+'.sh'
        finished_output_location = finished_directory+'/'+str(self.file_number)+'o.sh'
        finished_error_location = finished_directory+'/'+str(self.file_number)+'e.sh'
        
        # Submit to local node
        qstat = ['sh', shell_file_location, '>', finished_output_location, \
            '2>', finished_error_location]
        job = subprocess.Popen(qstat, subprocess.PIPE)
    
    def wait_until_finish(self):
        """
        This method won't do anything but will keep on running until all the 
        jobs in the queue are finished.  It does this by querying for files in 
        the shell_file_directory
        """
        while len(os.listdir(self.shell_file_directory)) > 1:
            time.sleep(10)
        
    def local_queue_status(self):
        """
        Get the length of the queue at the current time
        """
        p = subprocess.Popen(['qstat'], stdout = subprocess.PIPE)
        queue_length = p.stdout.read().count("\n")
        return int(queue_length)-2
        
    def darwin_queue_status(self):
        """
        Get the length of the darwin queue at the current time
        """
        p = subprocess.Popen(['ssh','beagle.darwinproject.mit.edu','cat qstat'], stdout=subprocess.PIPE)
        queue_length = p.stdout.read()
        try:
            queue_length = int(queue_length)
        except ValueError:
            queue_length = 999999999
        return queue_length
        
    def albertyw_node_status(self):
        """
        Get the number of free spots on albertyw.mit.edu at the current time
        """
        try:
            p = subprocess.Popen(['ssh','albertyw.mit.edu','cat '+'/home/albertyw/crank_jobs/status'], stdout=subprocess.PIPE)
            load = p.stdout.read()
            return int(load)
        except ValueError:
            return 0
            
    def mitmunc_node_status(self):
        """
        Get the number of free spots on mitmunc.mit.edu at the current time
        """
        try:
            p = subprocess.Popen(['ssh','mitmunc.mit.edu','cat '+'/home/albertyw/crank_jobs/status'], stdout=subprocess.PIPE)
            load = p.stdout.read()
            return int(load)
        except ValueError:
            return 0
    
    def local_node_status(self):
        """
        Get the load on the current node at the current time
        """
        p = subprocess.Popen(['cat','/proc/loadavg'], stdout=subprocess.PIPE)
        load = p.stdout.read()
        load = load[:load.find('.')]
        return int(load)
        
    def setup_darwin(self, genes_file_location):
        """
        Set up directories in darwin so that darwin can be used for testing
        """
        # Find good location on darwin
        output = subprocess.Popen(['ssh','beagle.darwinproject.mit.edu','ls '+self.darwin_directory], stdout=subprocess.PIPE)
        output = output.stdout.read()
        i = 0
        while str(i) in output:
            i += 1
        self.darwin_directory = self.darwin_directory+str(i)+'/'
        command = ['ssh','beagle.darwinproject.mit.edu','mkdir '+self.darwin_directory]
        output = subprocess.Popen(command, stdout = subprocess.PIPE)
        output.stdout.read()
        # Copy GenesFile to Darwin
        command = ['scp',genes_file_location,'beagle.darwinproject.mit.edu:'+self.darwin_directory+'GenesFile']
        output = subprocess.Popen(command, stdout = subprocess.PIPE)
        output = output.stdout.read()
        
    def setup_albertyw(self, genes_file_location):
        """
        Set up directories in albertyw so that albertyw can be used for testing
        """
        # Find good location on albertyw
        output = subprocess.Popen(['ssh','albertyw.mit.edu','ls '+self.albertyw_directory], stdout=subprocess.PIPE)
        output = output.stdout.read()
        i = 0
        while str(i) in output:
            i += 1
        self.albertyw_directory = self.albertyw_directory+str(i)+'/'
        command = ['ssh','albertyw.mit.edu','mkdir '+self.albertyw_directory]
        output = subprocess.Popen(command, stdout = subprocess.PIPE)
        output.stdout.read()
        # Copy GenesFile to Albertyw
        command = ['scp',genes_file_location,'albertyw.mit.edu:'+self.albertyw_directory+'GenesFile']
        output = subprocess.Popen(command, stdout = subprocess.PIPE)
        output = output.stdout.read()
        
    def setup_mitmunc(self, genes_file_location):
        """
        Set up directories in mitmunc so that mitmunc can be used for testing
        """
        # Find good location on albertyw
        output = subprocess.Popen(['ssh','mitmunc.mit.edu','ls '+self.mitmunc_directory], stdout=subprocess.PIPE)
        output = output.stdout.read()
        i = 0
        while str(i) in output:
            i += 1
        self.mitmunc_directory = self.mitmunc_directory+str(i)+'/'
        command = ['ssh','mitmunc.mit.edu','mkdir '+self.mitmunc_directory]
        output = subprocess.Popen(command, stdout = subprocess.PIPE)
        output.stdout.read()
        # Copy GenesFile to MITMUNC
        command = ['scp',genes_file_location,'mitmunc.mit.edu:'+self.mitmunc_directory+'GenesFile']
        output = subprocess.Popen(command, stdout = subprocess.PIPE)
        output = output.stdout.read()
        
    def check_albertyw(self):
        """
        Check whether albertyw is up so that albertyw can be used for testing
        """
        
        
    def check_darwin(self):
        """
        Check whether darwin is up so that darwin can be used for testing
        """
        
        
if __name__ == "__main__":
    schedule = Scheduler('.','.')
    print 'Local Queue Length/Free'
    n = schedule.local_queue_status()
    print n, (100-n)
    print 'Darwin Queue Length/Free'
    n = schedule.darwin_queue_status()
    print n, 484 - n
    print 'Albertyw Node Length/Free'
    n = schedule.albertyw_node_status()
    print 4-n, n
    print 'MITMUNC Node Length/Free'
    n = schedule.mitmunc_node_status()
    print 4-n, n
    print 'Local Node Length/Free'
    n = 8-n, n
    print schedule.local_node_status()
