from database import collection



#CALCULATE MACROS FOR RESULT
def calculate_macronutrient_goals(weight_goal: float, height: float, weight: int, age: int):
    # calculate Total Daily Energy Expenditure [TDEE]
    if age <= 30:
        bmr = 10 * weight + 6.25 * height - 5 * age + 5  # BMR for ages <= 30
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161  # BMR for ages > 30

    if weight_goal == 11:  # gain weight
        tdee = bmr * 1.2  # activity level
        calories = tdee + 1100  # add surplus calories for weight gain
    elif weight_goal == 33:  # lose weight
        tdee = bmr * 1.2  # activity level
        calories = tdee - 400  # subtract deficit calories for weight loss
    else:  # maintain weight
        tdee = bmr * 1.375  # activity level
        calories = tdee + 400

    # calculate macronutrient amounts
    protein = weight * 1.3  # Protein intake in grams
    fat = (calories * 0.25) / 9  # Fat intake in grams

    # ensure carbohydrates are not negative
    carbohydrates = max((calories - (protein * 4) - (fat * 9)) / 4, 0)  # Carbs in grams

    # calculate total recommended calories for macros
    total_recommended_calories = protein * 4 + fat * 9 + carbohydrates * 4

    return protein, fat, carbohydrates, total_recommended_calories

#function to create account
async def create_account(user_id):
    try:
        find = collection.find_one({"_id": user_id})
    except Exception as e:
        print("An error occurred while querying the database:", e)
        return

    if find is not None:
        print("User already exists.")
        return

    print("Creating account for user:", user_id)
    try:
        result = collection.insert_one({
            "_id": user_id,
            "protein": 0,
            "fat": 0,
            "carbohydrates": 0,
            "total_calories": 0,
            "upper_count": 0,
            "lower_count": 0,
            "push_count": 0,
            "pull_count": 0,
            "legs_count": 0,
        })
        print("Inserted new document:", result.inserted_id)
    except Exception as e:
        print("An error occurred while creating an account:", e)

# STORE MACROS ACCOUNT FUNCTION
async def store_macros(user_id, protein, fat, carbohydrates, total_calories):
    try:
        result = collection.update_one({"_id": user_id}, {"$set": {
            "protein": protein,
            "fat": fat,
            "carbohydrates": carbohydrates,
            "total_calories": total_calories
        }})
        if result.modified_count == 0:
            print("User document not found. Creating account...")
            await create_account(user_id)  # Call create_account if the user document doesn't exist
        else:
            print("Updated document:", result.modified_count)
    except Exception as e:
        print("An error occurred while storing macros:", e)