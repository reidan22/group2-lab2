################################################
##----------- Import packages here -----------##
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
################################################

def mainBevs():
    testBevs()
    #--- Put functions here to call it. ---#
    sampleStreamLit()

    pd.set_option('display.max_columns', 100)
    pd.set_option('display.max_rows', 100)

    #Loading and compiling dataset
    df_schools = pd.read_csv("./assets/Masterlist of Schools.csv", index_col="school.id")

    df_location = pd.read_csv("./assets/Schools Location Data.csv", 
                          encoding = "latin-1", 
                          index_col="School ID",
                          usecols=["School ID", "Enrolment", "Latitude", "Longitude"])

    df_rooms = pd.read_csv('./assets/Rooms data.csv', index_col="School ID")

    df_teachers = pd.read_csv("./assets/Teachers data.csv", index_col="school.id")

    df_elementary = pd.read_csv("./assets/Enrollment Master Data_2015_E.csv")[:-1].astype(int).set_index("School ID")

    df_secondary = (pd.read_csv('./assets/Enrollment Master Data_2015_S.csv')[:-1]
                  .replace(",", "", regex=True)
                  .astype(int)
                  .replace("SPED NG Male", "SPED NG Male SS")
                  .replace("SPED NG Female", "SPED NG Female SS")
                  .set_index("School ID"))

    df_mooe = (pd.read_csv('./assets/MOOE data.csv', index_col="school.id", usecols=["school.id", " school.mooe "])
             .replace(",", "", regex=True).astype(float))

    #Saving all datasets into one data frame
    df_all = pd.concat([df_schools, df_location, df_rooms, df_teachers, df_elementary, df_secondary, df_mooe], axis=1)
    df_all

    #Checking the shape
    df_all.shape

    #Checking for missing values
    df_all.isna().sum()

    #Checking for duplicates
    df_all[df_all.index.duplicated(keep=False)]

    # Obtain all numeric features and school.classification
    df_numeric = df_all[['school.region', 'school.cityincome','rooms.standard.academic', 'rooms.standard.unused',
       'rooms.nonstandard.academic', 'rooms.nonstandard.unused',
       'teachers.instructor', 'teachers.mobile', 'teachers.regular',
       'teachers.sped','Enrolment', ' school.mooe ', 'school.classification']]

    # Combine all rooms and all teachers
    df_numeric["rooms_total"] = (df_numeric['rooms.standard.academic'] + 
                             df_numeric['rooms.standard.unused'] + 
                             df_numeric['rooms.nonstandard.academic'] + 
                             df_numeric['rooms.nonstandard.unused'])

    df_numeric["teachers_total"] = (df_numeric['teachers.instructor'] + 
                             df_numeric['teachers.mobile'] + 
                             df_numeric['teachers.regular'] + 
                             df_numeric['teachers.sped'])

    df_numeric['student_teacher_ratio'] = df_numeric['Enrolment']/df_numeric["teachers_total"]
    df_numeric['student_room_ratio'] = df_numeric['Enrolment']/df_numeric["rooms_total"]
    df_numeric['student_mooe_ratio'] = df_numeric['Enrolment']/df_numeric[' school.mooe ']

    df_numeric = df_numeric.dropna()

    # Removing (statistical) outliers for MOOE
    Q1 = df_numeric[' school.mooe '].quantile(0.25)
    Q3 = df_numeric[' school.mooe '].quantile(0.75)
    IQR = Q3 - Q1

    df_outlier_removed = (df_numeric[(df_numeric[' school.mooe '] >= Q1 - 1.5*IQR) & 
                           (df_numeric[' school.mooe '] <= Q3 + 1.5*IQR)])
    df_outlier_removed.columns

    #Checking the dataset
    df_numeric ["school.cityincome"] = df_numeric["school.cityincome"].replace(['P 55 M or more'],'P 55 M or more but less than P 80 M')
    df_numeric

    #reordering categories
    df_numeric["school.cityincome"] = df_numeric["school.cityincome"].astype('category')
    df_numeric["school.cityincome"].cat.reorder_categories(['Below P 15 M', 'P 15 M or more but less than P 25 M', 
       'P 25 M or more but less than P 35 M',
       'P 35 M or more but less than P 45 M',
       'P 45 M or more but less than P 55 M',
       'P 55 M or more but less than P 80 M',
       'P 80 M or more but less than P 160 M',                                                 
       'P 160 M or more but less than P 240 M',
       'P 240 M or more but less than P 320 M',
       'P 320 M or more but less than P 400 M',
       'P 400 M or more',
       'Special Class'])

    #Getting the no. of students per city classified by income
    students_per_city_income = df_numeric.groupby("school.cityincome").agg(Enrolment=("Enrolment", sum))
    students_per_city_income

    #Plotting the bar graph for students per city classified by income
    plt.figure(figsize=(12,6), dpi = 80)
    plt.barh(students_per_city_income.index, students_per_city_income["Enrolment"].values)
    plt.title("Students")
    plt.ticklabel_format(axis="x", style="plain")
    plt.show

    # display graph
    st.pyplot(fig)

    #Getting the no. of teachers per city classified by income
    teachers_per_city_income = df_numeric.groupby("school.cityincome").agg(Teachers=("teachers_total", sum))
    teachers_per_city_income

    #Plotting the bar graph for teachers per city classified by income
    plt.figure(figsize=(12,6), dpi = 80)
    plt.barh(teachers_per_city_income.index, teachers_per_city_income["Teachers"].values)
    plt.title("Teachers")
    plt.ticklabel_format(axis="x", style="plain")
    plt.show

    # display graph
    st.pyplot(fig)

    #Getting the no. of rooms per city classified by income
    rooms_per_city_income = df_numeric.groupby("school.cityincome").agg(Rooms=("rooms_total", sum))
    rooms_per_city_income

    #Plotting the bar graph for rooms per city classified by income
    plt.figure(figsize=(12,6), dpi=80)
    plt.barh(rooms_per_city_income.index, rooms_per_city_income["Rooms"].values)
    plt.title("Rooms")
    plt.ticklabel_format(axis="x", style="plain")
    plt.show

    # display graph
    st.pyplot(fig)

    #Getting the total MOOE per city classified by income
    mooe_per_city_income = df_numeric.groupby("school.cityincome").agg(MOOE_per_city_income=(" school.mooe ",sum))
    mooe_per_city_income

    #Plotting the bar graph for total MOOE per city classified by income
    plt.figure(figsize=(12,6), dpi = 80)
    plt.barh(mooe_per_city_income.index, mooe_per_city_income ["MOOE_per_city_income"].values)
    plt.title("Total MOOE")
    plt.ticklabel_format(axis="x", style="plain")
    plt.show

    # display graph
    st.pyplot(fig)


def sampleStreamLit():
    st.title("An Exploratory Analysis of Public School Resources According to City Income Level")
    st.header("Sample header")
    st.text("Schools with the most no. of students and the most no. of resources (rooms, teachers, and MOOE) are located in cities with an income level of 55M or more but less than P80 M.")
    st.text("Schools with the least no. of students and the least no. of resources (rooms, teachers, and MOOE) are located in cities with an income level of P 80M or more but less than P 160 M.")










########################################################################
#---------------     Don't edit functions below this     --------------#
########################################################################
def testBevs():
    print("Running from Bevs")
    
if __name__ == "__main__":
    mainBevs()
