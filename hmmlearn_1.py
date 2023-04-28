from collections import defaultdict
import sys, json, os
from math import log

class HMM:
	def __init__(self):
		self.ptt = defaultdict(lambda : defaultdict(int))
		self.pwt = defaultdict(lambda : defaultdict(int))
		self.pt = defaultdict(int)
		self.ends = defaultdict(int)

	def train(self, path):
		with open(path,  encoding='utf8') as f, open('hmmmodel.txt', 'w') as out:
			sents = f.read().split('\n')
			total_tags = 0
			for sent in sents:
				prev_tag = 'START_TAG'
				self.pt[prev_tag]+=1
				total_tags+=1

				for word, tag in map(lambda x: (x[:x.rfind('/')], x[x.rfind('/')+1:]), sent.rstrip().split(' ') + ['END/END']):
					self.pt[tag]+=1
					total_tags+=1
					self.ptt[prev_tag][tag]+=1
					self.pwt[word][tag]+=1
					prev_tag = tag

				self.ends[word]+=1

			for word in self.ends:
				self.ends[word]/=self.pt['START_TAG']

			for prev_tag in self.ptt:
				for curr_tag in self.ptt:
					self.ptt[prev_tag][curr_tag] = (self.ptt[prev_tag][curr_tag] + 1) / (self.pt[prev_tag] + len(self.ptt))

			for tag in self.pt:
				self.pt[tag]/=total_tags
	           
			json.dump({'PTT':self.ptt, 'PWT':self.pwt, 'PT':self.pt, 'ENDS':self.ends}, out, indent=2)

if __name__=="__main__":
	HMM().train(sys.argv[1])