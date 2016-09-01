#@Author: Kyle Mede, kylemede@astron.s.u-tokyo.ac.jp
from __future__ import absolute_import
import logging
import platform
import datetime
import sys
import os
from six.moves import range
#import traceback

log_dict={}

class KMlogger(logging.getLoggerClass()):
    """
    This is the advanced logging object developed by:
    Kyle Mede, kylemede@astron.s.u-tokyo.ac.jp.  
    It inherits from the standard Python library 'logging' and provides 
    added features. The default log level for the output file will be 1, 
    ie ALL messages; while the default for the screen will be INFO, and can 
    be changed easily using the setStreamLevel(lvl) member function.
    """       
    
    def addNewLvls(self):
        """
        +---------------------+----------------------+
        |    Standard Levels  |        New Levels    |
        +---------------+-----+----------------+-----+
        |    Name       |Level|  Name          |Level|
        +===============+=====+================+=====+
        |               |     |RAISEMSG        | 99  |
        +---------------+-----+----------------+-----+
        |CRITICAL       |  50 |                |     | 
        +---------------+-----+----------------+-----+
        |ERROR          |  40 |                |     |
        +---------------+-----+----------------+-----+
        |WARNING        |  30 |                |     |
        +---------------+-----+----------------+-----+
        |               |     |IMPORTANTINFO   | 25  |
        +---------------+-----+----------------+-----+
        |INFO           |  20 |                |     |
        +---------------+-----+----------------+-----+
        |DEBUG          |  10 |                |     |
        +---------------+-----+----------------+-----+
        |               |     |FILEONLY        |  1  |
        +---------------+-----+----------------+-----+
        |NOTSET         |  0  |                |     |
        +---------------+-----+----------------+-----+
        """
        # Level for raise message to print to file (File only)
        RAISEMSG = 99
        logging.addLevelName(RAISEMSG, 'RAISEMSG')
        def raisemsg(self,msg,lvl=RAISEMSG, *args, **kws):
            self.log(lvl,msg, *args, **kws)
        logging.Logger.raisemsg = raisemsg
        # Level for minimal info more important than standard INFO level
        IMPORTANTINFO = 25
        logging.addLevelName(IMPORTANTINFO, 'IMPORTANTINFO')
        def importantinfo(self,msg,lvl=IMPORTANTINFO, *args, **kws):
            self.log(lvl,msg, *args, **kws)
        logging.Logger.importantinfo = importantinfo
        # Level for message to ONLY be written to file and not the screen
        FILEONLY = 1
        logging.addLevelName(FILEONLY, 'FILEONLY')
        def fileonly(self,msg,lvl=FILEONLY, *args, **kws):
            self.log(lvl,msg, *args, **kws)
        logging.Logger.fileonly = fileonly
        
    
    def setStreamLevel(self,lvl=20):
        """
        Set/change the level for the stream handler for a logging object.
        Any file handlers will be left alone.
        All messages of a higher severity level than 'lvl' will be printed 
        to the screen.
        
        Args:    
            lvl (int): The severity level of messages printed to the screen with 
                    the stream handler, default = 20.
        """
        # Kill off the old handlers and reset them with the setHandlers func
        for i in range(0,len(self.handlers)):
            h = self.handlers[i]
            if isinstance(h,logging.StreamHandler):
                self.removeHandler(h)
                break
        self.addStreamHandler(lvl)
        
    def getStreamLevel(self):
        """
        Get and return current stream handler's level.
        """
        shlvl = 0
        for i in range(0,len(self.handlers)):
            h = self.handlers[i]
            if isinstance(h,logging.StreamHandler):
                shlvl = h.level
        return shlvl
    
    def addFileHandler(self,filename='', dr='',lvl=1):
        """
        This function will add a file handler to a log with the provided level.
        
        Args:
            lvl (int): The severity level of messages printed to the file with 
                        the file handler, default = 1.
        """
        fname = self.name
        if filename != '':
            fname = filename
        if '.' not in fname:
            fname+='.log'
        fh = logging.FileHandler(os.path.join(dr,fname))
        fh.setLevel(lvl)
        frmtString = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        fFrmt = logging.Formatter(frmtString)
        fh.setFormatter(fFrmt)
        self.addHandler(fh)
    
    def addStreamHandler(self,lvl=20):
        """
        This function will add a stream handler to a log with the provided level.
        
        Args:
            lvl (int): The severity level of messages printed to the screen with 
                        the stream handler, default = 20.
        """
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(lvl)
        sFrmt = logging.Formatter('%(message)s')
        if False:
            #Another format example
            sFrmt = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        sh.setFormatter(sFrmt)
        self.addHandler(sh)   
        
    def logSystemInfo(self):
        """ 
        A function to be called just after a logging object is instantiated 
        to load the log up with info about the computer it is 
        being ran on and the software version.  This function utilizes the 
        psutil and platform libraries, so they must be install for it to work.  
        For clarity of the log, it is suggested to perform immediately after 
        instantiation to put it at the top of the log file.

                                        
        The messages this prints to the log will look like:
        
        | System Information Summary:
        | OS type = Linux
        | OS Version = 3.9.10-100.fc17.x86_64
        | Machine UserName = xxxxxx.astron.s.u-tokyo.ac.jp
        | Machine Processor Type = x86_64
        | Number of cores = 8
        | Total RAM [GB] = 23.5403785706, % used = 15.9
        | Python Version = '2.7.3'
    
        """
        t = datetime.date.today()
        infoStr = 'Date KMlogger object instantiated: '+t.strftime('%b %d, %Y')+'\n\n'
        infoStr+="\n"+"="*11+' System Information Summary '+'='*11
        infoStr+="\n"+'OS type = '+platform.uname()[0]
        infoStr+="\n"+'OS Version = '+platform.uname()[2]
        infoStr+="\n"+'Machine UserName = '+platform.uname()[1]
        infoStr+="\n"+'Machine Processor Type = '+platform.processor()
        try:
            #a quick fix as some macs have issues with psutil
            import psutil  
            infoStr+="\n"+'Number of cores = '+str(psutil.cpu_count())
        except:
            try:
                import multiprocessing
                multiprocessing.cpu_count()
            except:
                infoStr+="\n Both psutil and multiprocessing were unable to provide the number of CPUs."
        try:
            totMem = int(round(psutil.virtual_memory()[0]/1073741824.0))
            percentMem = int(round(psutil.virtual_memory()[2]))
            infoStr+="\n"+'Total RAM = '+str(totMem)+'[GB], with ~ '+str(percentMem)+"% already in use at simulation start"
        except:
            infoStr+="\n A problem with psutil occurred while investigating available RAM."
        infoStr+="\n"+'Python Version = '+repr(platform.python_version())
        infoStr+="\n"+'='*50
        self.fileonly(infoStr)
        
    def logDict(self,d):
        """
        Log all Key=value for every key in a dictionary.
          
        Args:
            d (dictionary): A standard python dictionary.
        """
        keys = list(d.keys())
        keys.sort()
        s = "\n"+"-"*78+"\n"+" "*20+"dictionary provided contains:\n"+"-"*78+"\n"
        for key in keys:
            s+=key+" = "+repr(d[key])+"\n"
        self.fileonly(s+"-"*78+"\n")
    
        
