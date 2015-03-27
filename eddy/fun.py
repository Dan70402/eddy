import nltk
from eddy.tagger import SequentialTagger
from eddy.tokenizer import TreebankTokenizer

invite_examples = [
#1:1 context
	"invite dan@contatta.com",# S/NP
	"Eddy invite",# NP VP
	"Eddy invite user",# NP VP
	"Eddy invite a user",# NP VP
	"Eddy invite dan@contatta.com",# NP VP 'EML'
	"Eddy invite user dan@contatta.com",# NP VP 'EML'
	"Eddy invite guest dan@contatta.com",# NP VP 'EML'
	"Eddy invite dan@contatta.com to PLACE",# NP VP 'EML' NP
	"Eddy invite dan@contatta.com to PLACE as user",# NP VP 'EML NP PP
	"Eddy invite dan@contatta.com to PLACE as guest",# NP VP 'EML NP PP
	"Eddy invite dan@contatta.com to PLACE as a user",# NP VP 'EML NP PP
	"Eddy invite dan@contatta.com to PLACE as a guest",# NP VP 'EML NP PP
	"Eddy invite dan@contatta.com as user",# NP VP 'EML' PP
	"Eddy invite dan@contatta.com as guest",# NP VP 'EML' PP
	"Eddy invite dan@contatta.com as a user",# NP VP 'EML' PP
	"Eddy invite dan@contatta.com as a guest",# NP VP 'EML' PP
	"Eddy invite dan@contatta.com as user to PLACE",# NP VP 'EML' PP NP
	"Eddy invite dan@contatta.com as guest to PLACE",# NP VP 'EML' PP NP
	"Eddy invite user dan@contatta.com to PLACE",# NP VP 'EML' NP
	"Eddy invite guest dan@contatta.com to PLACE",# NP VP 'EML' NP
]
# #room context
# 	"Eddy invite dan@contatta.com to room",# NP VP 'EML' NP
# 	"Eddy invite dan@contatta.com to the room",# NP VP 'EML' NP
# 	"Eddy invite dan@contatta.com as user",# NP VP 'EML' PP
# 	"Eddy invite dan@contatta.com as guest",# NP VP 'EML' PP
# 	"Eddy invite dan@contatta.com as a user",# NP VP 'EML' PP
# 	"Eddy invite dan@contatta.com as a guest",# NP VP 'EML' PP
# 	"Eddy invite dan@contatta.com as a user to room",
# 	"Eddy invite dan@contatta.com as a guest to room",
# 	"Eddy invite dan@contatta.com as a user to the room",
# 	"Eddy invite dan@contatta.com as a guest to the room",
# 	"Eddy invite dan@contatta.com to room as user",
# 	"Eddy invite dan@contatta.com to room as guest",
# 	"Eddy invite dan@contatta.com to the room as user",
# 	"Eddy invite dan@contatta.com to the room as guest",

#same use cases as above but invitation as noun isntead of invite verb
send_examples = [
	"Eddy send invite",
	"Eddy send invitation",
	"Eddy send user invite",
	"Eddy send user invitation",
	"Eddy send guest invite"
	"Eddy send guest invitation",
	"Eddy send invite to Dan",
	"Eddy send invitation to Dan",
	"Eddy send guest invite to dan@contatta.com",
	"Eddy send guest invitation to dan@contatta.com",
	"Eddy send user invite to dan@contatta.com",
	"Eddy send user invitation to dan@contatta.com",
]
#

tokenizer = TreebankTokenizer.TreebankTokenizer()
tagger = SequentialTagger.SequentialTagger()

# for e in examples:
# 	tokens = tokenizer.tokenize(e)
# 	print tagger.tag(tokens)

