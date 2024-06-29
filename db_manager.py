import mysql.connector
import create_table as ct
import requests
from mysql.connector import Error

mydb = mysql.connector.connect(
  host="localhost",
  user="food",
  password="P@ssw0rd",
  database="foodprojectdb",
  auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor(buffered=True)


def createTables():
    '''Creates the tables in MySQL.
    No return value
    '''
    mycursor.execute(ct.user_table)
    mycursor.execute(ct.recipe_table)
    mycursor.execute(ct.food_table)
    mycursor.execute(ct.food_in_recipe_table)
    mycursor.execute(ct.instruction_table)
    mycursor.execute(ct.store_table)
    createNutritionTables()

def createNutritionTables():
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS nutrition_facts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            food_id INT,
            measurement_unit VARCHAR(10) DEFAULT '100g',
            water DECIMAL(5,2),
            energy_general DECIMAL(5,2),
            energy_specific DECIMAL(5,2),
            nitrogen DECIMAL(5,2),
            protein DECIMAL(5,2),
            total_lipid DECIMAL(5,2),
            ash DECIMAL(5,2),
            carbohydrate_by_difference DECIMAL(5,2),
            carbohydrate_by_summation DECIMAL(5,2),
            fiber_total_dietary DECIMAL(5,2),
            sugars_total DECIMAL(5,2),
            sucrose DECIMAL(5,2),
            glucose DECIMAL(5,2),
            fructose DECIMAL(5,2),
            lactose DECIMAL(5,2),
            maltose DECIMAL(5,2),
            galactose DECIMAL(5,2),
            starch DECIMAL(5,2),
            citric_acid DECIMAL(5,2),
            malic_acid DECIMAL(5,2),
            vitamin_c DECIMAL(5,2),
            thiamin DECIMAL(5,2),
            riboflavin DECIMAL(5,2),
            niacin DECIMAL(5,2),
            vitamin_b6 DECIMAL(5,2),
            biotin DECIMAL(5,2),
            folate_total DECIMAL(5,2),
            vitamin_a_rae DECIMAL(5,2),
            carotene_beta DECIMAL(5,2),
            cis_beta_carotene DECIMAL(5,2),
            trans_beta_carotene DECIMAL(5,2),
            carotene_alpha DECIMAL(5,2),
            cryptoxanthin_beta DECIMAL(5,2),
            cryptoxanthin_alpha DECIMAL(5,2),
            cis_lycopene DECIMAL(5,2),
            trans_lycopene DECIMAL(5,2),
            cis_lutein_zeaxanthin DECIMAL(5,2),
            trans_lutein_zeaxanthin DECIMAL(5,2),
            vitamin_k_phylloquinone DECIMAL(5,2),
            vitamin_k_dihydrophylloquinone DECIMAL(5,2),
            vitamin_k_menaquinone DECIMAL(5,2),
            FOREIGN KEY (food_id) REFERENCES foods(id)
        );
    """)

def insertNutritionData(food_id, nutrition_data):
    placeholders = ', '.join(['%s'] * len(nutrition_data))
    columns = ', '.join(nutrition_data.keys())
    sql = "INSERT INTO nutrition_facts (food_id, {}) VALUES (%s, {})".format(columns, placeholders)
    mycursor.execute(sql, [food_id] + list(nutrition_data.values()))
    mydb.commit()

def tableCheck():
    tablesExist = False
    mycursor.execute("SHOW TABLES")
    print("here1")
    for x in mycursor:
        tablesExist = True
        print("Tables Already Exist")
        break
    if not tablesExist:
        print("here2")
        createTables()
        insertStores()
    print("Tables Created")

def queryNamesCount(name):
    query = """SELECT count(*)
    FROM users
    WHERE LOWER(username) = LOWER('{}');
    """.format(name)
    mycursor.execute(query)
    count = mycursor.fetchone()[0]
    return count

def queryNames(name):
    query = """SELECT username, password
    FROM users
    WHERE LOWER(username) = LOWER('{}');
    """.format(name)
    
    mycursor.execute(query)
    results = mycursor.fetchall()
    print(results)
    result = [row for row in results][0][0]
    print(result)
    return result

def queryNamesID(name):
    query = """SELECT userID
    FROM users
    WHERE LOWER(username) = LOWER('{}');
    """.format(name)
    
    mycursor.execute(query)
    results = mycursor.fetchall()
    result = [row for row in results][0][0]
    return result

def insertUser(username, password):
    insert = '''INSERT INTO users (username, password) 
    VALUES ('{}', '{}')'''.format(username, password)
    mycursor.execute(insert)
    mydb.commit()
    return

def insertRecipe_Instructions(recipeName, userID, instructionText, sourceURL):
    mycursor.execute('''START TRANSACTION;''')
    mycursor.execute('''SELECT @recipeID:= COUNT(*)+1 FROM recipes;''')
    mycursor.execute('''INSERT INTO recipes (recipeName, userID) VALUES ('{}', {});'''.format(recipeName, userID))
    mycursor.execute('''INSERT INTO instructions (instructionText, sourceURL, recipeID) 
    VALUES ('{}', '{}', @recipeID);
    '''.format(instructionText, sourceURL))
    mycursor.execute('''COMMIT;''')
    
    
    
    
    #print(transaction)
    #mycursor.execute(transaction, multi=True)
    mydb.commit()
    return

def queryRecipeID(recipeName, userID):
    query = """SELECT recipeID
    FROM recipes
    WHERE LOWER(recipeName) = '{}' AND userID = {};
    """.format(recipeName, userID)
    
    mycursor.execute(query)
    results = mycursor.fetchall()
    result = [row for row in results][0][0]
    return result

def queryFoodID(storeID, foodName):
    query = """SELECT foodID
    FROM foods
    WHERE storeID = {} AND LOWER(foodName) = LOWER('{}');
    """.format(storeID, foodName)
    
    mycursor.execute(query)
    results = mycursor.fetchall()
    result = [row for row in results][0][0]
    return result

def insertFoodRecipe(recipeID, foodID):
    insert = '''INSERT INTO foodrecipe (recipeID, foodID) 
    VALUES ({}, {})'''.format(recipeID, foodID)
    mycursor.execute(insert)
    mydb.commit()
    return

    

def queryinstructionsURLcount(URL):
    query = """SELECT count(*)
    FROM instructions
    WHERE LOWER(sourceURL) = LOWER('{}');
    """.format(URL)
    mycursor.execute(query)
    count = mycursor.fetchone()[0]
    return count


def insertFood(foodName, storeID):
    insert = '''INSERT INTO foods (storeID, foodName) 
    VALUES ('{}', '{}')'''.format(storeID, foodName)
    mycursor.execute(insert)
    mydb.commit()
    return

def insertStores():
    insert = '''INSERT INTO stores (storeName) 
    VALUES ('{}')'''.format("Amazon Fresh")
    mycursor.execute(insert)
    mydb.commit()
    
    insert = '''INSERT INTO stores (storeName) 
    VALUES ('{}')'''.format("Ralphs")
    mycursor.execute(insert)
    mydb.commit()
    return

def foodrecipefix():
    insert = '''INSERT INTO foodrecipe (recipeID, foodID) 
    VALUES ('{}', '{}')'''.format(1, 3)
    mycursor.execute(insert)
    mydb.commit()
    
    insert = '''INSERT INTO foodrecipe (recipeID, foodID) 
    VALUES ('{}', '{}')'''.format(1, 2)
    mycursor.execute(insert)
    mydb.commit()
    return

    

def queryFoodsCount(foodName, storeID):
    query = """SELECT count(*)
    FROM foods
    WHERE LOWER(foodName) = LOWER('{}') AND storeID = '{}';
    """.format(foodName, storeID)
    mycursor.execute(query)
    count = mycursor.fetchone()[0]
    return count
    

def getFoods(foodName, storeID):
    query = ""
    if foodName != "" and storeID != "":
        query = """SELECT foodName, storeID
        FROM foods
        WHERE LOWER(foodName) LIKE '%{}%' AND storeID = '{}';
        """.format(foodName, storeID)
    elif foodName == "" and storeID != "":
        query = """SELECT foodName, storeID
        FROM foods
        WHERE storeID = '{}';
        """.format(storeID)
    elif foodName != "" and storeID == "":
        query = """SELECT foodName, storeID
        FROM foods
        WHERE LOWER(foodName) LIKE '%{}%';
        """.format(foodName)
    else:
        query = """SELECT foodName, storeID
        FROM foods;
        """.format(storeID)
    mycursor.execute(query)
    results = mycursor.fetchall()
    print(results)
    return results


def getFoodsCount(foodName, storeID):
    query = ""
    if foodName != "" and storeID != "":
        query = """SELECT count(*)
        FROM foods
        WHERE LOWER(foodName) LIKE '%{}%' AND storeID = '{}';
        """.format(foodName, storeID)
    elif foodName == "" and storeID != "":
        query = """SELECT count(*)
        FROM foods
        WHERE storeID = '{}';
        """.format(storeID)
    elif foodName != "" and storeID == "":
        query = """SELECT count(*)
        FROM foods
        WHERE LOWER(foodName) LIKE '%{}%';
        """.format(foodName)
    else:
        query = """SELECT count(*)
        FROM foods;
        """.format(storeID)
    mycursor.execute(query)
    count = mycursor.fetchone()[0]
    return count

def getRecipesName(recipeName):
    query = ""
    if recipeName == "":
        query ="""SELECT recipeName, recipeID
        FROM recipes;
        """
    else:
        query ="""SELECT recipeName, recipeID
        FROM recipes
        WHERE LOWER(recipeName) LIKE '%{}%';
        """.format(recipeName)
    mycursor.execute(query)
    results = mycursor.fetchall()
    return results

def getuserfromrecipe(recipeID):
    query ="""SELECT username
        FROM (SELECT recipes.recipeID, users.username 
            FROM recipes, users 
            WHERE recipes.userID = users.userID) AS T
        WHERE recipeID = {};
        """.format(recipeID)
        
    mycursor.execute(query)
    results = mycursor.fetchall()
    return results

def getRecipesCount(recipeName):
    query = """SELECT count(*)
        FROM recipes
        WHERE LOWER(recipeName) LIKE '%{}%';
        """.format(recipeName)
    
    mycursor.execute(query)
    count = mycursor.fetchone()[0]
    return count

def getfoodsinrecipeCount(recipeID):
    query = """SELECT count(*) 
    FROM (SELECT users.userID, foodrecipe.foodID, recipes.recipeID 
        FROM recipes, users, foodrecipe 
        WHERE recipes.userID = users.userID 
            AND recipes.recipeID = foodrecipe.recipeID) AS t
    WHERE recipeID={}
    GROUP BY recipeID;
        """.format(recipeID)
    
    mycursor.execute(query)
    count = mycursor.fetchone()[0]
    return count


    

def fromRecipeIDgetEverything(recipeID):
    print(recipeID)
    print("LKWEKLKWLEKLKEWKL")
    view = """SELECT R.recipeID, R.recipeName, U.username, U.userID, I.instructionText, I.sourceURL
    FROM recipes R
    JOIN users U on (R.userID = U.userID)
    JOIN instructions I on (R.recipeID = I.recipeID)
    """
    
    items = """SELECT *
    FROM ({}) AS B
    WHERE recipeID = {};
    """.format(view, recipeID)
    mycursor.execute(items)
    items = mycursor.fetchall()
    print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    print(items)
    return items
#foodName, storeID, recipes.recipeID
def getFoodList(recipeID):
    query = """SELECT F.foodName, F.storeID
    FROM recipes R
    JOIN foodrecipe FR on (R.recipeID = FR.recipeID)
    JOIN foods F on (FR.foodID = F.foodID)
    WHERE FR.recipeID = {};
    """.format(recipeID)
    
    mycursor.execute(query)
    result = mycursor.fetchall()
    print()
    print(result)
    print()
    return result

def fetch_usda_food_data(api_key, query):
    """Fetch food data from USDA FoodData Central API."""
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def add_usda_food_to_database(food_data):
    """Process and add fetched USDA food data to the database."""
    for item in food_data['foods']:
        food_name = item['description']
        nutrients = {nutrient['nutrientName']: nutrient['value'] for nutrient in item['foodNutrients']}
        
        # Example nutrient mapping (adjust according to your database schema)
        nutrient_mapping = {
            'Protein': nutrients.get('Protein', 0),
            'Total lipid (fat)': nutrients.get('Total lipid (fat)', 0),
            'Carbohydrate, by difference': nutrients.get('Carbohydrate, by difference', 0),
            'Energy': nutrients.get('Energy', 0),
            'Sugars, total including NLEA': nutrients.get('Sugars, total including NLEA', 0),
            'Fiber, total dietary': nutrients.get('Fiber, total dietary', 0),
            'Calcium, Ca': nutrients.get('Calcium, Ca', 0),
            'Iron, Fe': nutrients.get('Iron, Fe', 0),
            'Sodium, Na': nutrients.get('Sodium, Na', 0),
            'Vitamin C, total ascorbic acid': nutrients.get('Vitamin C, total ascorbic acid', 0),
            'Vitamin A, IU': nutrients.get('Vitamin A, IU', 0)
        }
        
        try:
            # Assuming you have a function to insert foods, which you might need to modify or create
            insertFood(food_name, nutrient_mapping)  # You'll need to adapt this part to match your database schema
        except Error as e:
            print(f"Database error: {e}")
            continue

# Example usage
api_key = 'YOUR_USDA_API_KEY'
food_query = 'apple'
food_data = fetch_usda_food_data(api_key, food_query)
if food_data:
    add_usda_food_to_database(food_data)

#mydb.close()