def getLogger(name='generalLoggerName',dr='',lvl=20,addFH=True,addSH=True,):
    """This will either return the logging object already
    instantiated, or instantiate a new one and return it.  
    **Use this function to both create and return any logger** to avoid 
    accidentally adding additional handlers by using the setUpLogger function 
    instead.
    
    Args:
        name (str): The name for the logging object and 
                    name.log will be the output file written to disk.
        lvl (int): The severity level of messages printed to the screen with 
                    the stream handler, default = 20.
        addFH (boolean): Add a file handler to this logger?  Default severity 
                         level for it will be 1, and it will be named following
                         name+'.log'.  Default = True.
        addSH (boolean): Add a stream handler to this logger? Severity set with 
                        the lvl argument.  Default = True.        
    Returns:
        log (KMlogger object): A KMlogger object that was either 
                                  freshly instantiated or determined to 
                                  already exist, then returned.
    """
    log = False
    try:
        log = log_dict[name]
    except:
        log = setUpLogger(name,dr,lvl,addFH,addSH)
    return log

def setUpLogger(name='generalLoggerName',dr='',lvl=20,addFH=True,addSH=True):
    """ This function is utilized by getLogger to set up a new logging object.
    It will have the default name 'generalLoggerName' and stream handler level
    of 20 unless redefined in the function call.  
    NOTE:
    If a file handler is added, it will have the lowest severity level by 
    default (Currently no need for changing this setting, so it will stay 
    this way for now).  Remember that any messages will be passed up to any 
    parent loggers, so children do not always need their own file handler.
    
    Args:
        name (str): The name for the logging object and 
                    name.log will be the output file written to disk.
        lvl (int): The severity level of messages printed to the screen with 
                    the stream handler, default = 20.
        addFH (boolean): Add a file handler to this logger?  Default severity 
                         level for it will be 1, and it will be named following
                         name+'.log'.  Default = True.
        addSH (boolean): Add a stream handler to this logger? Severity set with 
                        the lvl argument.  Default = True.
    Returns:
        log (KMlogger object): A KMlogger object that was freshly 
                                   instantiated.
    """
    logging.setLoggerClass(KMlogger)
    log = logging.getLogger(name)
    log_dict[name]=log
    log.addNewLvls()
    log.setLevel(1)
    # add the requested handlers to the log
    if addFH:
        log.addFileHandler(dr=dr,lvl=1)
    # make a stream handler
    if addSH:
        log.addStreamHandler(lvl)
    return log    
# END OF FILE    