from flask import Flask, render_template, request
from optimization import *
app = Flask(__name__)

@app.route('/')
def dropdown_diet_type():
    diets = ['Regular', 'Vegan', 'Vegetarian', 'Pescatarian']
    item_include = list(df['Main.food.description'])
    item_include.append('No Selection') 
    return render_template('diet_type.html', diet=diets, item_include = item_include)

@app.route('/diet_out', methods=['POST'])
def show_diet():
    if request.method == "POST":
        diet = request.form['diet']
        item_inc = request.form['item_include']
        string = diet_problem(diet, item_inc)
        diets = ['Regular', 'Vegan', 'Vegetarian', 'Pescatarian']
        item_include = list(df['Main.food.description'])
        item_include.append('No Selection') 
        return render_template('diet_output.html', string=string, diet=diets, item_include = item_include)


if __name__ == "__main__":
    app.run()
