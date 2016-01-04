#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
# -------------------------- * Response-effect compatibility paradigm: * --------------------------------------
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
### The subject sees a stimulus (a triangle or a square),
### Responds manually (pressing "2" or "8") and
### Receives an effect that can be either compatible or incompatible to his answer. (hears either "2" or "8")
### Then new trial starts.
### There's a short practice block without effect in the beginning, then experiment starts.
### Compatible and incompatible trials are blocked

#===================== Imports ========================
from psychopy import visual, core, event, gui, sound
import random, csv, time, numpy as np 
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
#from psychopy.constants import *  # things like STARTED, FINISHED. this is more important with vocal response
#from __future__ import print_function #why?
#from psychopy.iohub import launchHubServer

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

#================= PSTbox setup here ==================

#===================== dlg ============================
def _(string):
    return texts[string][exp_info['language']]
texts = {
    'instr':
        {'de':"Herzlich Willkommen zum Experiment",
        'en':"Welcome in experiment"}
}

exp_info = {'participant':'participant_ID',
    'language': texts.values()[0].keys()}

dlg = gui.DlgFromDict(exp_info, title= "REC_manual",
order = ['participant', 'language'],
    tip = {'participant':'Identifier of the participant.',
        'language':'Language of the instructions.',})
if dlg.OK:
    thisInfo = dlg.data
    print thisInfo
else: print 'user cancelled'

sbj_num = int(dlg.data[0]) # extract participant's number to personalize experiment (condition order)

#============= setup monitor ===========
win = visual.Window([1024,768], allowGUI=True, fullscr=False, waitBlanking=True, monitor='testMonitor', units='deg') # Create window

#============ Open log file to write ===========
file_name = exp_info['participant']+'REC_MAN-AUD.csv' 
log_file = open(file_name, 'a')
log_file.write('sbj_num, block, condition, trialnum, rt, stimulus, response, correctresponse, accuracy\n') # Heading

#========== time ============
trial_clock = core.Clock() # Clock for measuring response time
# define some intervals to use
ITI = 1.2 # inter-trial interval
REdelay = 0.2 # delay between response and effect
effecttime = 0.5 # period of effect exposure (makes sense with visual stimuli)

#======== visual stimuli ===========
triangle = visual.ShapeStim(win, lineWidth=3.5, lineColor=(1.0, 1.0, 1.0), lineColorSpace='rgb', fillColor=None, fillColorSpace='rgb', vertices=((-5, -3.5), (0, 5), (5, -3.5)), closeShape=True, pos=(0, 0), size=0.7, ori=0.0, opacity=1.0, contrast=1.0, depth=0, interpolate=True, lineRGB=None, fillRGB=None, name="triangle", autoLog=None, autoDraw=False)
square = visual.Rect(win, lineWidth=3.5, lineColor=(1.0, 1.0, 1.0), lineColorSpace='rgb', fillColor=None, fillColorSpace='rgb', vertices=((-10, -10), (-10, 10), (10, 10), (10, -10)), closeShape=True, pos=(0, 0), size=12, ori=0.0, opacity=1.0, contrast=1.0, depth=0, interpolate=True, lineRGB=None, fillRGB=None, name="triangle", autoLog=None, autoDraw=False)

#=========== auditory effect ===========
zwei = sound.Sound(value=r'/home/detlef/psychopy/noemi/wb_2.wav')
acht = sound.Sound(value=r'/home/detlef/psychopy/noemi/wb_8.wav')
effectsound = [zwei, acht]

# ------------------ dictionaries -----------------------

stim_get = {'triangle': triangle, 'square': square}
sound_get = {'zwei': zwei, 'acht': acht}

#============================================
#============= PRACTICE BLOCK ===============
#============================================
block = 0
condition = 0

# practice instruction
practice_instruction = visual.TextStim(win=win, ori=0, name='instr1',
    text="Welcome to the experiment!\n\n You are going to see a number on the screen.\n\n If you see a triangle, please press the '2' key. If you see a square, please press the '8' key.\n\n We'll start with a short practice block. Press any key whenever you're ready to proceed.\n\n(Esc will quit)\n\n",
    font='Arial', alignHoriz='center', alignVert='center',
    pos=[0, 0], height=1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)
practice_instruction.draw()
win.flip()
event.waitKeys()
core.wait(0.5)

trialnum=2 # it's got to be an even number or one of the 2 stimuli will be displayed more times

#in order to have the two types of stimuli in 50-50%
stimuli = [triangle for i in range(trialnum/2)] +  [square for i in range(trialnum/2)]

