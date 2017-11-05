Requirements to run:
	1. pickle module for python3
	2. place the processed_dataset.pickle file in the same folder as the code SuffixTrees.py

To Run the code -- python3 SuffixTrees.py

Its menu driven:
	Select question 1, question 2 or question 3

For question 1, it builds a genaralised Suffix tree if done for the first time.
	Then search for a pattern.
	It prints the all occurrences of tale title, suffix in which the pattern occurs and the context in which the pattern occurs
	Subsequent selection of question 1 doesnt build tree, instead uses the previously built tree and just searches and prints results

For question 2, question 3, a list of trees one per tale is created
	Its created only once and same thing reused no matter question 2 or 3

For question2,
	Given a pattern, it'll match the biggest substring possible per tale.
	If full pattern matched
		Then it prints details of all occurrences in that tale
	else if a part matched(biggest substring)
		Then it prints the details of first occurrence in that tale

For question 3
	Given a query string of words, it'll return all the tales ordered rankwise based on the relevance heuristic used
