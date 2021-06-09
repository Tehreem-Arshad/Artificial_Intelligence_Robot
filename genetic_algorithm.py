#21100250 Tehreem Arshad Genetic Algorithm Implementation
# Set up library imports.
import random
from collections import Counter
from itertools import chain
from bitstring import *

########################################################
'''
    - This module assumes you first read the Jupyter notebook. 
    - You are free to add other members functions in class GeneticAlgorithm
      as long as you do not modify the code already written. If you have justified
      reasons for making modifications in code, come talk to us. 
    - Our implementation uses recursive solutions and some flavor of 
      functional programming (maps/lambdas); You're not required to do so.
      Just Write clean code. 
'''
########################################################

class GeneticAlgorithm(object):

    def __init__(self, POPULATION_SIZE, CHROMOSOME_LENGTH, verbose):
        self.wall_bit_string_raw = "01010101011001101101010111011001100101010101100101010101"
        self.wall_bit_string = ConstBitStream(bin = self.wall_bit_string_raw)
        self.population_size = POPULATION_SIZE
        self.chromosome_length = CHROMOSOME_LENGTH # this is the length of self.wall_bit_string
        self.terminate = False
        self.verbose = verbose # In verbose mode, fitness of each individual is shown. 

    def run_genetic_alg(self):
        '''  
        The pseudo you saw in slides of Genetic Algorithm is implemented here. 
        Here, You'll get a flavor of functional 
        programming in Python- Those who attempted ungraded optional tasks in tutorial
        have seen something similar there as well. 
        Those with experience in functional programming (Haskell etc)
        should have no trouble understanding the code below. Otherwise, take our word that
        this is more or less similar to the generic pseudocode in Jupyter Notebook.

        '''
        "You may not make any changes to this function."

        # Creation of Population
        solutions = self.generate_candidate_sols(self.population_size) # arg passed for recursive implementation.

        # Evaluation of individuals
        parents = self.evaluate_candidates(solutions)

        while(not self.terminate):
            # Make pairs
            pairs_of_parents = self.select_parents(parents)

            # Recombination of pairs.
            recombinded_parents = list(chain(*map(lambda pair: \
                self.recombine_pairs_of_parents(pair[0], pair[1]), \
                    pairs_of_parents))) 

            # Mutation of each individual
            mutated_offspring = list(map(lambda offspring: \
                self.mutate_offspring(offspring), recombinded_parents))

            # Evaluation of individuals
            parents = self.evaluate_candidates(mutated_offspring) # new parents (offspring)
            if self.verbose and not self.terminate:
                self.print_fitness_of_each_indiviudal(parents)

######################################################################
###### These two functions print fitness of each individual ##########

# *** "Warning" ***: In this function, if an individual with 100% fitness is discovered, algorithm stops. 
# You should implement a stopping condition elsewhere. This codition, for example,
# won't stop your algorithm if mode is not verbose.
    def print_fitness_of_one_individual(self, _candidate_sol):
        _WallBitString = self.wall_bit_string
        _WallBitString.pos = 0
        _candidate_sol.pos = 0
        
        matching_bit_pairs = 0
        try:
            if not self.terminate:
                while (_WallBitString.read(2).bin == _candidate_sol.read(2).bin):
                    matching_bit_pairs = matching_bit_pairs + 1
                print('Individual Fitness: ', round((matching_bit_pairs)/28*100, 2), '%')
        except: # When all bits matched. 
            pass
            return

    def print_fitness_of_each_indiviudal(self, parents):
        if parents:
            for _parent in parents:
                self.print_fitness_of_one_individual(_parent)