#practice block's procedure
random.shuffle(stimuli) # need to reshuffle before every condition or else stimuli exposure order will be the same in all blocks
for trial in stimuli:
    if trial == triangle:
        triangle.draw()
    else:
        square.draw()
    win.flip()
    trial_clock.reset()
    keylist = event.waitKeys() #(maxwait?)
    response=keylist[0]
    if response=='escape': core.quit()
    win.flip()
    core.wait(ITI) # blank screen, ITI
afterpracticeinstr = visual.TextStim(win=win, ori=0, name='afterpracticeinstr',
    text="Alright, now you'll start the actual experiment.\n\nYou're task is going to be the same as before:\nIf you see a triangle, please press the '2' key. If you see a square, please press the '8' key.\n\nPress any key whenever you're ready to proceed.\n\n(Esc will quit)\n\n",
    font='Arial', alignHoriz='center', alignVert='center', pos=[0, 0], height=1, wrapWidth=None, color='white', colorSpace='rgb', opacity=1, depth=0.0)
afterpracticeinstr.draw()
win.flip()
event.waitKeys()
core.wait(0.5)


#===================================================================================
#============================== EXPERIMENTAL BLOCKS ================================
#===================================================================================

trialnum = 4 # diff trial number than in practice block
stimuli = [triangle for i in range(trialnum/2)] +  [square for i in range(trialnum/2)]

def trial_handle(stimulus, eff):
    stim = stim_get[stimulus]
    effsound = sound_get[eff]
    stim.draw()
    win.flip()
    trial_clock.reset()
    keylist = event.waitKeys() #(maxWait=2)?
    response=keylist[0]
    if response=='escape': core.quit()
    else: rt=trial_clock.getTime()
    stim.draw(), win.flip(), core.wait(REdelay) # show stimulus also during response and while sbj waits for the effect to show
    #stim.draw(), effsound.play(), win.flip() # play effectsound
    effsound.play()
    return response, rt
    

# compatible condition
def anyblock(condition):
    random.shuffle(stimuli) # reshuffle
    trialnum = 1 # for the output
    stimulus = '' # for the output
    for trial in stimuli:
        if trial == triangle:
            stimulus = 'triangle'
            correctresponse = "2"
            if condition == 1: #compatible
                (response, rt) = trial_handle(stimulus, 'zwei')
            else: # incompatible
                (response, rt) = trial_handle(stimulus, 'acht')
        else:
            stimulus = 'square'
            correctresponse = "8"
            if condition == 1: #compatible
                (response, rt) = trial_handle(stimulus, 'acht')
            else: #incompatible
                (response, rt) = trial_handle(stimulus, 'zwei')
        core.wait(effecttime), win.flip() # blank screen. ITI = 1200ms
        log_file.write('%d, %d, %d, %d, %f, %s, %s, %s, %d\n' % (sbj_num, block, condition, trialnum, rt, stimulus, response, correctresponse, response == correctresponse))
        core.wait(ITI)
        trialnum += 1


def compblock():
    condition = 1 # for the output
    anyblock(condition)

#incompatible condition
def incompblock():
    condition = 2 # for the output
    anyblock(condition)

#====================================================================
#================= defining pause instruction =======================
#====================================================================

def pause_slide():
    pause_instruction = visual.TextStim(win=win, ori=0, name='instr2',
    text="Now you can take a short break!\n\nYour task is going to be the same as before:\nIf you see a triangle, please press the '2' key. If you see a square, please press the '8' key.\n\nPress any key whenever you're ready to proceed.\n\n(Esc will quit)\n\n",
    font='Arial', alignHoriz='center', alignVert='center', pos=[0, 0], height=1, wrapWidth=None, color='white', colorSpace='rgb', opacity=1, depth=0.0)
    pause_instruction.draw(), win.flip(), event.waitKeys(), core.wait(ITI)

# ========================================================
# ============== define condition orders =================
# ========================================================
# =================== EXPERIMENT =========================
# ========================================================

if sbj_num < 4:
    block += 1 # because of output: need to follow blocknumber
    compblock(), pause_slide()
    block += 1
    incompblock()
else:
    block += 1
    incompblock(), pause_slide()
    block += 1
    compblock()

# ============= Thank you, goodbye ==============
thanks = visual.TextStim(win=win, ori=0, name='afterpracticeinstr',
        text="The experiment is over!\n\nThank you very much for your participation!\n\nPress a key to quit the experiment.\n\n Goodbye!",
        font='Arial', alignHoriz='center', alignVert='center', pos=[0, 0], height=1, wrapWidth=None, color='white', colorSpace='rgb', opacity=1, depth=0.0)
thanks.draw(), win.flip(), event.waitKeys(), core.quit()

log_file.close()
