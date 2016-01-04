from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, event, gui, sound, data, logging
from psychopy.constants import *  # things like STARTED, FINISHED
import random, csv
import os  # handy system and path functions
import sys # to get file system encoding

random.seed(4711) 

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'Versuch2'  # from the Builder filename that created this script
expInfo = {u'participant': u'1000'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp


# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------------------------------------------------------------------------------
# --------------- String Definitions -------------------------------------------
# ------------------------------------------------------------------------------

textdict = {'Instruktion' : u'Hallo und herzlich willkommen!\nIn diesem Experiment werden Sie gesprochene Zahlen von 1 bis 9 h\xf6ren.\nDie Zahlen werden jeweils auf einer Seite von einer Frau und auf der anderen Seite von einem Mann gesprochen. \nIhre Aufgabe ist es, entweder auf die links ODER rechts gesprochene Zahl zu achten und zu entscheiden, ob diese Zahl gr\xf6\xdfer oder kleiner als 5 ist. \n\nIst die Zahl kleiner als 5, dr\xfccken Sie bitte die linke Taste. \nIst die Zahl gr\xf6\xdfer als 5, dr\xfccken Sie bitte die rechte Taste.\n\nDamit Sie wissen, ob Sie jeweils auf die linke oder rechte Seite achten sollen, wird Ihnen am Anfang jedes Durchgangs ein Hinweisreiz pr\xe4sentiert.\n\nSehen Sie das Wort "links" oder das Symbol "\u2190",\nso achten Sie bitte auf die linke Zahl.\n\nSehen Sie das Wort "rechts" oder das Symbol "\u2192",\nso achten Sie bitte auf die rechte Zahl.\n\nFalls Sie noch Fragen haben, wenden Sie sich nun gerne an den Versuchsleiter.\nWenn es keine Fragen mehr gibt, dr\xfccken Sie bitte die Leertaste, \num mit dem \xdcbungsblock zu beginnen.\n',
            'Start' : u'Dies war der \xdcbungsblock.\nDr\xfccken Sie nun bitte die Leertaste, um mit der Bearbeitung des Experiments zu beginnen.',
            'Pause' : 'Eine kurze Pause!\nWeiter geht es mit der Leertaste.',
            'ZwInstr' : u'Nun werden Ihnen wieder zwei Zahlen via Kopfh\xf6rer pr\xe4sentiert. \nDie Zahlen werden jeweils auf einer Seite von einer Frau und auf der anderen von einem Mann gesprochen. Ihre Aufgabe ist es nun, entweder auf die Frauen- oder auf die M\xe4nnerstimme zu achten und zu entscheiden, ob die gesprochene Zahl kleiner als 5 oder gr\xf6\xdfer als 5 ist.\nDamit Sie wissen, ob Sie jeweils auf die Frauen- oder M\xe4nnerstimme achten sollen, \nwird Ihnen am Anfang jedes Durchgangs ein Hinweisreiz pr\xe4sentiert.\nSehen Sie das Wort "Frau" oder das Symbol "\u2640", \nso achten Sie bitte auf die Frauenstimme.\nSehen Sie das Wort "Mann" oder das Symbol "\u2642", \nso achten Sie bitte auf die M\xe4nnerstimme.\nWeiterhin gilt:\nIst die Zahl kleiner als 5, dr\xfccken Sie bitte die linke Taste. \nIst die gesprochene Zahl gr\xf6\xdfer als 5, dr\xfccken Sie bitte die rechte Taste.\nDr\xfccken Sie bitte die Leertaste, um mit der Bearbeitung des Blocks zu beginnen.\n',
            'Danke' : u'Das Experiment ist nun zu Ende.\nVielen Dank f\xfcr Ihre Teilnahme! '}

icondict = {'links' : u'\u2190', 'rechts': u'\u2192', 'M' : u'\u2642', 'F' : u'\u2640'}

def MakeAudioFileNames():
    audioFileNames = {}
    for gL in ['M','F']: # genderLeft
        for nL in [1,2,3,4,6,7,8,9]: # numberLeft
            for gR in ['M', 'F']:
                for nR in [1,2,3,4,6,7,8,9]:
                    if gL != gR:
                        audioFileNames[(gL, nL, gR, nR)] = "%s%d%s%d.wav" % (gL, nL, gR, nR)
    return audioFileNames

def MakeBlockLists():
    audioFileNames = MakeAudioFileNames()
    blocklistOrt = []
    t=0
    for seite in ['links', 'rechts']:
        for symbol in ['icon', 'wort']:
            for nL in [1,2,3,4,6,7,8,9]: # nL means number on left side
                for nR in [1,2,3,4,6,7,8,9]: # nR is number on right side
                    if seite == 'links':
                        if nL < 5:
                            corrResponse = 'left'
                        else:
                            corrResponse = 'right'
                    else:
                        if nR < 5:
                            corrResponse = 'left'
                        else:
                            corrResponse = 'right'
                    if random.random() < 0.5: 
                        CSI = 0.9
                        RCI = 0.2
                    else:
                        CSI = 0.1
                        RCI = 1.0
                    if random.random() < 0.5:
                        gL = 'M'
                        gR = 'F'
                    else:
                        gL = 'F'
                        gR = 'M'
                    audioFile = audioFileNames[(gL, nL, gR, nR)]
                    blocklistOrt.append((seite, symbol, nL, nR, corrResponse, audioFile, CSI, RCI))
                    t += 1
                    
    blocklistGender = []
    t=0
    for gender in ['M', 'F']:
        for symbol in ['icon', 'wort']:
            for nL in [1,2,3,4,6,7,8,9]:
                for nR in [1,2,3,4,6,7,8,9]:
                    if random.random() < 0.5:
                        gL = 'M'    # gender left side is male
                        gR = 'F'
                        if nL < 5:
                            corrResponse = 'left'
                        else:
                            corrResponse = 'right'
                    else:
                        gR = 'M'
                        gL = 'F'
                        if nR < 5:
                            corrResponse = 'left'
                        else:
                            corrResponse = 'right'
                    if gender == 'F':
                        (gL,gR) = (gR,gL)
                    if random.random() < 0.5: 
                        CSI = 0.9
                        RCI = 0.2
                    else:
                        CSI = 0.1
                        RCI = 1.0
                    audioFile = audioFileNames[(gL, nL, gR, nR)]
                    blocklistGender.append((gender, symbol, nL, nR, corrResponse, audioFile, CSI, RCI))
                    t += 1
    return blocklistOrt, blocklistGender

def ZeigeText(zeigText, waitForKey = True, waitAfter = 2.0, escapeQuits = True):
    ZT = visual.TextStim(win=win, ori=0, name=zeigText,
        text= textdict[zeigText], font='Arial',
        pos=[0, 0], height=0.055, wrapWidth=None,
        color=[-1.000,-1.000,-1.000], colorSpace='rgb', opacity=1, depth=0.0)
    ZT.draw()
    win.flip()
    if waitForKey:
        keylist = event.waitKeys(keyList=['space','escape'])
        response=keylist[0]
        if response == 'space':
            win.flip() # blank screen
        if response=='escape' and escapeQuits: # escape terminates the experiment
            core.quit()
    core.wait(waitAfter)
    
def Instruction():
    ZeigeText('Instruktion')
    
def InstructionStart():
    ZeigeText('Start')
    
def InstructionPause():
    ZeigeText('Pause')
    
def InstructionGender():
    ZeigeText('ZwInstr')

def Thanks():
    ZeigeText('Danke', waitForKey = False, waitAfter = 5.0)
    
# ------------------------------------------------------------------------------
# Start Code - component code to be run before the window creation
# -------------------------------------------------------------------------------

# Setup the Window
win = visual.Window(size=(1280, 800), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='Lenovo', color=[1.000,1.000,1.000], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "trial"
trialClock = core.Clock()
Cue1 = visual.TextStim(win=win, ori=0, name='Cue1',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.3, wrapWidth=None,
    color=[-1.000,-1.000,-1.000], colorSpace='rgb', opacity=1,
    depth=0.0)
sound_1 = sound.Sound('A', secs=-1)
sound_1.setVolume(1)

# Initialize components for Routine "Feedback"
FeedbackClock = core.Clock()
msg = " "
Feedback_Prac = visual.TextStim(win=win, ori=0, name='Feedback_Prac',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.3, wrapWidth=None,
    color=[1.000,-1.000,-1.000], colorSpace='rgb', opacity=1,
    depth=-1.0)

def ExecBlock(listBlock):
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    Block = data.TrialHandler(trialList=listBlock,nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=None,
        seed=None, name='Block')
    thisExp.addLoop(Block)  # add the loop to the experiment
    thisBlock = Block.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisBlock.rgb)
    if thisBlock != None:
        for paramName in thisBlock.keys():
            exec(paramName + '= thisBlock.' + paramName)

    for thisBlock in Block:
        currentLoop = Block
        # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
        if thisBlock != None:
            for paramName in thisBlock.keys():
                exec(paramName + '= thisBlock.' + paramName)
        
        #------Prepare to start Routine "trial"-------
        t = 0
        trialClock.reset()  # clock 
        frameN = -1
        # update component parameters for each repeat
        Cue1.setText(Cue)
        sound_1.setSound(Soundfile)
        Response = event.BuilderKeyResponse()  # create an object of type KeyResponse
        Response.status = NOT_STARTED
        # keep track of which components have finished
        trialComponents = []
        trialComponents.append(Cue1)
        trialComponents.append(sound_1)
        trialComponents.append(Response)
        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "trial"-------
        continueRoutine = True
        while continueRoutine:
            # get current time
            t = trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Cue1* updates
            if t >= 0.0 and Cue1.status == NOT_STARTED:
                # keep track of start time/frame for later
                Cue1.tStart = t  # underestimates by a little under one frame
                Cue1.frameNStart = frameN  # exact frame index
                Cue1.setAutoDraw(True)
            # start/stop sound_1
            if t >= CSI and sound_1.status == NOT_STARTED:
                # keep track of start time/frame for later
                sound_1.tStart = t  # underestimates by a little under one frame
                sound_1.frameNStart = frameN  # exact frame index
                sound_1.play()  # start the sound (it finishes automatically)
            
            # *Response* updates
            if t >= CSI and Response.status == NOT_STARTED:
                # keep track of start time/frame for later
                Response.tStart = t  # underestimates by a little under one frame
                Response.frameNStart = frameN  # exact frame index
                Response.status = STARTED
                # keyboard checking is just starting
                Response.clock.reset()  # now t=0
                event.clearEvents(eventType='keyboard')
            if Response.status == STARTED:
                theseKeys = event.getKeys(keyList=['left', 'right'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    if Response.keys == []:  # then this was the first keypress
                        Response.keys = theseKeys[0]  # just the first key pressed
                        Response.rt = Response.clock.getTime()
                        # was this 'correct'?
                        if (Response.keys == str(CorrAns)) or (Response.keys == CorrAns):
                            Response.corr = 1
                        else:
                            Response.corr = 0
                        # a response ends the routine
                        continueRoutine = False
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "trial"-------
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        sound_1.stop() #ensure sound has stopped at end of routine
        # check responses
        if Response.keys in ['', [], None]:  # No response was made
           Response.keys=None
           # was no response the correct answer?!
           if str(CorrAns).lower() == 'none': Response.corr = 1  # correct non-response
           else: Response.corr = 0  # failed to respond (incorrectly)
        # store data for Block (TrialHandler)
        Block.addData('Response.keys',Response.keys)
        Block.addData('Response.corr', Response.corr)
        if Response.keys != None:  # we had a response
            Block.addData('Response.rt', Response.rt)
        # the Routine "trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()

        #------Prepare to start Routine "Feedback"-------
        t = 0
        FeedbackClock.reset()  # clock 
        frameN = -1
        routineTimer.add(0.500000)
        # update component parameters for each repeat
        if Response.corr:#stored on last run routine
            continue
        else:
            msg="Falsch"
        Feedback_Prac.setText(msg)
        # keep track of which components have finished
        FeedbackComponents = []
        FeedbackComponents.append(Feedback_Prac)
        for thisComponent in FeedbackComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "Feedback"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = FeedbackClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # *Feedback_Prac* updates
            if t >= 0.0 and Feedback_Prac.status == NOT_STARTED:
                # keep track of start time/frame for later
                Feedback_Prac.tStart = t  # underestimates by a little under one frame
                Feedback_Prac.frameNStart = frameN  # exact frame index
                Feedback_Prac.setAutoDraw(True)
            if Feedback_Prac.status == STARTED and t >= (0.5-win.monitorFramePeriod*0.75): #most of one frame period left
                Feedback_Prac.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in FeedbackComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "Feedback"-------
        for thisComponent in FeedbackComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        thisExp.nextEntry()
        
    # completed 1 repeats of 'Block'

    # get names of stimulus parameters
    if Block.trialList in ([], [None], None):  params = []
    else:  params = Block.trialList[0].keys()
    # save data for this loop
    Block.saveAsExcel(filename + '.xlsx', sheetName='Block',
        stimOut=params,
        dataOut=['n','all_mean','all_std', 'all_raw'])



debug = True # zu Entwicklungszwecken

blocklistOrt, blocklistGender = MakeBlockLists()
random.shuffle(blocklistOrt)
random.shuffle(blocklistGender)

# make blocks by splitting blocklists

blockOrt1 = blocklistOrt[:int(len(blocklistOrt)/2)]
blockOrt2 = blocklistOrt[int(len(blocklistOrt)/2):]
blockGender1 = blocklistGender[:int(len(blocklistGender)/2)]
blockGender2 = blocklistGender[int(len(blocklistGender)/2):]

def idxCueRep(blocklist):
    t = len(blocklist)
    idx = -1 # default is no repetition
    for i in range(t-1):
        a = blocklist[i]
        b = blocklist[i+1]
        if a[0] == b[0] and a[1] == b[1]: # cue repetition
            idx = i # position of repetition
            break
    return idx
            

def CueNoRepShuffle(blocklist):
    random.shuffle(blocklist)
    newlist = []
    tt = len(blocklist)
    print tt
    iflag = True
    indx = idxCueRep(blocklist)
    count = 0
    while indx > -1:
        newlist.append(blocklist[:indx])
        blocklist = blocklist[indx:]
        random.shuffle(blocklist)
        indx = idxCueRep(blocklist)
        count += 1
        if count > 5 * tt: # give up
            count = -1
            newlist.append(blocklist)
            break
    if len(newlist) == 0:
        newlist = blocklist
    if idxCueRep(newlist) > -1:
        count = -1
    return newlist, count
    

random.shuffle(blocklistOrt)
random.shuffle(blocklistGender)

#i=-1 # -1 means cue repetition
#while i<0: # if necessary try until doomsday
#    blocklistOrt, i = CueNoRepShuffle(blocklistOrt)
#i=-1
#while i<0:
#    blocklistGender, i = CueNoRepShuffle(blocklistGender)

blockPractOrt = blocklistOrt[:16]
blockPractGender = blocklistGender[:16]

# feed TrialHandler
def FeedTrialHandlerOrt(blockOrt):
    listOrt = []
    for item in blockOrt:
        (seite, symbol, nL, nR, corrResponse, audioFile, csi, rci) = item
        if symbol == 'icon':
            cue = icondict[seite]
        else:
            cue = seite
        thisdict = {'Cue' : cue, 'Stimulus_links' : nL, 'Stimulus_rechts' : nR, 'Soundfile' : audioFile,
        'CorrAns' : corrResponse, 'Bedeutung' : seite , 'CSI' : csi, 'RCI' : rci}
        listOrt.append(thisdict)
    return listOrt

def FeedTrialHandlerGender(blockGender):
    listGender = []
    for item in blockGender:
        (gender, symbol, nL, nR, corrResponse, audioFile, csi, rci) = item
        if symbol == 'icon':
            cue = icondict[gender]
        else:
            cue = gender
        thisdict = {'Cue' : cue, 'Stimulus_links' : nL, 'Stimulus_rechts' : nR, 'Soundfile' : audioFile,
        'CorrAns' : corrResponse, 'Bedeutung' : gender , 'CSI' : csi, 'RCI' : rci}
        listGender.append(thisdict)
    return listGender
    

listPractOrt = FeedTrialHandlerOrt(blockPractOrt)
listPractGender = FeedTrialHandlerGender(blockPractGender)
listOrt1 = FeedTrialHandlerOrt(blockOrt1)
listOrt2 = FeedTrialHandlerOrt(blockOrt2)
listGender1 = FeedTrialHandlerGender(blockGender1)
listGender2 = FeedTrialHandlerGender(blockGender2)

if debug == False:
    Instruction()
    ExecBlock(listPractOrt)
    InstructionStart()
    ExecBlock(listOrt1)
    InstructionPause()
    ExecBlock(listOrt2)
    InstructionGender()
    ExecBlock(listPractGender)
    Instruction(Start)
    ExecBlock(listGender1)
    InstructionPause()
    ExecBlock(listGender2)
    Thanks()

if debug:
    print listPractOrt
    print listPractGender
    
core.quit()