
import random

population = []
for x in range(0, 100):
    species = []
    species.append(x)
    species.append(random.random() * 1000)
    population.append(species)

print(population)

while(len(population) > 1):
    num1 = random.randint(0,len(population)-1)
    species1 = population[num1]
    del population[num1]
    num2 = random.randint(0,len(population)-1)
    species2 = population[num2]
    del population[num2]
    if(species1[1] > species2[1]):
        species1[1] = species1[1] + species2[1]
        population.append(species1)
    elif(species1[1] == species2[1]):
        population.append(species1)
        population.append(species2)
    else:
        species2[1] = species2[1] + species1[1]
        population.append(species2)

print(population)