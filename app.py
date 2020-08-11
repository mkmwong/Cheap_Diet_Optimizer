from flask import Flask, render_template, request
from optimization import *
app = Flask(__name__)

@app.route('/')
def dropdown_diet_type():
    diets = ['Regular', 'Vegan', 'Vegetarian', 'Pescatarian']
    item_include = list(df['Main.food.description'])
    item_include.append('No Selection')
    allergy =  allergies
    return render_template('diet_type.html', diet=diets, item_include = item_include, allergy = allergy)

@app.route('/diet_out', methods=['POST'])
def show_diet():
    if request.method == "POST":
        diet = request.form['diet']
        item_inc = request.form['item_include']
        item_exc = request.form['item_exclude']
        allergy_group = request.form['allergy']
        string = diet_problem(diet, item_inc, item_exc, allergy_group)
        diets = ['Regular', 'Vegan', 'Vegetarian', 'Pescatarian']
        item_include = list(df['Main.food.description'])
        item_include.append('No Selection') 
        allergy = allergies
        return render_template('diet_output.html', string=string, diet=diets, item_include = item_include, allergy = allergy)

@app.route('/data_source')
def show_data_source():
    return render_template('data_source.html')

@app.route('/limitations')
def show_limit():
    return render_template('limitation.html')

if __name__ == "__main__":
    app.run()
