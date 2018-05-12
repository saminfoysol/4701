import csv
import random

#define tree with branching factor of 3
class Tree(object):
    def __init__(self):
        self.left = None
        self.center = None
        self.right = None
        self.data = None
        self.probability = 0.0

#these are the progressions in the tree already so we don't duplicate
tracked_progressions = {}

#function to construct the valid tones of a particular key
def constructTones(key, type):
	#open csv to match relative minor to appropriate accidentals
	reader = csv.reader(open('relativeminor.csv'))

	rMinors = {}
	for row in reader:
		rMinors[row[0]] = row[1]

	if (type == "minor"):
		key = rMinors[key]

	#basically construct the key signature
	tones = ["A","B","C","D","E","F","G"]
	circleOfFifths = {"Cb":7,"Gb":6,"Db":5,"Ab":4,"Eb":3,"Bb":2,"F":1,"C":0,"G":1,"D":2,"A":3,"E":4,"B":5,"F#":6,"C#":7}
	if (key == "F" or (len(key) == 2 and key[1] == 'b')):
		accidental = "b"
		pos = 1
		count = 3
	else: 
		accidental = "#"
		pos = 5
		count = 4

	for x in range(0, circleOfFifths[key]):
		tones[pos] = tones[pos] + accidental
		pos = (pos + count) % 7
	
	return tones

#takes progression and converts to appropriate roman numeral equivalent
def convertToTones(progression, key, tonal):
	roman_num_arr = []
	tones = constructTones(key, tonal)
	#find tonic to base off
	for x in range(0,len(tones)):
		if (tones[x] == key):
			one = x
	#construct tonemap to map tones with roman numerals
	toneMap = {}
	for x in range(0,len(tones)):
		#minor chords
		if (x == 1 or x == 2 or x == 5):
			toneMap[tones[(one + x)%7]+"m"] = str(x + 1)
		#major chords
		else:
			toneMap[tones[(one + x)%7]] = str(x + 1)

	
	for x in range(0, len(progression)):
		roman_num_arr.append(toneMap[progression[x]])

	return roman_num_arr

datasets = {1:'2chords.csv',2:'2chords.csv',3:'3chords.csv',4:'4chords.csv'}

def treeHelper(original,root,count):
	
	p = root.data
	#base case to stop further branching
	if (len(root.data) == count):
		return root
	for x in range(0,3):
		#open dataset and find next 3 most probable chords that come after what we have so far
		with open(datasets[len(root.data)+1]) as csvfile:
			reader = csv.DictReader(csvfile)
			max_probability = 0.0
			max_progression = []
			for row in reader:
				foundation = row['chord_HTML'].split(',')
				foundation = foundation[:-1]

				#DEBUGGING PROBLEM SOLVED: progressions that have no possibility
				if (foundation == p and ((row['probability']) > max_probability) and ((row['chord_HTML']) not in tracked_progressions)):
					tracked_progressions[(row['chord_HTML'])] = row['probability']
					potential_progression = row['chord_HTML'].split(',')
					#only for basic chords for now
					if (len(potential_progression[-1]) == 1):
						max_progression = row['chord_HTML'].split(',')
						max_probability = (row['probability'])
		if (x==0):
			root.left = Tree()
			root.left.data = max_progression
			root.left.probability = max_probability
			root.left = treeHelper(original,root.left,count)
			#print(root.left.data)
			
		if (x == 1):
			root.center = Tree()
			root.center.data = max_progression
			root.center.probability = max_probability
			root.center = treeHelper(original,root.center,count)
			#print(root.center.data)
			
		if (x == 2):
			root.right = Tree()
			root.right.data = max_progression
			root.right.probability = max_probability
			root.right = treeHelper(original,root.right,count)
			#print(root.right.data)
	return root
			
def generateTree(progression, key, tonal, length):
	tracked_progressions = {}
	depth = length - len(progression)
	root = Tree()
	root.data = convertToTones(progression,key,tonal)
	root.probability = 1.0
	return treeHelper(root,root,4)


#add up the probabilities, random number generate
def chordGenerator(root):
	if (root.left == None and root.center == None and root.right == None):
		return root.data
	total = float(root.center.probability) + float(root.left.probability) + float(root.right.probability)
	randVal = random.uniform(0.0, total)
	if (randVal < float(root.left.probability)):
		ret = chordGenerator(root.left)
	elif (randVal < float(root.left.probability) + float(root.center.probability)):
		ret = chordGenerator(root.center)
	else:
		ret = chordGenerator(root.right)
	return ret

def convertBack(progression, key, tonal):
	chosen_progression = []
	tones = constructTones(key, tonal)
	roman_map = {}
	for x in range(0, len(tones)):
		if (tones[x] == key):
			pos = x
	#we have all the tones here. start at pos, add m where appropriate
	for x in range(0, len(tones)):
		if (tones[(x + pos)%7] == 1 or tones[(x + pos)%7] == 2 or tones[(x + pos)%7] == 5):
			tones[(x + pos)%7] = tones[(x + pos)%7] + "m"
		roman_map[str(x+1)] = tones[(x + pos)%7]

	for x in range(0, len(progression)):
		chosen_progression.append(roman_map[progression[x]])
	return chosen_progression


tr = generateTree(["F#m","Em"], "D","major",4)
chosen = chordGenerator(tr)
print(chosen)
print(convertBack(chosen, "D","major"))

