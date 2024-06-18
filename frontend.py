from flask import Flask, render_template, request, redirect, url_for
import db_manager as db

app = Flask("FoodProject")

db.tableCheck()


global globals
globals = {"currentName": None,  "destination": None}
global foodItemCount
foodItemCount = 1


@app.route("/", methods=["GET", "POST"])
def home():
    global globals
    recipeName = ""
    if request.method == "POST":
        print(request.form)
        recipeSelect = request.form.get("recipe")

        if (recipeSelect != None):
            values = recipeSelect.split("+")
            rName = values[0]
            recipe = db.getRecipesName(recipeName=rName.lower())[0]
            user = db.getuserfromrecipe(recipeID=recipe[1])
            print(recipe)

            return redirect(url_for('recipe', id=recipe[1]))

        else:
            recipeName = request.form.get("recipebox")

    count = db.getRecipesCount(recipeName=recipeName.lower())
    result = db.getRecipesName(recipeName=recipeName.lower())
    foodcounts = []
    creator = []
    print(result)
    for r in result:
        foodcounts.append(db.getfoodsinrecipeCount(recipeID=r[1]))
        creator.append(db.getuserfromrecipe(recipeID=r[1]))
    print(count)
    print(";laskdf;as;lkdfjkasdfsdakfsa;lk")
    print(result)
    print(foodcounts)
    # foodcount = db.getfoodsinrecipeCount(recipeName=recipeName)
    # foodlocations = ""

    return render_template("home.html", globals=globals, count=count, result=result, foodcounts=foodcounts, creator=creator)


@app.route("/nav", methods=["GET", "POST"])
def nav():
    global globals
    if request.method == "POST":
        print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        print(request.form)
        nav_recipe = request.form.get("nav-recipe")
        nav_create = request.form.get("nav-create")
        nav_food = request.form.get("nav-food")
        nav_addfood = request.form.get("nav-addfood")
        if (nav_recipe != None):
            globals['destination'] = 'recipe'
            return redirect(url_for('home'))
        elif (nav_create != None):
            globals['destination'] = 'create'
            print('OOOOOOOOOOOOOOOOOOOOO')
            print(globals['currentName'])
            if (globals['currentName'] == None):
                return redirect(url_for('signin'))
            return redirect(url_for('create'))
        elif (nav_food != None):
            globals['destination'] = 'food'
            return redirect(url_for('food'))
        elif (nav_addfood != None):
            globals['destination'] = 'addfood'
            if (globals['currentName'] == None):
                return redirect(url_for('signin'))
            return redirect(url_for('addfood'))

    return redirect(url_for('home'))


@app.route("/signout", methods=["GET", "POST"])
def signout():
    global globals
    if request.method == "POST":
        globals['currentName'] = None
    return redirect(url_for('home'))


@app.route("/recipe/<id>")
def recipe(id):
    global globals
    global foodItemCount
    values = db.fromRecipeIDgetEverything(id)[0]
    fList = db.getFoodList(id)
    foodList = []
    for f in fList:
        if f[1] == 0:
            foodList.append((f[0], "Amazon Fresh"))
        else:
            foodList.append((f[0], "Ralphs"))

    data = {"recipename": "",
            "instructions": "",
            "url": "",
            "foodList": [""],
            "username": ""
            }

    data["recipename"] = values[1]
    data["username"] = values[2]
    data["instructions"] = values[4]
    data["url"] = values[5]
    data["foodList"] = foodList
    print(values)

    return render_template("recipe.html", globals=globals, data=data)


@app.route("/sign-in", methods=["GET", "POST"])
def signin():
    global globals
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        button = request.form.get("sign-in")

        query = db.queryNamesCount(username)

        if (button != None):
            if (query > 0):
                print(db.queryNames(username))
                globals['currentName'] = username
                return redirect(url_for(globals["destination"]))
            else:
                return render_template("/signin.html", globals=globals, badsignin=True)
        else:
            return redirect(url_for('signup'))
    return render_template("/signin.html", globals=globals, badsignin=False)


@app.route("/signin", methods=["GET", "POST"])
def sign_in():
    global globals
    if request.method == "POST":
        globals["destination"] = 'home'

    return redirect(url_for('signin'))


