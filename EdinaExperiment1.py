from psychopy import visual, core, event, gui, sound
import random, csv
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

def _(string):
    return texts[string][exp_info['language']]
texts = {
    'instr':
        {'de':"Herzlich Willkommen zum Experiment",
        'en':"Welcome in experiment"}
}

exp_info = {'participant':'participant_ID',
    'language': texts.values()[0].keys()}

dlg = gui.DlgFromDict(exp_info, title= "Exp 3",
order = ['participant', 'language'],
    tip = {'participant':'Identifier of the participant.',
        'language':'Language of the instructions.',})
if dlg.OK:
    thisInfo = dlg.data
    print thisInfo
else: print 'user cancelled'

win = visual.Window([1024,768], allowGUI=True, fullscr=False, waitBlanking=True, monitor='testMonitor', color='black', units='deg')

file_name = exp_info['participant']+'_Exp_3.csv'

log_file = open(file_name, 'w')
log_file.write('block, trial, rt, vis_stim, audit_stim, focus, response, correct_resp\n')

text_instruction = visual.TextStim(win, wrapWidth= 30, pos=[0,0], text=_('instr'))
text_instruction.draw()
win.flip()
event.waitKeys()
diamond = visual.ImageStim(win, image='/home/detlef/psychopy/edina/diamond.jpg', size=(1, 1), pos=(0, 0))
leftSound = sound.Sound(value= r'/home/detlef/psychopy/edina/400HzLeft.wav')
rightSound = sound.Sound(value= r'/home/detlef/psychopy/edina/400HzRight.wav')
trial_clock = core.Clock()

# -----------------------------------------------------------------------------------------
# ---------------- generate lists ---------------------------------------------------------
# -----------------------------------------------------------------------------------------

num_blocks = 2
num_trials = 4*2 # number of trials per block, must be a multiple of 2
visual_stimuli = [] # initialize as empty list
auditory_stimuli = []
focus = []

for t in range(num_trials/2):
    visual_stimuli = visual_stimuli + ['DL'] + ['DR'] # Diamond left/right
    auditory_stimuli = auditory_stimuli + ['SL'] + ['SR'] # sound left/right
    if (t % 2) == 0: # modulo
        focus = focus + ['audio'] + ['audio']
    else:
        focus = focus + ['visual'] + ['visual']

# ---------------------------------------------------------------------------------------------
# ------------------------------------- hashes ------------------------------------------------
# ---------------------------------------------------------------------------------------------

visual_positions = {'DR':10, 'DL':-10}
auditory_positions = {'SR':'rightSound', 'SL':'leftSound'}

# ---------------------------------------------------------------------------------------------
# ----------------------------- experimental loop ---------------------------------------------
# ---------------------------------------------------------------------------------------------

for block in range(num_blocks):
    random.shuffle(visual_stimuli)
    random.shuffle(auditory_stimuli)
    for trial in range(num_trials):
        diamond.setPos(newPos=(visual_positions[visual_stimuli[trial]], 0))
        diamond.draw() # in background
        side = auditory_stimuli[trial]
        if side[1] == 'L':
            leftSound.play()
        else:
            rightSound.play()
        win.flip() # screen visible
        trial_clock.reset()
        keylist = event.waitKeys()
        leftSound.stop(), rightSound.stop()
        if keylist is not None:
            response=keylist[0]
            if response=='escape':
                core.quit()
            else:
                rt=trial_clock.getTime()
                if focus[trial] == 'audio':
                    if auditory_stimuli[trial] == 'SR':
                        correct_response = 'right'
                    else:
                        correct_response = 'left'
                else: # visual focus was demanded
                    if visual_stimuli[trial] == 'DR':
                        correct_response = 'right'
                    else:
                        correct_response = 'left'
        else:
            response='none'
        win.flip() # blank screen
        log_file.write('%d, %d, %f, %s, %s, %s, %s, %s\n' % (block, trial, rt, visual_stimuli[trial], auditory_stimuli[trial], focus[trial], response, correct_response))
        core.wait(0.6) # RSI = 0.6 sec
        
    if block + 1 < num_blocks:
        text_pause = visual.TextStim(win, wrapWidth= 30, pos=[0,0], text='Pause')
        text_pause.draw()
        win.flip()
        
        pause_key = ['']
        while pause_key[0] not in ['space']:
            pause_key = event.waitKeys() # press space for next block
    else:
        text_pause = visual.TextStim(win, wrapWidth= 30, pos=[0,0], text='Vielen Dank')
        text_pause.draw()
        win.flip()
        core.wait(5)
log_file.close() 