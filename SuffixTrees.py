import pickle

# Load the processed dataset
with open('processed_dataset.pickle', 'rb') as handle:
    data = pickle.load(handle)


class node:
    def __init__(self):
        self.suffix_num = {} # tale_title(key), suffix_number(value)....Relevant only in leaf
        self.branches = [{}] * 256
    def set_suffix_num(self, tale_title, num):
        self.suffix_num[tale_title] = num
    def add_branch(self, sub_string, child):
        t = {}
        t[sub_string] = child
        self.branches[ord(sub_string[0])] = t
    def get_suffix_num(self):
        return self.suffix_num
    def get_all_children(self):
        return self.branches
    def is_leaf(self):
        if(self.branches == [{}] * 256):
            return True
        else:
            return False
    def all_leaves(self): # returns all the leaves of the node its called on
        if(self.is_leaf()):
            return [self]
        else:
            list_of_all_children_nodes = []
            x = self.get_all_children()
            for i in x:
                if(i):
                    list_of_all_children_nodes.append((list(i.values()))[0])
            #print(list_of_all_children_nodes)
            return [x for n in list_of_all_children_nodes for x in n.all_leaves()]

class SuffixTree:
    def __init__(self):
        self.root = node()

    def get_root(self):
        return self.root

    def build_tree(self, t, s): # t -- Title, s -- string
        title = t
        string = s + "$"
        for i in range(len(string)):
            temp = node()
            temp.set_suffix_num(tale_title = title, num = i)
            if(self.root.is_leaf()):
                self.root.add_branch(string[i:], temp)
            else:
                # Check if the prefix of that suffix is already there in some branch
                start = self.root
                j = i # for matching the suffix with branch stuff
                start_branches = start.get_all_children()
                while((start.is_leaf() == False) and (start_branches[ord(string[j])])):
                    # do some comparisons and reach to an apt start node
                    edge_string = list(start_branches[ord(string[j])].keys())[0]
                    chars_matched = self.how_many_chars_match(string[j:], edge_string)

                    if(chars_matched == len(edge_string)):
                        # move the start branch to point to the child node (an internal node)
                        start = start_branches[ord(string[j])][edge_string]
                        start_branches = start.get_all_children()

                        # Same characters are there on the edges and while comparing .... it'll lead to a leaf node
                        if(start.is_leaf()):
                            # Merge temp and start
                            start.set_suffix_num(tale_title = title, num = i)

                    else:
                        # split the current node to accomodate the new node
                        current = start_branches[ord(string[j])].popitem()
                        current_edge_string = current[0]
                        current_node = current[1]

                        internal_node = node()
                        # connect current node to internal node
                        internal_node.add_branch(current_edge_string[chars_matched:], current_node)

                        ''''
                        # connect temp to internal_node
                        internal_node.add_branch(string[chars_matched:], temp)
                        '''

                        # connect internal_node to start
                        start.add_branch(current_edge_string[0: chars_matched], internal_node)
                        start = internal_node
                        start_branches = start.get_all_children()
                    j = j + chars_matched

                # add the branch for current suffix to start
                if(start.is_leaf() == False):
                    start.add_branch(string[j:], temp)
        

    def how_many_chars_match(self, s1, s2):
        i = 0
        while((i < len(s1) and i < len(s2)) and (s1[i] == s2[i])):
            i += 1
        return i

    def return_all_matches(self, pattern):
        start = self.root
        i = 0
        mismatch_occurred = False
        while((mismatch_occurred == False) and (i < len(pattern))):
            corresponding_edge = start.get_all_children()[ord(pattern[i])]
            if(corresponding_edge):
                corresponding_edge_string = list(corresponding_edge.keys())[0]
                next_node = list(corresponding_edge.values())[0]
                x = self.how_many_chars_match(pattern[i:], corresponding_edge_string)
                if(x == len(corresponding_edge_string)):
                    i = i + x
                    start = next_node
                else:
                    i = i + x
                    if(i < len(pattern)):
                        mismatch_occurred = True
                    start = next_node
            else:
                mismatch_occurred = True

        return(start, i)

    def print_all_leaves(self, node):
        x = node.all_leaves()
        #print(len(x))
        for i in range(len(x)):
            d = x[i].get_suffix_num()
            print(d)
            for j in d:
                print("Title : \n", j)
                print("Suffix : \n", data[j][d[j]:])
                t = data[j]
                context = ""
                z = d[j]
                while((z > 0) and ((t[z] != '.') and (t[z] != '!') and (t[z] != '?'))):
                    z -= 1
                z += 1
                while((z < len(t)) and ((t[z] != '.') and (t[z] != '!') and (t[z] != '?'))):
                    context += t[z]
                    z += 1

                context += t[z]
                print("Context : \n", context)
                print()
                print()

    def print_first_result_per_tale(self, node):
        x = node.all_leaves()
        #print(len(x))
        l = {}
        for i in range(len(x)):
            d = x[i].get_suffix_num()
            for j in d:
                if(j not in l):
                    l[j] = d[j]
                else:
                    l[j] = min(l[j], d[j])


        for j in l:
            print(j, l[j])
            print("Title : \n", j)
            print("Suffix : \n", data[j][l[j]:])
            t = data[j]
            context = ""
            z = l[j]
            while((z > 0) and ((t[z] != '.') and (t[z] != '!') and (t[z] != '?'))):
                z -= 1
            if(z > 0):
                z += 1
            while((z < len(t)) and ((t[z] != '.') and (t[z] != '!') and (t[z] != '?'))):
                context += t[z]
                z += 1

            context += t[z]
            print("Context : \n", context)
            print()
            print()


    def search(self, pattern, toPrint = True):
        # If toPrint == True, it prints results, else just returns biggest match

        return_value = self.return_all_matches(pattern)
        # return value will be the node reached matching chars and no of chars matched as a tuple
        reached_node = return_value[0]
        no_of_chars_matched = return_value[1]
        # print(return_value)

        if(no_of_chars_matched >= len(pattern)):
            if(toPrint):
                print()
                print("Pattern -- " + pattern + " -- Exists")
                print()
                print("All occurrences : ")
                print()
                self.print_all_leaves(reached_node)
                print()
            return (pattern, reached_node)
        else:
            if(toPrint):
                print()
                print("Pattern -- " + pattern + " -- doesnt exist")
                print()
                print("Pattern -- " + pattern[0: no_of_chars_matched] + " -- exists instead")
            m = no_of_chars_matched
            from_where_match_max = 0
            reached_node2 = reached_node
            i = 1
            while(i < len(pattern)):
                '''
                if(toPrint):
                    print("Searching for -- " + pattern[i:])
                '''
                temp = self.return_all_matches(pattern[i:])
                new_reached_node = temp[0]
                no_of_chars_matched2 = temp[1]
                if(no_of_chars_matched2 > m):
                    m = no_of_chars_matched2
                    from_where_match_max = i
                    reached_node2 = new_reached_node
                i += 1
            if(toPrint):
                print("Longest substring of pattern that matches -- " + pattern[from_where_match_max: (from_where_match_max + m)])
                print()
                self.print_first_result_per_tale(reached_node2)
            return (pattern[from_where_match_max: (from_where_match_max + m)], reached_node2)

    def relevance1(self, query):
        # First Part
        # Relevance based on how many words matched

        words_rough = query.split(" ")
        words = []
        for i in range(len(words_rough)):
            x = words_rough[i]
            temp = ""
            for j in x:
                if(j.isalpha() or j == "'"):
                    temp += j
            if(temp):
                words.append(temp)
        words = list(set(words))
        # print(words)
        count = 0
        for i in words:
            _, n = self.return_all_matches(i)
            if(n >= len(i)):
                count += 1
        # print("No of words matched : ", count)
        return count

    def relevance2(self, query):
        # Second Part
        # Relevance based on max number of words that matched in order (even punctuations considered except for the last word)


        biggest_matched_part, node = self.search(query, toPrint = False)

        children = node.all_leaves()
        if(len(children) > 0):
            leaf = children[0]

        leaf_data = leaf.get_suffix_num()
        # print(leaf_data)

        tale = data[list(leaf_data)[0]]
        index = leaf_data[list(leaf_data)[0]]
        
        i = index

        while((i > 0) and tale[i] != " " and tale[i] != '"'):
            i -= 1

        # print(biggest_matched_part)
        # l = (len(biggest_matched_part))

        biggest_matched_part_words = biggest_matched_part.split()

        # Eliminating the quotes if a word starts or ends with quotes
        
        for j in range(len(biggest_matched_part_words)):
            if(biggest_matched_part_words[j][-1] == '"'):
                biggest_matched_part_words[j] = biggest_matched_part_words[j][0: (len(biggest_matched_part_words[j]) - 1)]
            if(biggest_matched_part_words[j][0] == '"'):
                biggest_matched_part_words[j] = biggest_matched_part_words[j][1:]
        
        # print(biggest_matched_part_words)

        proper_words = tale[i:].split()[0: len(biggest_matched_part_words)]

        # Eliminating the quotes if a word starts or ends with quotes
        
        for j in range(len(proper_words)):
            if(proper_words[j][-1] == '"'):
                proper_words[j] = proper_words[j][0: (len(proper_words[j]) - 1)]
            if(proper_words[j][0] == '"'):
                proper_words[j] = proper_words[j][1:]

        # Relaxing the punctuations constraint for last word
        
        if(not(proper_words[-1][-1].isalpha()) or not(proper_words[-1][-1].isdigit())):
            proper_words[-1] = proper_words[-1][0:(len(proper_words[-1]) - 1)]
        
        # print(proper_words)

        count = 0
        for i in biggest_matched_part_words:
            if(i in proper_words):
                count += 1
        
        # print(count)
        
        return count

    def relevance(self, query):
        group = self.relevance1(query)
        # Now we know how many words in the phrase exists in the tale (checked without considering punctuations)
        # Now lets check the order of occurrence of these words
        how_many_words_in_order = 0
        if(group > 0):
            how_many_words_in_order = self.relevance2(query)

        return (group, how_many_words_in_order)


