################################################
##----------- Import packages here -----------##
import streamlit as st

################################################

def mainRenzo():
    testRenzo()
    #--- Put functions here to call it. ---#
    sampleStreamLit()


def sampleStreamLit():
    st.title("This is Renzo's Streamlit page")
    st.header("Sample header")
    st.text('Sample text')












########################################################################
#---------------     Don't edit functions below this     --------------#
########################################################################
def testRenzo():
    print("Running from Renzo")
    
if __name__ == "__main__":
    mainRenzo()