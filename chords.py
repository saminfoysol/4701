import csv

class Tree(object):
    def __init__(self):
        self.left = None
        self.center = None
        self.right = None
        self.data = None

tracked_progressions = {}

def constructTones(key, type):
	
	reader = csv.reader(open('relativeminor.csv'))

	rMinors = {}
	for row in reader:
		rMinors[row[0]] = row[1]

	if (type == "minor"):
		key = rMinors[key]

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

def convertToTones(progression, key, tonal):
	roman_num_arr = []
	tones = constructTones(key, tonal)
	for x in range(0,len(tones)):
		if (tones[x] == key):
			one = x
	toneMap = {}
	for x in range(0,len(tones)):
		toneMap[tones[(one + x)%7]] = str(x + 1)
	
	for x in range(0, len(progression)):
		roman_num_arr.append(toneMap[progression[x]])


	print(toneMap)
	return roman_num_arr

datasets = {1:'2chords.csv',2:'2chords.csv',3:'3chords.csv',4:'4chords.csv'}

def treeHelper(original,root,count):
	
	p = root.data
	if (len(root.data) == count):
		#print(root.data)
		#print(original.data)
		return root
	for x in range(0,3):
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
					max_progression = row['chord_HTML'].split(',')
					max_probability = (row['probability'])
		if (x==0):
			root.left = Tree()
			root.left.data = max_progression
			root.left = treeHelper(original,root.left,count)
			#print(root.left.data)
			
		if (x == 1):
			root.center = Tree()
			root.center.data = max_progression
			root.center = treeHelper(original,root.center,count)
			#print(root.center.data)
			
		if (x == 2):
			root.right = Tree()
			root.right.data = max_progression
			root.right = treeHelper(original,root.right,count)
			#print(root.right.data)
	return root
			
def generateTree(progression, key, tonal, length):
	depth = length - len(progression)
	root = Tree()
	root.data = convertToTones(progression,key,tonal)
	return treeHelper(root,root,4)


tr = generateTree(["C","G"], "C","minor",4)

print(convertToTones(["C","Bb","F"],"F","major"))

print(tr.data)

print(tr.left.data)
print(tr.center.data)
print(tr.right.data)

print(tr.left.left.data)
print(tr.left.center.data)
print(tr.left.right.data)

print(tr.center.left.data)
print(tr.center.center.data)
print(tr.center.right.data)

print(tr.right.left.data)
print(tr.right.center.data)
print(tr.right.right.data)