def main():
    print("-" * 50)
    print("\nQuestion 1 : \n", "\tFor an entered pattern, it'll prints all occurrences of the pattern accross all tales if pattern matches exactly")
    print("\telse it prints all the first occurences(if more than one occurence in the same tale) of the biggest substring of the pattern matched")
    print("\nQuestion 2 : \n", "\tFor an entered pattern, it prints the first occurence of the biggest substring per tale")
    print("\tif biggest substring = pattern length then it prints all occurences of that pattern in that tale")
    print("\nQuestion 3 : \n", "\tFor an entered pattern, It'll rank the tales according to the relevance heuristic used mentioned in the report")
    print("-" * 50)
    print("\tChoose an option")
    print(" 1. Question 1 ", " 2. Question 2", " 3. Question 3", " 4. Exit", sep = "\n", end = "\n :")
    option = int(input())
    print("-" * 50)
    tree = SuffixTree()
    trees = {}
    stop = False
    while(not(stop)):
        if(option == 1):
            if(tree.get_root().is_leaf()):
                print()
                print("Building Genaralized Suffix Tree")
                for i in data:
                    tree.build_tree(i, data[i])
                print()
                print("Generalized Suffix Tree Created Successfully!!")
                print()

            toSearch = input("Enter query String : ")
            tree.search(toSearch)

        elif(option == 2):
            if(not(trees)):
                # Creating a list of trees, one for each tale
                print()
                print("Creating a list of trees, one for each tale")
                for i in data:
                    temp_tree = SuffixTree()
                    temp_tree.build_tree(i, data[i])
                    trees[i] = temp_tree
                print()
                print("List of Trees, One for each tale created Successfully!!")
                print()

            toSearch = input("Enter query String : ")
            for i in trees:
                trees[i].search(toSearch)
                # Prints all occurrences if exact match else prints first match only

        elif(option == 3):
            if(not(trees)):
                # Creating a list of trees, one for each tale
                print()
                print("Creating a list of trees, one for each tale")
                for i in data:
                    temp_tree = SuffixTree()
                    temp_tree.build_tree(i, data[i])
                    trees[i] = temp_tree
                print()
                print("List of Trees, One for each tale created Successfully!!")
                print()

            '''
            Relevance :
                Given a query string which is a phrase of words, Group the tales according to the number of words
                that matched from the query string.
                Now within each group rank them based on largest substring that matches in that tale
            '''

            string_to_check_relevance = input("Enter string based on which tales ranked : ")
            print("Relevance based on search for the String : ", string_to_check_relevance)
            print()

            relevance_list = []
            max_words = 0
            for i in trees:
                title = i
                # print("\t\t\t\t",i)
                words, order = trees[i].relevance(string_to_check_relevance)
                if(words > max_words):
                    max_words = words
                
                relevance_list.append((title, words, order))

            rank = 1
            print("Rank\t\tTale")
            print()
            for i in (range(0, (max_words + 1))[::-1]):
                print("\nNo. of words from query string that exist in these tale", i, sep = "  ----------  ")
                print()
                temp = [x for x in relevance_list if x[1] == i]
                temp.sort(reverse = True, key = lambda x: x[2])
                for j in temp:
                    print(rank, j[0], sep = "\t\t")
                    rank += 1

        elif(option == 4):
            stop = True
            # print(tree.get_root().get_all_children())

        if(option != 4):
            print("-" * 50)
            print("\nQuestion 1 : \n", "\tFor an entered pattern, it'll prints all occurrences of the pattern accross all tales if pattern matches exactly")
            print("\telse it prints all the first occurences(if more than one occurence in the same tale) of the biggest substring of the pattern matched")
            print("\nQuestion 2 : \n", "\tFor an entered pattern, it prints the first occurence of the biggest substring per tale")
            print("\tif biggest substring = pattern length then it prints all occurences of that pattern in that tale")
            print("\nQuestion 3 : \n", "\tFor an entered pattern, It'll rank the tales according to the relevance heuristic used mentioned in the report")
            print("-" * 50)
            print("\tChoose an option")
            print(" 1. Question 1 ", " 2. Question 2", " 3. Question 3", " 4. Exit", sep = "\n", end = "\n :")
            option = int(input())
            print("-" * 50)

if __name__ == '__main__':
    main()
