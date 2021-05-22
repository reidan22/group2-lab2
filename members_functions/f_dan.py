################################################
##----------- Import packages here -----------##
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
################################################

def mainDan():
    testDan()
    #--- Put functions here to call it. ---#
    st.markdown("---")
    st.title("EDA")
    df2 = pd.read_csv('./assets/schools_with_mooe.csv')
    school = df2[["school.id"]]
    school_type = df2["school.classification"]
    rooms = df2['rooms.standard.academic'] + df2['rooms.standard.unused']+ df2['rooms.nonstandard.academic']+ df2["rooms.nonstandard.unused"]
    teachers = df2['teachers.instructor']+ df2['teachers.mobile']+df2['teachers.regular']+df2['teachers.sped']
    learner = df2["school.enrollment"]
    mooe = df2['school.mooe']
    df2["rooms"]=rooms
    df2["teachers"]=teachers

    data_original = df2[["school.id","school.classification","rooms","teachers","school.enrollment",'school.mooe']]
    data = df2[["school.id","school.classification","rooms","teachers","school.enrollment",'school.mooe']]

    data["teachersX"]= data["school.classification"].apply(lambda x: 4000 if x == "Elementary" else 8000)
    data["roomsX"]= data["school.classification"].apply(lambda x: 3000 if x == "Elementary" else 6000)
    data["learnersX"]= data["school.classification"].apply(lambda x: 200 if x == "Elementary" else 400)
    data["fixedX"]= data["school.classification"].apply(lambda x: 40000 if x == "Elementary" else 80000)
    boncodin = data["fixedX"] + (data["rooms"]*data["roomsX"]) + (data["learnersX"]*data["school.enrollment"]) + (data["teachersX"]*data["teachers"])
    data["boncodin"]= boncodin
    data["mooe-boncodin"] = data["school.mooe"]-boncodin
    data_cleaned = data.dropna()
    def showCorr(df):
        ax = plt.figure(figsize=(10,6))
        expected = np.log(df["boncodin"])
        actual = np.log(df["school.mooe"])
        plt.xlabel("boncodin")
        plt.ylabel("school.mooe")
        plt.scatter(expected,actual)
        st.pyplot(plt)

    
    def getCorr(df):
        correlation, p_value = stats.pearsonr(df["boncodin"], df["school.mooe"])
        return "Correlation is: "+ str(correlation)

    def showBoxPlot(df):
        df = df[["school.id","school.mooe","boncodin"]]
        plt.figure(figsize=(12,6))
        sns.boxplot(x="value", y="variable", data=pd.melt(df[["school.mooe","boncodin"]]))
        st.pyplot(plt)
        # plt.title("Distribution of Scores in the National Achievement Test")
        
    def removeOutliers(df):
        #Removing outliers
        Q1 = df['school.mooe'].quantile(0.25)
        Q3 = df['school.mooe'].quantile(0.75)
        IQR = Q3 - Q1

        df = (df[(df['school.mooe'] >= Q1 - 1.5*IQR) & (df['school.mooe'] <= Q3 + 1.5*IQR)])
        return df




    data_outliers_removed = removeOutliers(data_cleaned)
    data_outliers_removed_1 = removeOutliers(data_outliers_removed)
    st.markdown(" The graph shows a correlation between **Actual MOOE** received by schools and **Boncodin MOOE** with a correlation of **0.99**")
    showCorr(data_outliers_removed_1)
    getCorr(data_outliers_removed_1)
    st.markdown("However, the boxplot below shows a lot of outliers existing in the data with by **20%** of the original dataset.")
    st.markdown("This gives an insight to the researchers the nature of the dataset having huge discrepancies between the Actual MOOE and Boncodin MOOE.")
    showBoxPlot(data_outliers_removed_1)
    
    data_cleaned["diff"] = (data_cleaned["school.mooe"]-data_cleaned["boncodin"])

    plt.figure(figsize=(10,6))
    df3 = df2.merge(data_cleaned,on="school.id", how="left")
    df_plot = df3[["school.name_x","school.region","school.mooe_x","boncodin","diff"]].dropna()
    df_new = df_plot.groupby("school.region").sum()

    labels = df_new.index
    mooe = df_new["school.mooe_x"]
    boncodin = df_new["boncodin"]
    width = 0.35       # the width of the bars: can also be len(x) sequence
    df_school = df_plot
    df_school["diff"] = df_school["diff"].abs()
    df_new["region"]=df_new.index
    labels = df_new["region"]
    mooe = df_new["school.mooe_x"]
    boncodin = df_new["boncodin"]
    width = 0.35       # the width of the bars: can also be len(x) sequence
    x = np.arange(len(labels))  # the label locations
    fig, ax = plt.subplots()

    fig.set_figheight(10)
    fig.set_figwidth(20)

    rects1 = ax.bar(x - width/2, mooe, width, label='Actual MOOE')
    rects2 = ax.bar(x + width/2, boncodin, width, label='Boncodin MOOE')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Amount in Php 1,000,000,000',fontsize=16)
    ax.set_xlabel('Region',fontsize=16)
    ax.set_title('Difference of Actual MOOE and Boncodin MOOE per Region',fontsize=24)
    ax.legend()
    st.markdown("The graph below shows the difference in Actual MOOE and Boncodin MOOE per region")
    st.markdown("The regions having the highest difference between the two come from **NCR, Region III, and Region IV-A**")

    st.pyplot(fig)
    st.markdown("By looking at the data, this discrepancy reaches as high as **Php 6316200**")
    st.markdown("Showing that the current **Boncodin MOOE isn't representative** of what these schools are actually spending.")


    st.dataframe(df_school.sort_values(by="diff",ascending=False).head(10))
    st.markdown("---")

########################################################################
#---------------     Don't edit functions below this     --------------#
########################################################################
def testDan():
    print("Running from Dan")
    
if __name__ == "__main__":
    mainDan()