###### These two functions print fitness of each individual ##########
######################################################################

    def select_parents(self, parents):
        '''
        args: parents (list) => list of bitstrings (ConstbitStream)
        returns: pairs of parents (tuple) => consecutive pairs.
        '''

        # **** Start of Your Code **** #
        mylist = []
        for x in range(0,len(parents),2):
            p = (parents[x],parents[x+1])
            mylist.append(p)
        return mylist
        pass
        # **** End of Your Code **** #


    # A helper function that you may find useful for `generate_candidate_sols()`
    def random_num(self):
        random.seed()
        return random.randrange(2**14) ## for fitting in 14 bits.

    def generate_candidate_sols(self, n): 
        '''
        args: n (int) => Number of cadidates solutions to generate. 
        retruns: (list of n random 56 bit ConstBitStreams) 
                 In other words, a list of individuals: Population.

        Each cadidates solution is a 56 bit string (ConstBitStreams object). 

        One clean way is to first get four 14 bit random strings then concatenate
        them to get the desired 56 bit candidate. Repeat this for n candidates.
        '''

        # **** Start of Your Code **** #
        mylist = []
        for x in range(0,n):
            random1 = format(random.getrandbits(14), 'b').zfill(14)
            random2 = format(random.getrandbits(14), 'b').zfill(14)
            random3 = format(random.getrandbits(14), 'b').zfill(14)
            random4 = format(random.getrandbits(14), 'b').zfill(14)
            bit_56 = random1+ random2+ random3+ random4
            mylist.append(bit_56)
        return mylist
        pass
        # **** End of Your Code **** # 

    def recombine_pairs_of_parents(self, p1, p2):
        """
        args: p1, and p2  (ConstBitStream)
        returns: p1, and p2 (ConstBitStream)

        split at .6-.9 of 56 bits (CHROMOSOME_LENGTH). i.e. between 31-50 bits
        """

        # **** Start of Your Code **** #
        cut_here = random.randrange(int(0.6*self.chromosome_length), int(0.9*self.chromosome_length))
        state_1.state = 0
        s1 = state_1.read(len(p1)).bin
        state_2.state = 0
        s2 = state_2.read(len(p2)).bin
        len1 = s1[:cut_here]
        len2 = s2[:cut_here]
        len3 = s1[cut_here:]
        len4 = s2[cut_here:]
        rejoin1 = len1 + len4
        rejoin2 = len2 + len3
        rejoin1 = ConstBitStream(bin = recomb1)
        rejoin2 = ConstBitStream(bin = recomb2)
        return rejoin1, rejoin2

        pass
        # **** End of Your Code **** #

    def mutate_offspring(self, p):
        ''' 
            args: individual (ConstBitStream)
            returns: individual (ConstBitStream)
        '''

        # **** Start of Your Code **** #
        for x in range(0, 56):
            if p[x] == 1:
                p[x] = random.choice([0 , 1], p=[((1/self.population_size)*(1/self.chromosome_length)) , 1 -((1/self.population_size)*(1/self.chromosome_length)) ])
            elif p[x] == 0:
                p[x] = random.choice([1 , 0], p=[((1/self.population_size)*(1/self.chromosome_length)) , 1 -((1/self.population_size)*(1/self.chromosome_length)) ])
        pass
        # **** End of Your Code **** #

    def evaluate_candidates(self, candidates): 
        '''
        args: candidate solutions (list) => each element is a bitstring (ConstBitStream)
        
        returns: parents (list of ConstBitStream) => each element is a bitstring (ConstBitStream) 
                    but elements are not unique. Fittest candidates will have multiple copies.
                    Size of 'parents' must be equal to population size.  
        '''

        # **** Start of Your Code **** #
        Mylist = []
        matching_bit_pairs = 0
        parents = []
        temp_wall = self.wall_bit_string
        temp_wall.pos = 0
        for x in range(0, len(candidates)):
            candidates[x].pos = 0
            try:
                while(temp_wall.read(2).bin == candidates[x].read(2).bin):
                    matching_bit_pairs = matching_bit_pairs + 1
                Mylist.append(matching_bit_pairs/28)
            except:
                continue

        total_possible = 28
        total_matching = sum(Mylist)
        Res = (total_matching / total_possible) / self.population_size
        if(Res == 0):
            return candidates
        while True:
            for x in range(0, len(candidates)):
                for y in range(0, int(fitness_list[x]/Res) + 1):
                    parents.append(candidates[x])
                    if(len(parents) == self.population_size):
                        return parents
        pass
        # **** End of Your Code **** # 



