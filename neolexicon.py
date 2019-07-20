import requests, argparse, markov, sys
from requests.utils import quote as qr

quote = lambda x: qr(x.encode("utf-8"),safe="")

WORDBOT = "https://api.noopschallenge.com/wordbot"

def get_words(set,count):
	r = requests.get(WORDBOT+"?set={}&count={}".format(quote(set),quote(str(count))))
	r.raise_for_status()
	r = r.json()
	return r["words"]

def get_parser():
	parser = argparse.ArgumentParser("neolexicon.py",description="New words made fresh!")
	parser.add_argument("-l","--list-sets",action="store_true",help="List the sets and exit.")
	parser.add_argument("-s","--set",default="all",help="Set of words to request.")
	parser.add_argument("seed_count",nargs="?",default=100,type=int,help="How many words to seed the lexicon. The more the better.")
	parser.add_argument("neo_count",nargs="?",default=20,type=int,help="How many new words to make.")
	return parser

def main(args=sys.argv[1:]):
	parser = get_parser()
	args = parser.parse_args(args)
	if args.list_sets:
		try:
			sets = requests.get(WORDBOT+"/sets")
			sets.raise_for_status()
			print("Sets:\n"+"\n".join(sets.json()))
		finally:
			return
	words = get_words(args.set,args.seed_count)
	model = markov.MarkovWord()
	for word in words:
		model.train(word)
	new_words = set()
	while len(new_words)<args.neo_count:
		new_words.add(model.newWord())
	for word in new_words:
		print(word)

if __name__=="__main__": main()
