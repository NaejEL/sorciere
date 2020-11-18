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
        self.rupees = 0
        self.getInventory()
        self.doables = {}

    def getAllRecipes(self):
        action_count = int(input())
        for i in range(action_count):
            action_id, action_type, delta_0, delta_1, delta_2, delta_3, price, tome_index, tax_count, castable, repeatable = input().split()
            self.recipes_dict[int(action_id)] = {"type":action_type, "needed": [abs(int(delta_0)),abs(int(delta_1)),abs(int(delta_2)),abs(int(delta_3))], "price": int(price), "tome_index": int(tome_index), "tax_count": int(tax_count), "castable": int(castable), "repeatable": int(repeatable)}

    def getInventory(self):
        for i in range(2):
            inv_0, inv_1, inv_2, inv_3, score = [int(j) for j in input().split()]
            self.inventory[i] = [int(inv_0),int(inv_1),int(inv_2),int(inv_3)]
        self.rupees = score


    def getDoableRecipes(self):
        for recipe in self.recipes_dict:
            doable = True
            i = 0
            for n_ingr in self.recipes_dict[recipe]['needed']:
                if n_ingr != 0:
                    if n_ingr <= self.inventory[0][i]:
                        pass
                    else:
                        doable = False
                i += 1
            if doable is True:
                self.doables[recipe] = self.recipes_dict[recipe]['price']
        self.doables = sorted(self.doables.items(), key=lambda x: x[1], reverse=True)

    def doMostValuable(self):
        self.getDoableRecipes()
        self.makeRecipe(self.doables[0][0])

    def makeRecipe(self, recipe:int):
        action = self.recipes_dict[recipe]['type']
        print(action + ' ' +str(recipe))


    def calcMissingIngredients(self):
        pass

# game loop
while True:
    test = Recipes()
    test.doMostValuable()