examples = invite_examples
for example in examples[:4]:
	tagged = tagger.tag(tokenizer.tokenize(example))
	print tagged
	pos_tags = [pos for (token,pos) in tagged]

	lookup_dict = {}
	for token,pos in tagged:
		if pos not in lookup_dict.keys():
			lookup_dict[pos] = []
		lookup_dict[pos].append(token)
	#print lookup_dict

	pos_vals = [token for (token,pos) in tagged]
	#pos_tags = [pos for (token,pos) in tokenizer.tokenize(examples[0])]

	invite_grammar = nltk.CFG.fromstring("""
	S -> NP VP | NP VP 'EML' | NP VP 'EML' PP | NP VP 'EML' NP | NP VP 'EML' PP | NP VP 'EML' NP PP | NP VP 'EML' PP NP
	S -> S/NP
	S/NP -> VP 'EML'
	NP -> N | Det N
	VP -> V | V NP
	PP -> P NP
	P -> 'IN'
	N -> 'NN'
	Det -> 'TO' | 'DT'
	V -> 'VB'
	""")



	ROOT = 'ROOT'
	def getNodes(parent):
		for node in parent:
			if type(node) is nltk.Tree:
				if node.label() == ROOT:
					print "======== Sentence ========="
					print "Sentence:", " ".join(node.leaves())
				else:
					print "Label:", node.label()
					print "Leaves:", node.leaves()

				getNodes(node)
			else:
				print "Word:", node

	def mapBack(leaves, lookup_dict):

		index_counter = {}
		result = {}
		for tag in lookup_dict.keys():
			index_counter[tag] = 0
			result[tag] = []

		for l in leaves:
			#print "looking up " + str(l)
			result[l].append(lookup_dict[l][index_counter[l]])
			index_counter[l] += 1

		return result

	def getLeafByTag(tree, tags):
		#Give me the V and N for VP
		result = {}
		for tag in tags:
			result[tag] = None

		def getNodes(parent, tag):
			#Only works with base
			for node in parent:
				if type(node) is nltk.Tree:
					if node.label() == ROOT:
						getNodes(node, tag)
					else:
						if node.label() == tag:
							result[tag] = node[0]
							continue
						else:
							getNodes(node, tag)
						# print "Label:", node.label()
						# print "Leaves:", node.leaves()
				else:
					print "Word:" + node

		for tag in tags:
			getNodes(tree, tag)
		return result








	sent = examples[0]
	rd_parser = nltk.RecursiveDescentParser(invite_grammar, trace=0) #trace=2

	trees = []
	for tree in rd_parser.parse(pos_tags):
		trees.append(tree)
	if not trees: print "Parse Failed"



	for tree in trees:
		print(tree)
		#print getNodes(tree)
		leaves = tree.leaves()
		tree.draw()
		print(tree[0].label())

		maps = mapBack(leaves, lookup_dict)
		if maps['VB'][0] == "invite":
			print "Found an invite"

			if maps.has_key('EML'):
				print "Found emails: " + str(maps['EML'])
			else:
				print "No email found"
				print ""

		#If the first node has label S/NP we must have hit our S/NP rule]
		print str(len(tree))
		print tree

		bot_name = None
		user = None
		verb = None
		to_email = None
		to_place = None
		as_type = None

		if len(tree) == 1:
			print "Tree length is 1"
			#S -> S/NP
			if tree[0].label() == 'S/NP':
				#S/NP can only have two leaves (VP 'EML'
				leaves = tree[0].leaves()
				print leaves
				verb = maps[leaves[0]][0]
				to_email = maps[leaves[1]][0]
		elif len(tree) == 2:
			print "Tree length is 2"
			if tree[0].label() == 'NP':
				#The first noun is either a name or 'guest'|'user'
				mapped_val = maps['NN'][0]
				if mapped_val == 'guest' or mapped_val == 'user':
					as_type = mapped_val
				else:
					bot_name = mapped_val
			if tree[1].label() == 'VP':
				#if the second tree is VP we care about the VB and the NOUN (action and type)
				result = getLeafByTag(tree[1], ['V','N'])
				print 'hi'
				#
				#
				# #S/NP can only have two leaves (VP 'EML'
				# leaves = tree[0].leaves()
				# for t in tree:
				# 	print t.leaves()
				# # verb = maps[leaves[0]][0]
				# # to_email = maps[leaves[1]][0]

		else:
			print "bad tree length"

		print ' '.join(['bot_name:'+str(bot_name), 'user:'+str(user), 'verb:'+str(verb), 'to_email:'+str(to_email), 'to_place:'+str(to_place), 'as_type:'+str(as_type)])

		#print(tree.flatten())


"""
NP we just care about the noun
S/NP (verb, noun),(email)
"""