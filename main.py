import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


def debug(to_print: str):
    print(to_print, file=sys.stderr, flush=True)


class Recipes:
    def __init__(self):
        self.recipes_dict = {}
        self.getAllRecipes()
        self.inventory = {}
        self.inventory_slot = 0
        self.inventory_max_slot = 10
        self.rupees = 0
        self.getInventory()
        self.brewables = {}
        self.unbrewables = {}
        self.castables = {}
        self.uncastables = {}
        self.learnables = {}
        self.unlearnables = {}
        self.missing = {}
        self.lowest_dist = (0, 100)
        self.something_done = False

    def getAllRecipes(self):
        action_count = int(input())
        for i in range(action_count):
            action_id, action_type, delta_0, delta_1, delta_2, delta_3, price, tome_index, tax_count, castable, repeatable = input().split()
            self.recipes_dict[int(action_id)] = {"type": action_type, "needed": [int(delta_0), int(delta_1), int(delta_2), int(delta_3)],
                                                 "price": int(price), "tome_index": int(tome_index), "tax_count": int(tax_count),
                                                 "castable": int(castable), "repeatable": int(repeatable), "doable": False,
                                                 "missing": [0, 0, 0, 0], "distance": 0}

    def getInventory(self):
        for i in range(2):
            inv_0, inv_1, inv_2, inv_3, score = [
                int(j) for j in input().split()]
            self.inventory[i] = [int(inv_0), int(
                inv_1), int(inv_2), int(inv_3)]
        self.inventory_slot = sum(self.inventory[0])
        self.rupees = score

    def getDoables(self):
        for recipe in self.recipes_dict:
            doable = True
            i = 0
            for n_ingr in self.recipes_dict[recipe]['needed']:
                if n_ingr < 0:
                    if abs(n_ingr) <= self.inventory[0][i]:
                        pass
                    else:
                        doable = False
                        self.recipes_dict[recipe]['missing'][i] = abs(n_ingr)
                i += 1
            if doable is True:
                self.recipes_dict[recipe]['doable'] = True
                if self.recipes_dict[recipe]['type'] == 'BREW':
                    self.brewables[recipe] = self.recipes_dict[recipe]['price']
                elif self.recipes_dict[recipe]['type'] == 'CAST':
                    if self.recipes_dict[recipe]['castable'] == 1:
                        k = 0
                        for ing in self.recipes_dict[recipe]['needed']:
                            if ing > 0:
                                self.castables[recipe] = k
                            k += 1
                    else:
                        self.uncastables[recipe] = 0
                elif self.recipes_dict[recipe]['type'] == 'LEARN':
                    self.learnables[recipe] = self.recipes_dict[recipe]['price']

            else:
                if self.recipes_dict[recipe]['type'] == 'BREW':
                    self.getDistance(recipe)
                    self.unbrewables[recipe] = self.recipes_dict[recipe]['price']
                elif self.recipes_dict[recipe]['type'] == 'CAST':
                    self.uncastables[recipe] = 0
                elif self.recipes_dict[recipe]['type'] == 'LEARN':
                    self.unlearnables[recipe] = self.recipes_dict[recipe]['price']

    def win(self):
        something_done = False
        self.getDoables()
        # faire recette si possible
        if len(self.brewables) > 0:
            self.brewables = sorted(
                self.brewables.items(), key=lambda x: x[1], reverse=True)
            self.do(self.brewables[0][0])
            something_done = True
        # Tenter faire ingrédient si possible
        elif len(self.castables) > 0:
            # Choisir recette à faire
            self.getClosestRecipe()
            i = 0  # index ingr
            # Tenter faire ingrédient pour recette
            for n_ingr in self.recipes_dict[self.lowest_dist[0]]['missing']:
                if n_ingr != 0:
                    for recipe in self.castables:
                        if self.castables[recipe] == i and something_done is False:
                            if self.isNeeded(recipe, i) is False:
                                self.do(recipe)
                                something_done = True
                i += 1
            if something_done is False:
                # tenter d'apprendre un sort
                #self.learnables = sorted(self.learnables.items(), key=lambda x: x[1], reverse=True)
                # if len(self.learnables) > 0:
                #    self.do(self.learnables[0][0])
                #    something_done = True
                # Sinon faire plus gros ingrédient possible sans utiliser les ingrédients de la recette en cours
                self.castables = sorted(
                    self.castables.items(), key=lambda x: x[1], reverse=True)
                for i in range(len(self.castables)):
                    todo = True
                    j = 0
                    for ingr in self.recipes_dict[self.castables[i][0]]['needed']:
                        if ingr < 0:
                            if self.isNeeded(self.lowest_dist[0], j):
                                todo = False
                        j += 1
                    # Si place dans l'inventaire
                    if todo is True and something_done is False and self.inventory_slot < self.inventory_max_slot - 3:
                        self.do(self.castables[i][0])
                        something_done = True
                    # Si plus de place dans l'inventaire faire ingrédient le moins elevé même si besoin dans une recette
                    elif self.inventory_slot > self.inventory_max_slot - 3 and something_done is False:
                        # if len(self.castables) > 2:
                        #    self.do(self.castables[-2][0])
                        #    something_done = True
                        # else:
                        if self.castables[-1][0] != 78:
                            self.do(self.castables[-1][0])
                            something_done = True

        # Sinon REST (à ameliorer pour wait si pas possible)
        if something_done == False:
            print('REST')

    def getDistance(self, recipe: int):
        distance = 0
        for i in range(4):
            distance += self.recipes_dict[recipe]['missing'][i] * (i+1)
        self.recipes_dict[recipe]['distance'] = distance

    def getClosestRecipe(self):
        for recipe in self.unbrewables:
            dist = self.recipes_dict[recipe]['distance']
            if dist < self.lowest_dist[1]:
                self.lowest_dist = (recipe, dist)

    def isNeeded(self, recipe: int, i_ingr: int) -> bool:
        res = False
        i = 0
        for ingr in self.recipes_dict[recipe]['needed']:
            if int(ingr) < 0 and i == i_ingr:
                if self.inventory[0][i_ingr] < abs(int(ingr)):
                    res = True
            i += 1
        return res

    def do(self, recipe: int):
        print(self.recipes_dict[recipe]['type'] + ' ' + str(recipe))
        self.something_done = True


# game loop
while True:
    test = Recipes()
    test.win()
    debug(test.recipes_dict)
    debug(test.lowest_dist)
