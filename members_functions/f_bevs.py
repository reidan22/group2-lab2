################################################
##----------- Import packages here -----------##
import streamlit as st

################################################

def mainBevs():
    testBevs()
    #--- Put functions here to call it. ---#
    sampleStreamLit()


def sampleStreamLit():
    st.title("This is Bevs's Streamlit page")
    st.header("Sample header")
    st.text('Sample text')












########################################################################
#---------------     Don't edit functions below this     --------------#
########################################################################
def testBevs():
    print("Running from Bevs")
    
if __name__ == "__main__":
    mainBevs()