################################################
##----------- Import packages here -----------##
import streamlit as st

################################################

def mainEunice():
    testEunice()
    #--- Put functions here to call it. ---#
    
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    pd.set_option('display.max_columns', 100)
    pd.set_option('display.max_rows', 100)
    
    # Load data
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
    
    #combine all into one dataframe
    df_all = pd.concat([df_schools, df_location, df_rooms, df_teachers, df_elementary, df_secondary, df_mooe], axis=1)
    
    # Obtain all numeric features + school.classification
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
    # Create ratios
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
    # remove infinity
    df_outlier_removed = df_outlier_removed.replace([np.inf, -np.inf], np.nan)
    df_outlier_removed = df_outlier_removed.dropna()
    
    df_corr = df_outlier_removed.drop(['school.region', 'school.cityincome', 'school.classification' ],axis = 1)
    
    
    # create correlation matrix
    plt.figure(figsize=(12,10))
    sns.set_theme()
    ax = sns.heatmap(df_corr.corr(), annot=True, fmt='.2f',)
    
    
    # prepare data for kmeans
    df_ratio_ss = df_corr[['Enrolment', ' school.mooe ', 'rooms_total',
       'teachers_total' ]]
    
    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    df_scaled_ss = scaler.fit_transform(df_ratio_ss)
    
    #run kmeans
    from sklearn.cluster import KMeans
    model = KMeans(n_clusters=3)
    model.fit(df_scaled_ss)
    cluster_labels = model.predict(df_scaled_ss)   

    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(df_scaled_ss)
    cluster_labels = kmeans.predict(df_scaled_ss)   


    df_ratio_ss['Cluster_Labels'] = cluster_labels

    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler()
    df_minmax = scaler.fit_transform(df_ratio_ss)

    df_minmax = pd.DataFrame(df_minmax, index=df_ratio_ss.index, columns=df_ratio_ss.columns)

    df_minmax['Cluster_Labels'] = cluster_labels

    df_clusters = df_minmax.set_index("Cluster_Labels")
    df_clusters = df_clusters.groupby("Cluster_Labels").mean().reset_index()
    
    from math import pi
    def make_spider(row, title, color):

        # number of variable
        categories=list(df_clusters)[1:]
        N = len(categories)

        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        # Initialise the spider plot
        ax = plt.subplot(3,3,row+1, polar=True )

        # If you want the first axis to be on top:
        ax.set_theta_offset(pi / 3.5)
        ax.set_theta_direction(-1)

        # Draw one axe per variable + add labels labels yet
        plt.xticks(angles[:-1], categories, color='grey', size=8)

        # Draw ylabels
        ax.set_rlabel_position(0)
    #     plt.yticks([-2, -1, 0, 1, 2], [-2,-1, 0, 1, 2], color="grey", size=7) #for sscaled
    #     plt.ylim(-2.5,2.5)
        plt.yticks([-0.25, 0, 0.25, 0.5, 0.75, 1], [-0.25, 0, 0.25, 0.5,0.75, 1], color="grey", size=7) #formmscaled
        plt.ylim(-0.25,1)

        # Ind1
        values=df_clusters.loc[row].drop('Cluster_Labels').values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, color=color, linewidth=2, linestyle='solid')
        ax.fill(angles, values, color=color, alpha=0.4)

        # Add a title
        plt.title(title, size=14, color=color, y=1.1)
        
    #show spider graph
    my_dpi=100
    fig = plt.figure(figsize=(1000/my_dpi, 1000/my_dpi), dpi=my_dpi)
    plt.subplots_adjust(hspace=0.5)

    # Create a color palette:
    my_palette = plt.cm.get_cmap("Set2", len(df_clusters.index))

    for row in range(0, len(df_clusters.index)):
        make_spider(row=row, 
                    title='Cluster '+(df_clusters['Cluster_Labels'][row]).astype(str), 
                    color=my_palette(row))
    
    
    #add title
    st.title('Clusters formed after K-Means Clustering')
    #plot to streamlit
    st.pyplot(fig)
    st.text("""Three clusters have similar shape, but different magnitude.
Cluster 0 – lowest resources allocated
Cluster 1 – quantity of resources in between the two clusters
Cluster 2 – highest resources allocated
""")
    
    # prepare df for multiple bar graphs
    df_outlier_removed['Cluster_Labels'] = df_ratio_ss['Cluster_Labels']
    df_outlier_removed.groupby(['Cluster_Labels', 'school.cityincome']).size()
    income = ['Below P 15 M', 'P 15 M or more but less than P 25 M', 'P 25 M or more but less than P 35 M', 
             'P 35 M or more but less than P 45 M', 'P 45 M or more but less than P 55 M', 
            'P 55 M or more', 'P 80 M or more but less than P 160 M', 
             'P 160 M or more but less than P 240 M', 'P 240 M or more but less than P 320 M', 
             'P 320 M or more but less than P 400 M', 'P 400 M or more', 'Special Class']
    df_outlier_removed['school.cityincome'] = pd.Categorical(df_outlier_removed['school.cityincome'], 
                                                             categories=income, ordered=True)
    
    
    #create dfs for city income and clusters
    zero = df_outlier_removed[df_outlier_removed['Cluster_Labels']==0]['school.cityincome'].value_counts(sort=False).reset_index()
    one = df_outlier_removed[df_outlier_removed['Cluster_Labels']==1]['school.cityincome'].value_counts(sort=False).reset_index()
    two = df_outlier_removed[df_outlier_removed['Cluster_Labels']==2]['school.cityincome'].value_counts(sort=False).reset_index()
    
    zero['proportion'] = zero['school.cityincome']/zero['school.cityincome'].sum()
    one['proportion'] = one['school.cityincome']/one['school.cityincome'].sum()
    two['proportion'] = two['school.cityincome']/two['school.cityincome'].sum()
    
    #plot multiple bar graphs per city income and clusters
    fig2, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(12,10),  constrained_layout=True, sharex=True)
    ax1.bar(zero['index'], zero['proportion'])
    ax1.set_title('Cluster 0', fontsize=14)
    ax1.set_ylabel('proportion, n=23959', fontsize=14)
    ax2.bar(one['index'], one['proportion'])
    ax2.set_title('Cluster 1', fontsize=14)
    ax2.set_ylabel('proportion, n=9723', fontsize=14)
    ax3.bar(two['index'], two['proportion'])
    ax3.set_title('Cluster 2', fontsize=14)
    ax3.set_ylabel('proportion, n=2588', fontsize=14)
    ax1. set_ylim(0, 0.4)
    ax2. set_ylim(0, 0.4)
    ax3. set_ylim(0, 0.4)
    plt.xticks(rotation=45)
    fig2.suptitle('Distribution of Cluster according to City Income', fontsize=16)
    
    #plot to streamlit
    st.title("Distribution of Cluster according to City Income")
    st.pyplot(fig2)
    st.text(""" For all clusters
The highest proportion of schools belongs to the P45-55 M income class
The proportion of schools in lower income municipalities are greater compared to higher income municipalities

""")
    
    st.text(""" Proportion of schools in lower income municipalities slightly decreases from Cluster 0 to Cluster 2
 """)
    st.text(""" Proportion of schools in higher income municipalities slightly increases from Cluster 0 to Cluster 2""")

def sampleStreamLit():
    st.title("This is Eunice's Streamlit page")
    st.header("Sample header")
    st.text('Sample text')












########################################################################
#---------------     Don't edit functions below this     --------------#
########################################################################
def testEunice():
    print("Running from Eunice")
    
if __name__ == "__main__":
    mainEunice()