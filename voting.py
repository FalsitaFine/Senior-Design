def Vote(text):
	VoteB,VoteD = HardClassify(text)
	VoteML = MLClassify(text)
	Advanced = 0 
	if (Advanced):
		return VoteML
	else:
		if VoteD == VoteB:
			return VoteB
		else:
			return VoteML

