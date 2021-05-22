################################################
##----------- Import packages here -----------##
import streamlit as st

################################################

def mainRenzo():
    testRenzo()
    #--- Put functions here to call it. ---#
    st.title("MOOE")
    st.header("THE GREAT and POWERFUL")

    st.header("An exploratory data analysis of the nature and effect of MOOE in PH public schools.")
    st.text('COHORT 7 - SPRINT 1 - GROUP 2')
    st.text('Mentor: Sasa')
    st.markdown(""" 
        | Members                |
        | ------------- |:-------------:|
        | Eunice | Bev |
        | Renzo | Shawn |
        | Dan | |
    """)
    st.markdown("---")

    
    st.title('Background')
    st.header('Maintenance and Other Operating Expenses (MOOE)')
    st.write('The Department of Education allocates the annual budget for public schools based on their MOOE. The basis of the calculation of the MOOE is the Boncodin formula.')

    st.title('BONCODIN FORMULA')
    st.latex(""" 
        BoncodinMOOE = Fixed Amount + ClassroomFactor + TeacherFactor + StudentFactor
    """)
    st.write("where:")
    st.latex(""" 
        ClassroomFactor = AllowableAmount(Classroom) * NumberOfClassrooms
    """)
    st.latex(""" 
        TeacherFactor = AllowableAmount(Teacher) * NumberOfTeachers
    """)
    st.latex(""" 
        StudentFactor = AllowableAmount(Student) * NumberOfStudents
    """)
    st.subheader("Allowable() for 2015")
    st.markdown(""" 
        | Basis | Elementary | Secondary |
        | ------------- |:-------------:|:-------------:|
        | Every Classroom | Php3,000 | Php6,000 |
        | Every Teacher | Php4,000 | Php8,000 |
        | Every Learner | Php200 | Php400 |
 
    """)
    st.markdown("[https://www.teacherph.com/computation-public-schools-mooe/]")
    st.markdown("---")

    st.title("Investigation")
    st.header("1. Are there alternative methods to determine the allocated budget for public schools’ MOOE?")
    st.header("2. What other factors can be considered in determining public schools’ MOOE?")
    st.header("3. Can school capacity be considered in determining a school’s allocated budget for MOOE?")
    st.markdown("---")










########################################################################
#---------------     Don't edit functions below this     --------------#
########################################################################
def testRenzo():
    print("Running from Renzo")
    
if __name__ == "__main__":
    mainRenzo()