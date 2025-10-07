import pandas as pd
def categorie_age(age) :
    if age<=32 :
        return "18-32 ans"
    elif (age>32)&(age<=48)  :
        return "32-48 ans"
    elif (age >48) :
        return ">48 ans"
def dataset() :
    data= pd.read_csv(r"dataset\bank-full.csv", sep=';')
    data["cate_age"] =data["age"].map(categorie_age)

    return data
def type_col()  : 
    data= dataset()
    numerical_cols = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
    return numerical_cols,categorical_cols




