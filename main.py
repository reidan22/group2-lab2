from f_all import *

def main():
    testConnection()
    streamlit_main()

def streamlit_main():
    print("streamlit_main running...")
    my_page = st.sidebar.radio('Page Navigation', ['Background', 'Data Information', 'Methodology', 'Data Presentation', 'Conclusions and Recommendations'])
    if my_page == 'Background':
        st.title("Background")

    elif my_page == "Data Information":
        st.title("Data Information")

    elif my_page == "Methodology":
        st.title("Methodology")
        mainEunice()

    elif my_page == "Data Presentation":
        st.title("Data Presentation")

    elif my_page == 'Conclusions and Recommendations':
        st.title('Conclusions and Recommendations')

if __name__ == "__main__":
    main()