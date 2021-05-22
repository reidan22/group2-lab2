################################################
##----------- Import packages here -----------##
import streamlit as st

################################################

def mainRenzo():
    testRenzo()
    #--- Put functions here to call it. ---#
    sampleStreamLit()


def sampleStreamLit():
    st.title("MOOE - The Great and Powerful")
    st.header("An exploratory analysis of the nature and effect of MOOE in PH public schools")
    st.text('COHORT 7 - SPRINT 1 - GROUP 2')

    
    st.title('Background')
    st.header('Maintenance and Other Operating Expenses (MOOE)')
    st.text('The Department of Education allocates the annual budget for public schools based on their MOOE. The basis of the calculation of the MOOE is the Boncodin formula.')
    
    st.title('BONCODIN FORMULA')
    st.header('MOOE = Fixed Amount + (Allowable amount * Number of Classrooms) + (Allowable amount * Number of Teachers) + (Allowable amount * Number of Learners)')

    st.title("Investigation")
    st.header("1. Are there alternative methods to determine the allocated budget for public schools’ MOOE?")
    st.header("2. What other factors can be considered in determining public schools’ MOOE?")
    st.header("3. Can school capacity be considered in determining a school’s allocated budget for MOOE?")







########################################################################
#---------------     Don't edit functions below this     --------------#
########################################################################
def testRenzo():
    print("Running from Renzo")
    
if __name__ == "__main__":
    mainRenzo()