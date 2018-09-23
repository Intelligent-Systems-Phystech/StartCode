import os
import midi 
from math import floor
from sklearn import linear_model 
import numpy
from math import sqrt
from suffix_trees import STree
from matplotlib import pylab

#simple progress bar for fun
def ProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float (total)))
    filled = int (length * iteration // total)
    bar = fill * filled + "-" * (length - filled) 
    print ("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), end = '\r')
    if iteration == total: 
        print("\n")

#suffix tree library works with strings, so this function converts midi note code to letters
#for midi note code see appendix 1.3 http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html#BM0_
def digits_to_str (array):
    string = ""
    for i in array:
        if i % 12 == 0:
            string += "C"
        if i % 12 == 1:
            string += "C#"
        if i % 12 == 2:
            string += "D"
        if i % 12 == 3:
            string += "D#"
        if i % 12 == 4:
            string += "E"
        if i % 12 == 5:
            string += "F"
        if i % 12 == 6:
            string += "F#"
        if i % 12 == 7:
            string += "G"
        if i % 12 == 8:
            string += "G#"
        if i % 12 == 9:
            string += "A"
        if i % 12 == 10:
            string += "A#"
        if i % 12 == 11:
            string += "B"
        string += str(floor (i / 12) - 1) #adding the octave number
    return string

files = [] 
for f in os.listdir(os.getcwd()): #getting a list of all midi files in a wd
    if f.endswith(".mid"):
        files.append (f)    
max_n = 30
min_n = 15
max_lin_n = 15 
min_lin_n = 2#number of notes used for linear estimation
#start_n = 0 #minimum number of notes on every track to analyse
letters = []
numbers = []
model = linear_model.LinearRegression()
success_rate = 0
tone_err_rate = 0
errors = 0
'''
success_rate = numpy.zeros (shape = (1, n))  #each model will be run with and without additional parameter (see below)
tone_err_rate = numpy.zeros (shape = (1, n))
errors = numpy.zeros (shape = (1, n))
'''
log = open ("logfile.txt", "a") #the programm runs slowly, so it's useful to save logs
log.write ("Linear model, improved version\n")
for n in range (min_n, max_n):
    for lin_n in range (min_lin_n, max_lin_n):
        print ("Extracting data for n =", n, "lin_n =", lin_n)
        x = numpy.zeros (shape = (2 * len (files), n + 1)) 
        y = numpy.zeros (shape = (2 * len (files))) #correct answers
        for j, i in enumerate(files):
            ProgressBar (j, len(files) - 1)
            pattern = midi.read_midifile (i)
            bpm = 0
            for index, track in enumerate (pattern):
                k = 0 #note counter
                first_note = 1
                for event in track:
                    if index == 0:
                        if isinstance (event, midi.SetTempoEvent):
                            bpm = event.bpm  #bpm may be useful in the future 
                    elif 0 < index < 3:
                        if isinstance (event, midi.NoteEvent) and event.tick != 0:
                            if bpm == 0:
                                print ("Error: no bpm information available")
                                quit()
                            if k < n and not first_note: 
                                x[2 * j + index - 1][k] = event.get_pitch()#get n first notes
                            if k == n:
                                y[2 * j + index - 1] = event.get_pitch () #the n + 1 note is to be trained at
                                if n > 1:
                                    #note estmation based on simple syntax analysis
                                    current_note = digits_to_str ([x[2 * j + index - 1][n - 1]])
                                    for p, q in enumerate (x[2 * j + index - 1]): #getting a list of all notes played
                                        if digits_to_str([q]) not in letters and p < n and q != 0:
                                            letters.append (digits_to_str([q]))
                                            numbers.append (q)
                                    freq = [0] * len (letters) 
                                    st = STree.STree (digits_to_str (x[2 * j + index - 1][0:n])) #building the suffix tree
                                    for q, let in enumerate (letters):
                                        tmp = st.find_all (current_note + let) #determining how frequent the current_note+other_note combination is
                                        if isinstance(tmp, list):
                                            freq[q] += len (tmp)
                                        else:
                                            freq[q] += 1
                                    x[2 * j + index - 1][n] = numbers[freq.index(max(freq))] #adding the most frequent as another feature 
                                    letters = []
                                    numbers = []
                            if not first_note:
                                k += 1
                            first_note = 0
        model.fit (x[:, n - lin_n : n + 1], y) #training
        print (model.coef_)
        test = []
        for f in os.listdir(os.getcwd() + "/test"):
            if f.endswith(".mid"):
                test.append(f)
        test_x = numpy.zeros(shape = (1, n + 1))
        test_y = 0
        success = 0
        fail = 0
        tone_error = 0
        print ("Testing model for n =", n, "lin_n =", lin_n)
        letters = []
        numbers = []
        tmp = numpy.zeros (shape = (1, n + 1 - lin_n))
        for l, unit in enumerate (test): #the same algorythm for testing
            ProgressBar (l, len (test) - 1) 
            test_pattern = midi.read_midifile (os.getcwd() + "/test/" + unit)
            for a, track in enumerate (test_pattern):
                    if a > 0:
                        k = 0
                        first_note = 1
                        for event in track:
                            if isinstance (event, midi.NoteEvent) and event.tick != 0:
                                if k < n and not first_note:
                                    test_x[0][k] = event.get_pitch()
                                if k == n:
                                    test_y = event.get_pitch()
                                    current_note = digits_to_str ([test_x[0][n - 1]])
                                    for p, q in enumerate (test_x[0]): 
                                        if digits_to_str([q]) not in letters and p < n and q != 0:
                                            letters.append (digits_to_str([q]))
                                            numbers.append (q)
                                        freq = [0] * len (letters) 
                                        st = STree.STree (digits_to_str (test_x[0][0:n])) 
                                        for q, let in enumerate (letters):
                                            tmp = st.find_all (current_note + let)
                                            if isinstance(tmp, list):
                                                freq[q] += len (tmp)
                                            else:
                                                freq[q] += 1
                                        test_x[0][n] = numbers[freq.index(max(freq))]
                                if not first_note:
                                    k += 1
                                first_note = 0
                        letters = []
                        numbers = []
                        ans = model.predict (test_x [:, n - lin_n:n + 1])
                        if round(ans[0]) == test_y:
                            success += 1
                        else: 
                            if abs (ans[0] - test_y) <= 2:
                                tone_error += 1
                            fail += 1
                            errors += (ans - test_y)**2
        errors /= (success + fail)
        errors = round (sqrt (errors), 4)
        success_rate = round (success / (success + fail), 4)
        tone_err_rate  = round (tone_error / (success + fail), 4)
        print ("n is", n, "lin_n is", lin_n, "success rate is",  success_rate, \
               "tone error rate is",  tone_err_rate, "average error is", errors, "\n")
        log.write ("%s %s %s %s %s\n" % (n, lin_n, success_rate, tone_err_rate , errors))
log.close ()
'''
pylab.rcParams['font.family'] = 'serif'
pylab.rcParams['font.serif'] = 'FreeSerif'
pylab.rcParams['lines.linewidth'] = 2
pylab.rcParams['lines.markersize'] = 12
pylab.rcParams['xtick.labelsize'] = 24
pylab.rcParams['ytick.labelsize'] = 24
pylab.rcParams['legend.fontsize'] = 24
pylab.rcParams['axes.titlesize'] = 36
pylab.rcParams['axes.labelsize'] = 24
pylab.grid ()
x = numpy.linspace (start_n, n, n - start_n)
pylab.plot (x, success_rate[0], '--ro', x, success_rate[1], '--bo', x, success_rate[2], '--go', x, success_rate[3], '--ko')
pylab.savefig("1.png")
'''
