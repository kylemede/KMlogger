import kmLogger

def main():
    print '\nGet a logging object with stream level set to 0, and no file handler.'
    log = kmLogger.getLogger('main',lvl=0,addFH=False)
    
    # print a message for each level
    print '\nPrint a message for each level:\n'
    log.raisemsg('This is a raisemsg level (99) message')
    log.critical('This is a critical level (50) message')
    log.error('This is an error level (40) message')
    log.warning('This is a warning level (30) message')
    log.importantinfo('this is an importantinfo level (25) message')
    log.info('This is a info level (20) message')
    log.debug('This is a debug level (10) message')
    log.fileonly('This is a fileonly level (1) message')

    #Change the stream handler level
    print '\nChange stream handler level to 20'
    log.setStreamLevel(lvl=20)
    # print each message again to see what ones show up.
    print '\nPrint a message for each level:\n'
    log.raisemsg('This is a raisemsg level (99) message')
    log.critical('This is a critical level (50) message')
    log.error('This is an error level (40) message')
    log.warning('This is a warning level (30) message')
    log.importantinfo('this is an importantinfo level (25) message')
    log.info('This is a info level (20) message')
    log.debug('This is a debug level (10) message')
    log.fileonly('This is a fileonly level (1) message')
    
    
    print 'Add a file handler to logging object.'
    log.addFileHandler()




if __name__ == '__main__':
    main()