@app.route("/sign-up", methods=["GET", "POST"])
def signup():
    global globals
    if request.method == "POST":
        request.form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")

        query = db.queryNamesCount(username)

        if (password != confirmpassword):
            return render_template("signup.html", globals=globals, takenusername=False, differentpasswords=True)
        elif (query == 0):
            db.insertUser(username=username, password=password)
            globals["currentName"] = username
            return redirect(url_for(globals["destination"]))
        else:
            return render_template("signup.html", globals=globals, takenusername=True, differentpasswords=False)
    return render_template("signup.html", globals=globals, takenusername=False, differentpasswords=False)


@app.route("/create", methods=["GET", "POST"])
def create():
    global globals
    global foodItemCount

    result = db.getFoods(foodName="", storeID="")
    result.sort()
    data = {"recipename": "",
            "instructions": "",
            "url": "",
            "foodList": [""]
            }
    print(result)
    if request.method == "POST":
        print("HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(request.form)
        recipename = request.form.get('recipenamebox')
        instructions = request.form.get('instructionsbox')
        url = request.form.get('urlbox')
        i = 1
        foodList = []
        while (request.form.get('fooditem'+str(i)) != None):
            if (request.form.get('fooditem'+str(i)) != ''):
                foodList.append(request.form.get('fooditem'+str(i)))
            i += 1

        data["recipename"] = recipename
        data["instructions"] = instructions
        data["url"] = url
        data["foodList"] = foodList

        print(foodList)

        if request.form.get('submitbutton') == '':

            if recipename == '' or instructions == '' or url == '':
                return render_template("create.html", globals=globals, result=result, foodItemCount=foodItemCount, data=data, badValues=True, alreadyadded=False)

            print("OOOOOOOOOOOOOOOOOOOO")
            userid = db.queryNamesID(globals["currentName"])
            print(userid)
            # db.insertRecipe()
            db.insertRecipe_Instructions(
                recipeName=recipename, userID=userid, instructionText=instructions, sourceURL=url)
            print("GOT TO HERE 0_0")
            recipeid = db.queryRecipeID(
                recipeName=recipename.lower(), userID=int(userid))
            print("ALDLKFLKSDKLFJLSLDKFJSL")
            print(recipeid)
            print("jlasd;fkaslkdfkasdklfklsdf")
            for food in foodList:
                print(food)
                flist = food.split(" - ")
                print(flist)
                foodid = ''
                if flist[1] == 'Amazon Fresh':
                    foodid = db.queryFoodID(storeID=1, foodName=flist[0])
                else:
                    foodid = db.queryFoodID(storeID=2, foodName=flist[0])

                db.insertFoodRecipe(recipeID=int(recipeid), foodID=int(foodid))
            return redirect(url_for('home'))

        foodItemCount += 1

        return render_template("create.html", globals=globals, result=result, foodItemCount=foodItemCount, data=data, badValues=False, alreadyadded=False)

    foodItemCount = 1
    return render_template("create.html", globals=globals, result=result, foodItemCount=foodItemCount, data=data, badValues=False, alreadyadded=False)


@app.route("/add-food", methods=["GET", "POST"])
def addfood():
    global globals
    if request.method == "POST":
        print("))))))))))))))))))))))))")
        print(request.form)
        foodName = request.form.get("foodname")
        storeID = request.form.get("locationbox")
        if foodName != '' and storeID != '':
            query = db.queryFoodsCount(foodName, int(storeID))
            if query == 0:
                db.insertFood(foodName=foodName, storeID=int(storeID))
                return redirect(url_for('food'))
            return render_template("addfood.html", globals=globals, empty=False, alreadyadded=True)
        return render_template("addfood.html", globals=globals, empty=True, alreadyadded=False)

    return render_template("addfood.html", globals=globals, empty=False, alreadyadded=False)


@app.route("/food", methods=["GET", "POST"])
def food():
    global globals
    foodName = ''
    storeID = ''
    if request.method == "POST":
        print(request.form)
        foodName = request.form.get("foodbox")
        storeID = request.form.get("locationbox")

    count = db.getFoodsCount(foodName=foodName.lower(), storeID=storeID)
    result = db.getFoods(foodName=foodName.lower(), storeID=storeID)
    print("WEFOIWEJFOIWEJFIWOIEFJ")
    print(count)
    print(result)

    for row in result:
        print(row[1])

    return render_template("food.html", globals=globals, count=count, result=result)


if __name__ == "__main__":
    app.run(debug=True, port=5005)
