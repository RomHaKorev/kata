

def evaluate(state, neighbours):
	if state:
		nextState = (2 <= neighbours <= 3)
	else:
		nextState = neighbours == 3


	return nextState