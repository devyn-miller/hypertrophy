user_table = '''
CREATE TABLE users(
    userID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    username VARCHAR(32),
    password VARCHAR(32)
);
'''

recipe_table = '''
CREATE TABLE recipes(
    recipeID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    recipeName VARCHAR(128),
    deleted BOOLEAN DEFAULT False,
    userID INTEGER
);
'''

food_table = '''
CREATE TABLE foods(
    foodID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    storeID Integer,
    foodName VARCHAR(128)
);
'''

food_in_recipe_table = '''
CREATE TABLE foodrecipe(
    foodrecipeID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    recipeID INTEGER,
    foodID INTEGER
);
'''

instruction_table = '''
CREATE TABLE instructions(
    instructionID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    instructionText TEXT,
    sourceURL VARCHAR(128),
    recipeID INTEGER
);
'''

store_table = '''
CREATE TABLE stores(
    storeID INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    storeName VARCHAR(64),
    address VARCHAR(128)
);
'''

