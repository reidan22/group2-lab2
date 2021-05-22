################################################
##----------- Import packages here -----------##
import streamlit as st

################################################

def mainShawn():
    testShawn()
    st.markdown("---")
    st.header("Methodology")
    st.image("./assets/Methodology.png")
    st.markdown("---")
    #sampleStreamLit()


def sampleStreamLit():
    st.title("This is Shawn's Streamlit page")
    st.header("Sample header")
    st.text('Sample text')












########################################################################
#---------------     Don't edit functions below this     --------------#
########################################################################
def testShawn():
    print("Running from Shawn")
    
if __name__ == "__main__":
    mainShawn()