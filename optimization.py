### importing packages needed ###
from pulp import *
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

### importing dataframe with condensed nutrition and price data###
df = pd.read_csv('summary_price_nutri_condense_nofilter_minimized.csv', error_bad_lines = False)
food = df['interaction']

### define list of code for classes of food ###
selected = LpVariable.dicts('selected', food, lowBound = 0, upBound = 1, cat = 'Binary')
meat_code = [2002,2004,2006,2008,2010,2202,2204,2206,2502,2602,2604,2606,2608]
dairy_code = [1602,1820]
fish_code = [2402]
shellfish_code = [2404]
egg_code = [2502]
oil_code = [8012]
peanut_food_code = [42110100, 42202000,42203000, 42111210]
tree_nut_food_code = [42200500,42101000,42104110,42107000,42113000,42109100,42501000]
soybean_food_code = [41420010, 41107000, 41420380, 41810400,41811400,41811600,41811800,41410010]
gluten_code = [4004, 4202] 
other_code = list(set(df['WWEIA.Category.code'])- set(meat_code+dairy_code + fish_code + egg_code + oil_code + shellfish_code ))
allergies = ['Dairy','Egg','Peanut','Shellfish','Fish','Tree nut', 'Soy', 'Gluten']

### setup basic nutrition; could allow manually designated value later ###
def nutrition_setup(prob,food_vars):
    print('setting up macro condition...')
    prob += lpSum([df['Price'][i]*food_vars[food[i]] for i in range(0,len(food))]), 'Total cost of diet'
    prob += lpSum([df['Protein'][i]* food_vars[food[i]] for i in range(0,len(food))]) >= 50, 'Min. Protein Intake'
    prob += lpSum([df['Protein'][i]* food_vars[food[i]] for i in range(0,len(food))]) <= 175, ' Max. Protein Intake'
    prob += lpSum([df['Energy'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 1800, 'Min. Calorie Intake'
    prob += lpSum([df['Energy'][i] * food_vars[food[i]] for i in range(0,len(food))]) <= 2110, 'Max. Calorie Intake'
    prob += lpSum([df['Cholesterol'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 30, 'Min. Cholesterol Intake'
    prob += lpSum([df['Cholesterol'][i] * food_vars[food[i]] for i in range(0,len(food))]) <= 240, 'Max. Cholesterol Intake'
    prob += lpSum([df['Total.Fat'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 44, 'Min. Fat Intake'
    prob += lpSum([df['Total.Fat'][i] * food_vars[food[i]] for i in range(0,len(food))]) <= 77, 'Max. Fat Intake'
    prob += lpSum([df['Carbohydrate'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 225, 'Min. Carbohydrate Intake'
    prob += lpSum([df['Carbohydrate'][i] * food_vars[food[i]] for i in range(0,len(food))]) <= 325, 'Max. Carbohydrate Intake'
    prob += lpSum([df['Fiber'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 12, 'Min. Dietary Fiber Intake'
    prob += lpSum([df['Fiber'][i] * food_vars[food[i]] for i in range(0,len(food))]) <= 40, 'Max. Dietary Fiber Intake'
    prob += lpSum([df['Sugars'][i] * food_vars[food[i]] for i in range(0,len(food))]) <= 65, 'Max. Sugar Intake'

### setup mineral requirement; could allow manually designated value later ###
def mineral_setup(prob,food_vars):
    print('setting up mineral conditions...')
    prob += lpSum([df['Iron'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 18, 'Min. Iron Intake'
    prob += lpSum([df['Calcium'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 1300, 'Min. Calcium Intake'
    prob += lpSum([df['Magnesium'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 420, 'Min. Magnesium Intake'
    prob += lpSum([df['Zinc'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 15, 'Min. Zinc Intake'
    prob += lpSum([df['Copper'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 0.9, 'Min. Copper Intake'
    prob += lpSum([df['Selenium'][i] * food_vars[food[i]]for i in range(0,len(food))]) >= 55, 'Min. Selenium Intake'
    prob += lpSum([df['Potassium'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 4700, 'Min. Potassium Intake'
    prob += lpSum([df['Sodium'][i] * food_vars[food[i]] for i in range(0,len(food))]) <= 2300, 'Max. Sodium Intake'

### setup vitamin requriement; could allow manually designated value later ###
### Vegetarian: Ignore vit. D
### Vegan: Ignore vit.D, vit.b6, vit.b12, vit.E
def vitamin_setup(prob,food_vars,diet_type):
    print('Setting up vitamin conditions...')
    prob += lpSum([df['Vitamin.C'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 90, 'Min. VitC Intake'
    prob += lpSum([df['Thiamin'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 1.2, 'Min. Thiamin Intake'
    prob += lpSum([df['Riboflavin'][i]* food_vars[food[i]] for i in range(0,len(food))]) >= 1.3, 'Min. Riboflavin Intake'
    prob += lpSum([df['Niacin'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 16, 'Min. Niacin Intake'
    prob += lpSum([df['Folate'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 400, 'Min. Folate Intake'
    prob += lpSum([df['Vitamin.K'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 120, 'Min. VitK Intake'
    prob += lpSum([df['Vitamin.A'][i]* food_vars[food[i]] for i in range(0,len(food))]) >= 900, 'Min VitA Intake'
    if(diet_type != 'Vegan'):
        prob += lpSum([df['Vitamin.E'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 15, 'Min. VitE Intake'
        prob += lpSum([df['Vitamin.B.6'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 1.7, 'Min. Vitb6 Intake'
    if(diet_type == 'Regular' or diet_type == 'Pescatarian'):
        prob += lpSum([df['Vitamin.D'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 20, 'Min. VitD Intake'
        prob += lpSum([df['Vitamin.B.12'][i] * food_vars[food[i]] for i in range(0,len(food))]) >= 2.4, 'Min. Vitb12 Intake'

### other serving size limitations
def others_setup(prob,food_vars, diet_type, idx):
    f_name = df['interaction']
    for i in range(0,len(df['WWEIA.Category.code'])):
        prob += food_vars[f_name[i]] <= 100 * selected[f_name[i]], f_name[i]+'_connect selected with food amount'
        ### if the item is specified to be included or excluded by the user,
        ### do not set it again in this function!
        if idx != None:
            if isinstance(idx, int):
                if i == idx:
                    pass
            else:
                if i in idx:
                    pass
        ### setting up meat requirement based on diet type
        elif df['WWEIA.Category.code'][i] in meat_code:
            if diet_type == 'Vegan' or diet_type == 'Vegetarian' or diet_type == 'Pescatarian':
                prob += selected[f_name[i]] == 0
            else:
                prob += food_vars[f_name[i]] == 1 * selected[f_name[i]] , f_name[i]+'Min. serving size restriction'
        ### setting up fish requirement based on diet type
        elif df['WWEIA.Category.code'][i] in fish_code:
            if diet_type == 'Vegan' or diet_type == 'Vegetarian':
                prob += selected[f_name[i]] == 0
            else:
                prob += food_vars[f_name[i]] == 1 * selected[f_name[i]] , f_name[i]+'Min. serving size restriction'
        ### setting up egg and dairy requirement based on diet type
        elif df['WWEIA.Category.code'][i] in dairy_code + egg_code:
            if diet_type == 'Vegan':
                prob += selected[f_name[i]] == 0
            else:
                if df['WWEIA.Category.code'][i] in [1820]:
                    prob += food_vars[f_name[i]] == 1 * selected[f_name[i]] , f_name[i]+'Min. serving size restriction'
                else:
                    prob += food_vars[f_name[i]] >= 0.5 * selected[f_name[i]] , f_name[i]+'Min. serving size restriction'
                    prob += food_vars[f_name[i]] <= 2 * selected[f_name[i]] , f_name[i]+'Max. serving size restriction'
        ### required some amount of oil for cooking
        elif df['WWEIA.Category.code'][i] in oil_code:
            prob += selected[f_name[i]] == 1
            prob += food_vars[f_name[i]] >= 0.0694 * selected[f_name[i]] , f_name[i]+'Min. serving size restriction'
            prob += food_vars[f_name[i]] <= 0.1389 * selected[f_name[i]] , f_name[i]+'Max. serving size restriction'
        ### currently not supporting shellfish because it's making user eats a disgusting amount of oyster
        elif df['WWEIA.Category.code'][i] in shellfish_code:
            prob += selected[f_name[i]] == 0
        else:
            ### lemon and lime serving size limitation
            if df['Food.code'][i] == 61113010 or df['Food.code'][i] == 61116010:
                prob += food_vars[f_name[i]] >= 0.1 * selected[f_name[i]] , f_name[i]+'Min. serving size restriction'
                prob += food_vars[f_name[i]] <= 0.5 * selected[f_name[i]] , f_name[i]+'Max. serving size restriction'
            ### lettuce serving size limitation
            elif df['Food.code'][i] == 75113060:
                prob += food_vars[f_name[i]] >= 0.3 * selected[f_name[i]] , f_name[i]+'Min. serving size restriction'
                prob += food_vars[f_name[i]] <= 0.7 * selected[f_name[i]] , f_name[i]+'Max. serving size restriction'
            ### carb serving size limitation
            elif df['WWEIA.Category.code'][i] in [4002, 4004, 4202, 4204,4206,4208]:
                prob += food_vars[f_name[i]] >= 0.8 * selected[f_name[i]] , f_name[i]+'Min. serving size restriction'
                prob += food_vars[f_name[i]] <= 1.2 * selected[f_name[i]] , f_name[i]+'Max. serving size restriction'
            ### vegetables serving size limitation
            elif df['WWEIA.Category.code'][i] in [6420]:
                prob += food_vars[f_name[i]] <= 1.2 * selected[f_name[i]] , f_name[i]+'Max. serving size restriction'
            ### pea limitation
            elif df['Food.code'][i] == 75120000:
                prob += food_vars[f_name[i]] == 1 * selected[f_name[i]] , f_name[i]+'Min. serving size restriction'
            else:
                prob += food_vars[f_name[i]] >= 0.5 * selected[f_name[i]] , f_name[i]+'Min. serving size restriction'
                prob += food_vars[f_name[i]] <= 1.5 * selected[f_name[i]] , f_name[i]+'Max. serving size restriction'

### setting limitation in number of servings
def serving_num_limit(prob):
    carb_idx = [i for i in range(len(df['WWEIA.Category.code'])) if df['WWEIA.Category.code'][i] in [4002, 4004, 4202, 4204,4206,4208]]
    prob += lpSum([selected[food[i]] for i in carb_idx]) >= 2
    prob += lpSum([selected[food[i]] for i in carb_idx]) <= 4
    yogurt_idx = [i for i in range(len(df['WWEIA.Category.code'])) if df['WWEIA.Category.code'][i] in [1820,2806]]
    prob += lpSum([selected[food[i]] for i in yogurt_idx]) <= 1
    bean_idx = [i for i in range(len(df['WWEIA.Category.code'])) if df['WWEIA.Category.code'][i] in [2802]]
    prob += lpSum([selected[food[i]] for i in bean_idx]) <= 2

### For printing output after optimal solution is found
def format_output(prob_var, food_des, portion_weight):
    ret_str = []
    for i in range(len(food_des)):
        if prob_var[i].varValue > 0:
            weight = round(prob_var[i].varValue * portion_weight[i])
            ret_str.append( str(food_des[i] + ": " + str(weight) + 'g'))
    return(ret_str)

### For detecting any conflicts between diet choice and item choice
def detect_conflict(diet_type, item_inc):
    has_conflict = False
    code = df['WWEIA.Category.code'][list(df['Main.food.description']).index(item_inc)]
    if diet_type == 'Pescatarian' and code in meat_code:
        has_conflict = True
    elif diet_type == 'Vegetarian' and code in meat_code + fish_code + shellfish_code:
        has_conflict = True
    elif diet_type == 'Vegan' and code in meat_code + fish_code + shellfish_code + dairy_code + egg_code:
        has_conflict = True
    return(has_conflict)

### For including or item that user selects to include
def include_or_exclude_item(prob, food_vars, idx, type_it):
    print(df['Main.food.description'][idx])
    if type_it == 'include':
        prob += selected[df['interaction'][idx]] == 1
        prob += food_vars[df['interaction'][idx]] >= 0.5 * selected[df['interaction'][idx]] , df['interaction'][idx]+'Min. serving size restriction'
    elif type_it == 'exclude':
        prob += selected[df['interaction'][idx]] == 0
###
def exclude_allergies(prob, food_vars, group):
    idx = []
    if group == 'Dairy':  
        for i in range(len(df['WWEIA.Category.code'])):
            if df['WWEIA.Category.code'][i] in dairy_code:
                idx.append(i)
                prob += selected[df['interaction'][i]] == 0
    elif group == 'Egg':
        for i in range(len(df['WWEIA.Category.code'])):
            if df['WWEIA.Category.code'][i] in egg_code:
                idx.append(i)
                prob += selected[df['interaction'][i]] == 0
    elif group == 'Peanut':
        for i in range(len(df['WWEIA.Category.code'])):
            if df['Food.code'][i] in peanut_food_code:
                idx.append(i)
                prob += selected[df['interaction'][i]] == 0
    elif group == 'Shellfish':
        for i in range(len(df['WWEIA.Category.code'])):
            if df['WWEIA.Category.code'][i] in shellfish_code:
                idx.append(i)
                prob += selected[df['interaction'][i]] == 0
    elif group == 'Fish':
        for i in range(len(df['WWEIA.Category.code'])):
            if df['WWEIA.Category.code'][i] in fish_code:
                idx.append(i)
                prob += selected[df['interaction'][i]] == 0
    elif group == 'Tree nut':
        for i in range(len(df['WWEIA.Category.code'])):
            if df['Food.code'][i] in tree_nut_food_code:
                idx.append(i)
                prob += selected[df['interaction'][i]] == 0
    elif group == 'Soy':
        for i in range(len(df['WWEIA.Category.code'])):
            if df['Food.code'][i] in soybean_food_code:
                idx.append(i)
                prob += selected[df['interaction'][i]] == 0 
    return(idx)

### Function to solve the cheap diet problem
def diet_problem(diet_type,item_inc=None, item_exc=None, allergy_group=None):
    idx = None
    if item_inc != 'No Selection':
        idx = list(df['Main.food.description']).index(item_inc)
        if(detect_conflict(diet_type, item_inc)):
            return(['There is conflict with your selections. Please try again.'])
    prob = LpProblem('Cheap Diet Problem',  LpMinimize)
    food_vars = LpVariable.dicts('food', food, lowBound = 0, upBound = 10, cat = 'Continuous')
    nutrition_setup(prob,food_vars)
    mineral_setup(prob,food_vars)
    vitamin_setup(prob,food_vars,diet_type)
    if item_inc != 'No Selection':
        include_or_exclude_item(prob, food_vars, idx, 'include')
    if item_exc != 'No Selection':
        idx2 = list(df['Main.food.description']).index(item_exc)
        include_or_exclude_item(prob, food_vars, idx2, 'exclude')
        idx = [idx, idx2]
    if allergy_group != 'No Selection':
        allergy_idx = exclude_allergies(prob, food_vars, allergy_group)
        idx = [idx, allergy_idx]
    others_setup(prob,food_vars,diet_type, idx)
    serving_num_limit(prob)
    prob.solve()
    ret_str = []
    if (LpStatus[prob.status] == 'Optimal'):
        ret_str.extend(format_output(prob.variables(),df['Main.food.description'],df['Portion.weight']))
        ret_str.append("The price for a day's diet is: $" + str(round(pulp.value(prob.objective),2)))
    else:
        ret_str = ["Diet is infeasible."]
    return(ret_str)
