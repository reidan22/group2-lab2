################################################
##----------- Import packages here -----------##
import streamlit as st

################################################

def mainBevs():
    testBevs()
    #--- Put functions here to call it. ---#
    sampleStreamLit()

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
    st.text('Sample text')












########################################################################
#---------------     Don't edit functions below this     --------------#
########################################################################
def testBevs():
    print("Running from Bevs")
    
if __name__ == "__main__":
    mainBevs()
