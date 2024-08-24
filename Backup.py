__author__ = "<Daniel Prvanov>"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "<prvda3131@otago.ac.nz>"

import random
import numpy as np

agentName = "<my_agent>"
perceptFieldOfVision = 7   # Choose either 3,5,7 or 9
perceptFrames = 2          # Choose either 1,2,3 or 4
trainingSchedule = [("self", 400), ("random", 1)]
lower_bound = -10000
upper_bound = 10000

# This is the class for your snake/agent
class Snake:

    def __init__(self, nPercepts, actions):
        # You should initialise self.chromosome member variable here (whatever you choose it
        # to be - a list/vector/matrix of numbers - and initialise it with some random
        # values)

        self.nPercepts = nPercepts
        self.actions = actions
        self.chromosome = [0] * nPercepts * 3
        for i in range(0, len(self.chromosome)):
            self.chromosome[i] = random.randint(lower_bound,upper_bound)/1000
        for i in range(0,3):
            self.chromosome.append(random.randint(lower_bound,upper_bound)/1000)


    def AgentFunction(self, percepts):

        # You should implement a model here that translates from 'percepts' to 'actions'
        # through 'self.chromosome'.
        #
        # The 'actions' variable must be returned and it must be a 3-item list or 3-dim numpy vector

        #
        # The index of the largest numbers in the 'actions' vector/list is the action taken
        # with the following interpretation:
        # 0 - move left
        # 1 - move forward
        # 2 - move right
        #
        #
        # Different 'percepts' values should lead to different 'actions'.  This way the agent
        # reacts differently to different situations.
        #
        # Different 'self.chromosome' should lead to different 'actions'.  This way different
        # agents can exhibit different behaviour.

        # Flatten percepts into 1d array and split self.chromosomes up into sections that
        # will be multiplied by percepts.
        percepts = percepts.flatten()
        first_third_no = int(len(self.chromosome)/3 - 1)
        second_third_no = int(first_third_no * 2 + 1)
        third_third_no = int(first_third_no * 3 + 2)

        # Calculates the three sections.
        a1_nums = self.chromosome[:first_third_no]
        a2_nums = self.chromosome[first_third_no+1:second_third_no]
        a3_nums = self.chromosome[second_third_no+1:third_third_no]

        # Multiplies each section by percepts then adds one chromosome of random variance.
        a1_nums = np.multiply(a1_nums, percepts)
        a2_nums = np.multiply(a2_nums, percepts)
        a3_nums = np.multiply(a3_nums, percepts)
        a1_nums = np.append(a1_nums, self.chromosome[first_third_no])
        a2_nums = np.append(a2_nums, self.chromosome[second_third_no])
        a3_nums = np.append(a3_nums, self.chromosome[third_third_no])

        # Sums each section and returns the greatest one, this will be the action.
        a1 = np.sum(a1_nums)
        a2 = np.sum(a2_nums)
        a3 = np.sum(a3_nums)
        a = [a1, a2, a3]
        index = a.index(max(a))


        return self.actions[index]

def evalFitness(population):

    N = len(population)

    # Fitness initialiser for all agents
    fitness = np.zeros((N))

    # This loop iterates over your agents in the old population - the purpose of this boiler plate
    # code is to demonstrate how to fetch information from the old_population in order
    # to score fitness of each agent
    for n, snake in enumerate(population):
        # snake is an instance of Snake class that you implemented above, therefore you can access any attributes
        # (such as `self.chromosome').  Additionally, the object has the following attributes provided by the
        # game engine:
        #
        # snake.size - list of snake sizes over the game turns
        # .
        # .
        # .
        maxSize = np.max(snake.sizes)
        turnsAlive = np.sum(snake.sizes > 0)
        maxTurns = len(snake.sizes)

        # This fitness functions considers snake size plus the fraction of turns the snake
        # lasted for.  It should be a reasonable fitness function, though you're free
        # to augment it with information from other stats as well
        fitness[n] = maxSize + turnsAlive / maxTurns

    return fitness


def newGeneration(old_population):

    # This function should return a tuple consisting of:
    # - a list of the new_population of snakes that is of the same length as the old_population,
    # - the average fitness of the old population

    N = len(old_population)

    nPercepts = old_population[0].nPercepts
    actions = old_population[0].actions


    fitness = evalFitness(old_population)

    # At this point you should sort the old_population snakes according to fitness, setting it up for parent
    # selection.
    sorted_old_pop = [x for _, x in sorted(zip(fitness, old_population), key=lambda pair: pair[0])]
    sorted_old_pop = sorted_old_pop[::-1]

    # Create new population list...
    new_population = list()

    #for n in range(int(N)):
    #    new_snake = Snake(nPercepts, actions)
    #    mutation_rate = random.randint(5,25)/100

    #    first = sorted_old_pop[0]
    #    second = sorted_old_pop[1]
    #    third = sorted_old_pop[2]
    #    fourth = sorted_old_pop[3]
    #    elites = []
    #    elites.append(first)
    #    elites.append(second)
    #    elites.append(third)
    #    elites.append(fourth)
    #    elite_select = random.randint(0, len(elites)-1)

    #    new_chromosome = elites[elite_select].chromosome
    #    mutation_amount = int(mutation_rate * len(new_chromosome))

    #    for i in range(0, mutation_amount):
    #        x = random.randrange(0, len(new_chromosome) - 1)
    #        new_chromosome[x] = random.randint(lower_bound, upper_bound) / 1000

        #new_snake.chromosome = new_chromosome
        #new_population.append(new_snake)

    for n in range(N):

        # Create a new snake
        new_snake = Snake(nPercepts, actions)

        # Create a mutation rate between 5 and 25 percent of the chromosome
        mutation_rate = random.randint(5,25)/100

        # Here you should modify the new snakes chromosome by selecting two parents (based on their
        # fitness) and crossing their chromosome to overwrite new_snake.chromosome
        mother = sorted_old_pop[0]
        father = sorted_old_pop[1]


        mother_half = mother.chromosome[:len(mother.chromosome)//2]
        father_half = father.chromosome[len(father.chromosome)//2:]
        new_chromosome = mother_half + father_half

        #choromosome_options = []
        #choromosome_options.append(mother.chromosome)
        #choromosome_options.append(father.chromosome)
        #choromosome_options.append(child_choromosome)
        #choromosome_options.append(child_choromosome)
        #print(choromosome_options)
        #print("----")
        #new_select = random.randint(0, len(choromosome_options) - 1)
        #new_chromosome = choromosome_options[new_select]

        mutation_amount = int(mutation_rate * len(new_chromosome))
        for i in range(0, mutation_amount):
            x = random.randrange(0, len(new_chromosome) - 1)
            new_chromosome[x] = random.randint(lower_bound, upper_bound) /1000
        new_snake.chromosome = new_chromosome
        new_population.append(new_snake)

    # At the end you need to compute the average fitness and return it along with your new population
    avg_fitness = np.mean(fitness)

    return (new_population, avg_fitness)
