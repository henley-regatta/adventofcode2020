#!/usr/bin/python3
#
# My answer for Day 21 part 2 - almost identical to part 1
#
# BITTEN REAL HARD BY PYTHON OBJECT MUTABILITY. Not happy at all.
#
#
# PROBLEM:
#    Given a list of foods (1 per line) listed in the form:
#       {<ingredient> <ingredient>...} (contains {<allergen>,<allergen>...})
#    And with the restriction that a given <ingredient> can have *at most*
#    one <allergen>, and that an allegen appears in one and only one ingredient
#
#    * Output a canonical list in alphabetical order *by allergen* of the
#      allergenic ingredients

import sys
import copy

datafile="../data/day21_input.txt"
#datafile="../data/day21_test1.txt"

#Input parser
dishes={}
with open(datafile,"r") as menu:
    d=0
    for l in menu:
        #Split into ingredients and allergens
        l=l.strip()
        if len(l)==0 :
            continue
        bits=l.strip().rstrip(')').split("(contains ")
        dishingredients=bits[0].split()
        dishallergens=bits[1].split(', ')
        dishes[d] = {'i' : set(dishingredients), 'a' : set(dishallergens)}
        d+=1

################################################################################
#Quick pass through the list of ingredients making a count (as the answer needs it)
#and do some book-keeping on ingredients and allergen mappings to dishes
def buildIngAllerLists(dishes) :
    ingredients={}
    allergens={}
    for d in dishes.keys() :
        for ing in dishes[d]['i'] :
            if ing not in ingredients :
                ingredients[ing]= { 'c' : 1, 'd' : [ d ] }
            else :
                ingredients[ing]['c'] +=1
                ingredients[ing]['d'].append(d)
        for a in dishes[d]['a'] :
            if a not in allergens :
                allergens[a] = { 'c' : 1, 'd' : [ d ] }
            else :
                allergens[a]['c'] +=1
                allergens[a]['d'].append(d)
    return ingredients,allergens

###############################################################################
# Solution is an iterative process:
#  a) list above contains a mapping of dish->incredients->allergens
#  b) Search that list and determine WHICH ingredient(s) appear EVERY TIME
#     that allergen is mentioned.
#  c) IF only one, it's the allergen. Remove it, remove any instances of it
#     from any other dish, and remove any dishes containing only that allergen.
#     a) Any ingredients now not appearing in any dish are "clean"
#  d) Repeat b, d until all mappings are found.
#     a) "clean list" is anything excluded by step c

#We need these for the terminal book-keeping
masterIngredients,masterAllergens = buildIngAllerLists(dishes)

#Part2 demands we later sort by allergen, so cache that as a result too
aller_ind_map={}

allergenic_ingredients=set()
all_ingredients=set()
for i in masterIngredients:
    all_ingredients.add(i)
rDishes=copy.deepcopy(dishes)
foundAllAllergens=False
while not foundAllAllergens:
    allerCands={}
    rIngredients,rAllergens = buildIngAllerLists(rDishes)
    for a in rAllergens:
        #From the first dish that appears build up a set of possible ingredients
        d = rAllergens[a]['d'][0]
        candI=set(rDishes[d]['i'])
        #Now for the rest of the dishes with that allergen, remove ingredients
        #that DO NOT Appear in that dishes ingredient list.
        for d in rAllergens[a]['d'][1:] :
            candI = candI & rDishes[d]['i']
        allerCands[a] = candI
    for a in allerCands :
        if len(allerCands[a])==1 :
            #MATCH. What's the ingredient?
            ing=allerCands[a].pop()
            aller_ind_map[a]=ing
            allergenic_ingredients.add(ing)
            #Remove this allergen from any dishes
            tDishes=copy.deepcopy(rDishes)
            for d in rDishes :
                if a in rDishes[d]['a'] :
                    if len(rDishes[d]['a'])==1 :
                        #SPECIALCASE remove the whole dish.
                        del tDishes[d]
                    else :
                        #remove the allergen from the dish
                        tDishes[d]['a'].remove(a)
            rDishes=copy.deepcopy(tDishes)
            #Remove the ingredient from all dishes
            for d in rDishes :
                if ing in rDishes[d]['i'] :
                    tDishes[d]['i'].remove(ing)
            rDishes=copy.deepcopy(tDishes)

    if len(allergenic_ingredients) == len(masterAllergens) :
        foundAllAllergens=True

print(aller_ind_map)
oList=[]
for a in sorted(aller_ind_map.keys()) :
    oList.append(aller_ind_map[a])
print("Your Part 2 Answer of Allergen-Sorted Dangerous Ingredients Is:")
print(",".join(oList))
