from django.db import models
from django.contrib.auth.models import User

import json

class History(models.Model):
    """
    The class belongs to a table containing all processes, which were started with analyze.
    """
    class Meta:
        """
        Set the user's permissions
        """
        permissions = (
                       ('history_submit_job', 'Can submit a job'),
                       ('history_cancel_job', 'Can cancel a job'),
                       ('browse_full_data', 'Can search all data'),
                      )


    #: Date and time when the process were scheduled
    timestamp       = models.DateTimeField()
    #: Name of the tool
    tool            = models.CharField(max_length=50)
    #: Version of the tool
    version         = models.CharField(max_length=10)
    #: The configuration this can be quiet lengthy
    configuration   = models.TextField()
    #: Output file generated by SLURM 
    slurm_output    = models.TextField()
    #: User ID
    uid             = models.ForeignKey(User, null=True, to_field='username', db_column='uid')#models.CharField(max_length=20)
    #: Status (scheduled, running, finished, cancelled)
    status          = models.IntegerField(max_length=1)

    
    def __init__(self, *args, **kwargs):
        """
        Creates a dictionary for projectStatus
        """
        self.status_dict = dict()
        public_props = (name for name in dir(self.processStatus) if not name.startswith('_'))
        for name in public_props:
            self.status_dict[getattr(self.processStatus,name)] = name
        
        super(History, self).__init__(*args, **kwargs)
        
    def slurmId(self):
        #import string
        #alle = string.maketrans('','')
        #nodigs = alle.translate(alle, string.digits)
        #slurm_file = str(self.slurm_output)
        #slurm_file = '12312aasdas'
        return self.slurm_output[-8:-4]    
        

    def config_dict(self):
        """
        Converts the configuration to a dictionary
        """
        return json.loads(self.configuration)

    def status_name(self):
        """
        Returns status as string
        """    
        return self.status_dict[self.status]

        

    class processStatus:
        """
        The allowed statuses
        finished           - the process finished and produced output files
        finished_no_output - the process finished, but no output files were created
        scheduled          - the job was send to slurm
        running            - the job is executed
        broken             - an exception occurred
        not_scheduled      - an error occurred during scheduling
        """
        finished, finished_no_output, broken, running, scheduled, not_scheduled = range(6)
        
        
            

class Result(models.Model):
    """
    This class belongs to a table storing results.
    The output files of process will be recorded here.
    """
    #: history id
    history_id      = models.ForeignKey(History)
    #: path to the output file
    output_file     = models.TextField()
    #: path to preview file
    preview_file    = models.TextField(default='')
    #: specification of a file type 
    file_type       = models.IntegerField(max_length=2)
    
    class Meta:
        """
        Set the user's permissions
        """
        permissions = (
                       ('results_view_others', 'Can view results from other users'),
                      )

    class Filetype:
        """
        Different IDs of file types
        data      - ascii or binary data to download
        plot      - a file which can be converted to a picture
        preview   - a local preview picture (copied or converted) 
        """
        data, plot, preview = range(3)
        

    def fileExtension(self):
        """
        Returns the file extension of the result file
        """
        from os import path
        return path.splitext(self.output_file)[1]
    
    # some not yet implemented ideas
    ##: Allows a logical clustering of results
    # group           = models.IntegerField(max_length=2)
    ##: Defines an order for each group
    # group_order     = models.IntegerField(max_length=2)
