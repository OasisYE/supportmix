import ConfigParser
import sys
import os


def createDataPath(dataPath='data'):
    """Returns the Current Path of the "executable" """
    #Check if running from the binary
    frozen = getattr(sys, 'frozen', None)
    if frozen:
        programPath= os.path.split(__file__.replace("%slibrary.zip"%os.path.sep,""))[0]
    else:
        programPath= os.path.split(__file__)[0]
    return os.path.join(programPath, dataPath)


def readConfig(configFile="SupportMix.cfg"):
    config=ConfigParser.ConfigParser()
    config.read(configFile)
    return config

#def validateConfig(configFile):
#    config=readConfig()


#--- TODO:  Add support for reading plot options
#    group = OptionGroup(parser, 'Plotting Options', 'Use these options to generate graphics and customize graphics.'
#                    'It is believed that some of them bite.')
#    group.add_option('-p', '--plot', dest='doPlot', action='store_true', default=False,
#                      help='Generate graphical output')
#    group.add_option('--RGB', type='string',  dest='rgb', action='callback', callback=optColorProcessor, 
#                      help='Color specifications of different populations for graphing : ', metavar='colors')
#    group.add_option('--labels', type='string', dest='labels', action='callback', callback=optLabelProcessor,
#                      help='populations labels for graphing Example: ceu,yri,mkk', metavar='labels')
#    parser.add_option_group(group)
#    (options, args) = parser.parse_args()

    
def getConfigOptions(configFile):
    
    config=readConfig(configFile)
    configData={}
    
    if config.has_option('parameters', 'chromosome'):
        configData['chrom']=config.getint('parameters', 'chromosome')
    else:
        configData['chrom']=0
    
    if config.has_option('parameters', 'window'):
        configData['win']=config.getint('parameters','window')
    else:
        configData['win']=100
    
    if config.has_option('parameters','generations'):
        configData['nGens']=config.getfloat('parameters','generations')
    else:
        configData['nGens']=6.0
        
    if config.has_option('parameters','saveFile'):
        configData['saveFile']=config.get('parameters','saveFile')
    else:
        configData['saveFile']='outSupportMix'
    
    #File related processing
    if config.has_section('data location'):
        baseDataDir=config.get('data location','baseDataDir')
    else:
        baseDataDir=None
    
    #here we assume that all the files including the ancestry file are located 
    #in the data path
    #If the ancestry file's full path is specified the path will be used instead.
    #Otherwise will try to locate the file in the data dir
    
#    if config.has_option('parameters','ancestryFile'):
    
    ancestryFile=config.get('parameters','ancestryFile')
    
    if os.path.exists(ancestryFile):
        configData['correctFile']=ancestryFile
    
    elif baseDataDir!=None:
        #Check for ancestry file in data path
        ancestryFile=os.path.join(baseDataDir,ancestryFile)
        if os.path.exists(ancestryFile):
            configData['correctFile']=ancestryFile
        else:
            raise ConfigParser.Error("Can't find Ancestry File")
            
    
    
    fileNames=[]
    admixed=None
    for item in config.items('input'):
        fileItem=item[1]
        
        if baseDataDir!=None:
            fileItem=os.path.join(baseDataDir,fileItem)
        #Validate file existence
        if not os.path.exists(fileItem):
            raise ConfigParser.Error("Can't find file: %s"%fileItem)
            
        if item[0]!='admixed':
            fileNames.append(fileItem)
        else:
            admixed=fileItem
    
    if admixed:
        fileNames.append(admixed)
    else:
        raise ConfigParser.Error("Admixed population not defined")
    
    configData['fileNames']=fileNames
    
    if config.has_section('plot options'):
        #configData['doPlot']=config.getboolean('plot options', 'plot')
        
        if config.has_option('plot options', 'plot'):
            configData['doPlot']=config.get('plot options', 'plot')
        else:
            configData['doPlot']=None
        
        if config.has_option('plot options', 'RGB'):
            configData['RGB']=config.get('plot options', 'RGB')
            configData['doPlot']=True
        else:
            configData['RGB']=None
        
        if config.has_option('plot options', 'labels'):
            configData['labels']=config.get('plot options', 'labels')
            configData['doPlot']=True
        else:
            configData['labels']=None
        
    return configData
    

if __name__ =="__main__":
   
    print getConfigOptions("supportMix.cfg")
    
