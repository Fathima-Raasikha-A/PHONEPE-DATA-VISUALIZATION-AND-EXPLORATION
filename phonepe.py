import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json

# creating dataframes

#sql database creation

mydb=psycopg2.connect(host= "localhost",
                     user="postgres",
                     password= "anasrazi",
                     database="phonepe_data_analysis",
                     port="5432"
                     )
cursor=mydb.cursor()

#1. for aggregated_transaction_df

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()

table1=cursor.fetchall()

Aggregated_transaction = pd.DataFrame(table1,columns=("states","years", "quarter", "Trans_type","Trans_count", "Trans_amount"))

#2.for aggregated users:

cursor.execute("SELECT * FROM aggregated_users")
mydb.commit()

table2=cursor.fetchall()

Aggregated_users = pd.DataFrame(table2,columns=("states","years", "quarter", "Brand","Trans_count", "Percentage"))

#3.Map_transaction:

cursor.execute("SELECT * FROM map_transaction")
mydb.commit()

table3=cursor.fetchall()

map_transaction = pd.DataFrame(table3,columns=("states","years", "quarter", "Dist_name","Trans_count", "Trans_amount"))

#4.map_users

cursor.execute("SELECT * FROM map_users")
mydb.commit()

table4=cursor.fetchall()

map_users = pd.DataFrame(table4,columns=("states","years", "quarter", "Dist_name","Reg_Users", "App_opened"))

#top_transaction

cursor.execute("SELECT * FROM top_transaction")
mydb.commit()

table5=cursor.fetchall()

top_transaction = pd.DataFrame(table5,columns=("State","Year", "quarter", "Dist_name","Trans_count", "Trans_amount"))

#top_users
cursor.execute("SELECT * FROM top_users")
mydb.commit()

table6=cursor.fetchall()

top_users = pd.DataFrame(table6,columns=("states","years", "quarter", "Pincode","Reg_Users"))


def Trans_countamount_Y_G(df,year):
    Trans_countamount_Y = df[df["years"]==year]
    Trans_countamount_Y.reset_index(inplace=True)

    # Trans_countamount_Y _Group:

    Trans_countamount_Y_Group = Trans_countamount_Y.groupby("states")[["Trans_count","Trans_amount"]].sum()
    Trans_countamount_Y_Group.reset_index(inplace=True)

    #Plotting details:

    col1,col2= st.columns(2)
    with col1:
        fig_amount = px.bar(Trans_countamount_Y_Group, x="states", y="Trans_amount", title=f"{year}  Transaction Amount",
                            color_discrete_sequence= px.colors.sequential.Bluered, height=650, width=600)

        st.plotly_chart(fig_amount)
    with col2:
        fig_count = px.bar(Trans_countamount_Y_Group, x="states", y="Trans_count", title=f"{year}  Transaction Count",
                            color_discrete_sequence= px.colors.sequential. Agsunset,height=650, width=600)

        st.plotly_chart(fig_count)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)

    state_names=[]

    data1=json.loads(response.content)

    for feature in data1["features"]:
        state_names.append(feature["properties"]["ST_NM"])

    state_names.sort()
    col1,col2=st.columns(2)
    with col1:
        fig_india_1 = px.choropleth(Trans_countamount_Y_Group, geojson=data1, locations="states",
                                featureidkey="properties.ST_NM", color= "Trans_amount", 
                                color_continuous_scale= "Emrld",
                                range_color=(Trans_countamount_Y_Group["Trans_amount"].min(),
                                Trans_countamount_Y_Group["Trans_amount"].max()),
                                hover_name="states", title=f"{year}  TRANSACTION AMOUNT",
                                fitbounds="locations", height= 600, width = 600)
                                
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2 = px.choropleth(Trans_countamount_Y_Group, geojson=data1, locations="states",
                                featureidkey="properties.ST_NM", color= "Trans_count", 
                                color_continuous_scale= "Redor",
                                range_color=(Trans_countamount_Y_Group["Trans_count"].min(),
                                Trans_countamount_Y_Group["Trans_count"].max()),
                                hover_name="states", title=f"{year}  TRANSACTION COUNT",
                                fitbounds="locations", height= 600, width = 600)
                                
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return Trans_countamount_Y


def Trans_countamount_Y_T(df,state):
    Trans_countamount_Y_T1 = df[df["states"]==state]
    Trans_countamount_Y_T1.reset_index(inplace=True)

    # Trans_countamount_Y _Group:

    Trans_countamount_Y_T1_Group = Trans_countamount_Y_T1.groupby("Trans_type")[["Trans_count","Trans_amount"]].sum()
    Trans_countamount_Y_T1_Group.reset_index(inplace=True)

    #Plotting details:
    
    col1,col2= st.columns(2)
    with col1:

        fig_1= px.bar(Trans_countamount_Y_T1_Group, x= "Trans_count", y= "Trans_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 600, 
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION COUNT",height= 500)
        st.plotly_chart(fig_hbar_1)

    with col2:

        fig_hbar_2= px.bar(Trans_countamount_Y_T1_Group, x= "Trans_amount", y= "Trans_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 600,
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", height= 500)
        st.plotly_chart(fig_hbar_2)

    return Trans_countamount_Y_T1

def Trans_countamount_Y_Q(df,quarter):
    Trans_countamount_Y = df[df["quarter"]==quarter]
    Trans_countamount_Y.reset_index(inplace=True)

    # Trans_countamount_Y _Group:

    Trans_countamount_Y_Group = Trans_countamount_Y.groupby("states")[["Trans_count","Trans_amount"]].sum()
    Trans_countamount_Y_Group.reset_index(inplace=True)

    #Plotting details:
    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(Trans_countamount_Y_Group, x="states", y="Trans_amount", 
                            title=f"{Trans_countamount_Y["years"].min()} Q{quarter}   Transaction Amount",
                                color_discrete_sequence= px.colors.sequential.Bluered, height=650, width=600)

        st.plotly_chart(fig_amount)
    with col2:
        fig_count = px.bar(Trans_countamount_Y_Group, x="states", y="Trans_count",
                            title=f"{Trans_countamount_Y["years"].min()} Q{quarter}  Transaction Count",
                                color_discrete_sequence= px.colors.sequential. Agsunset,height=650, width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)

        state_names=[]

        data1=json.loads(response.content)

        for feature in data1["features"]:
            state_names.append(feature["properties"]["ST_NM"])

        state_names.sort()

        fig_india_1 = px.choropleth(Trans_countamount_Y_Group, geojson=data1, locations="states",
                                featureidkey="properties.ST_NM", color= "Trans_amount", 
                                color_continuous_scale= "Emrld",
                                range_color=(Trans_countamount_Y_Group["Trans_amount"].min(),Trans_countamount_Y_Group["Trans_amount"].max()),
                                hover_name="states", title=f"{Trans_countamount_Y["years"].min()} Q{quarter}  TRANSACTION AMOUNT",
                                fitbounds="locations", height= 600, width = 600)
                                
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2 = px.choropleth(Trans_countamount_Y_Group, geojson=data1, locations="states",
                                featureidkey="properties.ST_NM", color= "Trans_count", 
                                color_continuous_scale= "Redor",
                                range_color=(Trans_countamount_Y_Group["Trans_count"].min(),Trans_countamount_Y_Group["Trans_count"].max()),
                                hover_name="states", title=f"{Trans_countamount_Y["years"].min()} Q{quarter}  TRANSACTION COUNT",
                                fitbounds="locations", height= 600, width = 600)
                                
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2) 

def AguS_Y_B(df,year):
    AguS_YB = df[df["years"]==year]
    AguS_YB.reset_index(inplace=True)

    # Trans_countamount_Y _Group:

    AguS_YB_Group = AguS_YB.groupby("Brand")[["Trans_count","Percentage"]].sum()
    AguS_YB_Group.reset_index(inplace=True)

    #Plotting details:
    
    fig_count = px.bar(AguS_YB_Group, x="Brand", y="Trans_count", title=f"{year}  Transaction count",
                            color_discrete_sequence= px.colors.sequential.Bluered, height=650, width=600)

    st.plotly_chart(fig_count)

    fig_percent = px.bar(AguS_YB_Group, x="Brand", y="Percentage", title=f"{year}  Percentage",
                            color_discrete_sequence= px.colors.sequential. Agsunset,height=650, width=600)
    st.plotly_chart(fig_percent)

    return AguS_YB


def AguS_Q_B(df,quarter):
    AguS_QB = df[df["quarter"]==quarter]
    AguS_QB.reset_index(inplace=True)

    # Trans_countamount_Y _Group:

    AguS_QB_Group = AguS_QB.groupby("Brand")[["Trans_count","Percentage"]].sum()
    AguS_QB_Group.reset_index(inplace=True)
    
    #Plotting details:
    fig_count = px.bar(AguS_QB_Group, x="Brand", y="Trans_count", title=f" Q{quarter}  Transaction count",
                                color_discrete_sequence= px.colors.sequential.Bluered, height=650, width=600)

    st.plotly_chart(fig_count)

    fig_percent = px.bar(AguS_QB_Group, x="Brand", y="Percentage", title=f" Q{quarter}  Percentage",
                            color_discrete_sequence= px.colors.sequential.Agsunset, height=650, width=600)
    
    st.plotly_chart(fig_percent)

    return AguS_QB   

def Aggre_user_S(df,state):
    aguqy= df[df["states"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    aguqyg= pd.DataFrame(aguqy.groupby("Brand")["Trans_count"].sum())
    aguqyg.reset_index(inplace= True)

    fig_scatter_1= px.line(aguqyg, x= "Brand", y= "Trans_count", markers= True,width=1000)

    st.plotly_chart(fig_scatter_1)


def map_trans_Y_G(df,year):
    map_trans_Y = df[df["years"]==year]
    map_trans_Y.reset_index(inplace=True)

    # map_trans_Y _Group:

    map_trans_Y_Group = map_trans_Y.groupby("Dist_name")[["Trans_count","Trans_amount"]].sum()
    map_trans_Y_Group.reset_index(inplace=True)

    #Plotting details:
    
    fig_amount = px.bar(map_trans_Y_Group, x="Dist_name", y="Trans_amount", title=f"{year}  Transaction Amount",
                            color_discrete_sequence= px.colors.sequential.Bluered, height=650, width=600)

    st.plotly_chart(fig_amount)

    fig_count = px.bar(map_trans_Y_Group, x="Dist_name", y="Trans_count", title=f"{year}  Transaction Count",
                            color_discrete_sequence= px.colors.sequential. Agsunset,height=650, width=600)
    st.plotly_chart(fig_count)

    return map_trans_Y

def map_trans_Q_G(df,quarter):
    map_trans_Q = df[df["quarter"]==quarter]
    map_trans_Q.reset_index(inplace=True)

    # map_trans_Q_Group:

    map_trans_Q_Group = map_trans_Q.groupby("Dist_name")[["Trans_count","Trans_amount"]].sum()
    map_trans_Q_Group.reset_index(inplace=True)

    #Plotting details:
    
    fig_amount = px.bar(map_trans_Q_Group, x="Dist_name", y="Trans_amount", title=f"Q{quarter}  Transaction Amount",
                            color_discrete_sequence= px.colors.sequential.Bluered, height=650, width=600)

    st.plotly_chart(fig_amount)

    fig_count = px.bar(map_trans_Q_Group, x="Dist_name", y="Trans_count", title=f"Q{quarter}  Transaction Count",
                            color_discrete_sequence= px.colors.sequential. Agsunset,height=650, width=600)
    st.plotly_chart(fig_count)

    return map_trans_Q

def map_user_1(df, year):
    map_user_y= df[df["years"] == year]
    map_user_y.reset_index(drop= True, inplace= True)
    map_user_y_g= map_user_y.groupby("states")[["Reg_Users", "App_opened"]].sum()
    map_user_y_g.reset_index(inplace= True)

    fig_map_user_1= px.line(map_user_y_g, x= "states", y= ["Reg_Users","App_opened"], markers= True,
                                width=1000,height=800,title= f"{year} REGISTERED USERS AND APP_OPENED", color_discrete_sequence= px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_map_user_1)

    return map_user_y

def map_user_2(df, quarter):
    map_user_q= df[df["quarter"] == quarter]
    map_user_q.reset_index(drop= True, inplace= True)
    map_user_q_g= map_user_q.groupby("states")[["Reg_Users", "App_opened"]].sum()
    map_user_q_g.reset_index(inplace= True)

    fig_map_user_1= px.line( map_user_q_g, x= "states", y= ["Reg_Users","App_opened"], markers= True,
                                title= f"{df['years'].min()}, Q {quarter} REGISTERED USERS AND APP_OPENED",
                                width= 1000,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_1)

    return  map_user_q

def map_user_3(df, state):
    map_user_state= df[df["states"] == state]
    map_user_state.reset_index(drop= True, inplace= True)
    map_user_state_g= map_user_state.groupby("Dist_name")[["Reg_Users", "App_opened"]].sum()
    map_user_state_g.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_1= px.bar(map_user_state_g, x= "Reg_Users",y= "Dist_name",orientation="h",
                                    title= f"{state.upper()} REGISTERED USERS",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_1)

    with col2:
        fig_map_user_2= px.bar(map_user_state_g, x= "App_opened", y= "Dist_name",orientation="h",
                                    title= f"{state.upper()} APP_OPENED",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_2)

def top_trans_Y_G(df,year):
    top_trans_Y = df[df["Year"]==year]
    top_trans_Y.reset_index(inplace=True)

    # top_trans_Y _Group:

    top_trans_Y_Group = top_trans_Y.groupby("Dist_name")[["Trans_count","Trans_amount"]].sum()
    top_trans_Y_Group.reset_index(inplace=True)

    #Plotting details:
    
    fig_amount = px.bar(top_trans_Y_Group, x="Dist_name", y="Trans_amount", title=f"{year}  Transaction Amount",
                            color_discrete_sequence= px.colors.sequential.Bluered, height=650, width=600)

    st.plotly_chart(fig_amount)

    fig_count = px.bar(top_trans_Y_Group, x="Dist_name", y="Trans_count", title=f"{year}  Transaction Count",
                            color_discrete_sequence= px.colors.sequential. Agsunset,height=650, width=600)
    st.plotly_chart(fig_count)

    return top_trans_Y

def top_trans_Q_G(df,quarter):
    top_trans_Q = df[df["quarter"] == quarter]
    top_trans_Q.reset_index(inplace=True)

    # top_trans_Q _Group:

    top_trans_Q_Group = top_trans_Q.groupby("Dist_name")[["Trans_count","Trans_amount"]].sum()
    top_trans_Q_Group.reset_index(inplace=True)

    #Plotting details:
    
    fig_amount = px.bar(top_trans_Q_Group, x="Dist_name", y="Trans_amount", title=f" Q{quarter}  Transaction Amount",
                            color_discrete_sequence= px.colors.sequential.Bluered, height=650, width=600)

    st.plotly_chart(fig_amount)

    fig_count = px.bar(top_trans_Q_Group, x="Dist_name", y="Trans_count", title=f"Q{quarter}  Transaction Count",
                            color_discrete_sequence= px.colors.sequential. Agsunset,height=650, width=600)
    st.plotly_chart(fig_count)

    return top_trans_Q

def top_trans_S_G(df,state):
    top_trans_S = df[df["State"]== state]
    top_trans_S.reset_index(inplace=True)

    # top_trans_S _Group:

    top_trans_S_Group = top_trans_S.groupby("Dist_name")[["Trans_count","Trans_amount"]].sum()
    top_trans_S_Group.reset_index(inplace=True)

    #Plotting details:
    
    fig_amount = px.bar(top_trans_S_Group, x="Dist_name", y="Trans_amount", title=f" Q{quarter}  Transaction Amount",
                            color_discrete_sequence= px.colors.sequential.Bluered, height=650, width=600)

    st.plotly_chart(fig_amount)

    fig_count = px.bar(top_trans_S_Group, x="Dist_name", y="Trans_count", title=f"Q{quarter}  Transaction Count",
                            color_discrete_sequence= px.colors.sequential. Agsunset,height=650, width=600)
    st.plotly_chart(fig_count)


def top_user_1(df,year):
    top_user_y= df[df["years"] == year]
    top_user_y.reset_index(drop= True, inplace= True)

    top_user_y_g= pd.DataFrame(top_user_y.groupby(["states","quarter"])["Reg_Users"].sum())
    top_user_y_g.reset_index(inplace= True)

    fig_top_1= px.bar(top_user_y_g, x= "states", y= "Reg_Users", barmode= "group", color= "quarter",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_1)

    return top_user_y

def top_user_2(df,quarter):
    top_user_q= df[df["quarter"] == quarter]
    top_user_q.reset_index(drop= True, inplace= True)

    top_user_q_g= pd.DataFrame(top_user_q.groupby(["states","quarter"])["Reg_Users"].sum())
    top_user_q_g.reset_index(inplace= True)

    fig_top_1= px.bar(top_user_q_g, x= "states", y="Reg_Users" , barmode= "group", color= "Reg_Users",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Bluered)
    st.plotly_chart(fig_top_1)

    return top_user_q

def top_user_3(df,state):
    top_user_y_s= df[df["states"] == state]
    top_user_y_s.reset_index(drop= True, inplace= True)

    top_user_y_s_g= pd.DataFrame(top_user_y_s.groupby("quarter")["Reg_Users"].sum())
    top_user_y_s_g.reset_index(inplace= True)

    fig_top_1= px.bar(top_user_y_s, x= "quarter", y= "Reg_Users",barmode= "group",
                           width=1000, height= 800,color= "Reg_Users",hover_data="Pincode",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_1)


def question_1():
    brand= Aggregated_users [["Brand","Trans_count"]]
    brand1= brand.groupby("Brand")["Trans_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Trans_count", names= "Brand", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def question_2():
    low_trans_c= Aggregated_transaction[["states", "Trans_amount"]]
    low_trans_c_1= low_trans_c.groupby("states")["Trans_amount"].sum().sort_values(ascending= True)
    low_trans_c_2= pd.DataFrame(low_trans_c_1).reset_index().head(10)

    fig_low_trans_cs= px.bar(low_trans_c_2, x= "states", y= "Trans_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_low_trans_cs)

def question_3():
    high_trans_dist= map_transaction[["Dist_name", "Trans_amount"]]
    high_trans_dist_1= high_trans_dist.groupby("Dist_name")["Trans_amount"].sum().sort_values(ascending=False)
    high_trans_dist_2= pd.DataFrame(high_trans_dist_1).head(10).reset_index()

    fig_high_trans_dist= px.pie(high_trans_dist_2, values= "Trans_amount", names= "Dist_name", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_high_trans_dist)

def question_4():
    high_trans_dist= map_transaction[["Dist_name", "Trans_amount"]]
    high_trans_dist_1= high_trans_dist.groupby("Dist_name")["Trans_amount"].sum().sort_values(ascending=True)
    high_trans_dist_2= pd.DataFrame(high_trans_dist_1).head(10).reset_index()

    fig_high_trans_dist= px.pie(high_trans_dist_2, values= "Trans_amount", names= "Dist_name", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_high_trans_dist)


def question_5():
    states_app= map_users[["states", "App_opened"]]
    states_app_1= states_app.groupby("states")["App_opened"].sum().sort_values(ascending=False)
    states_app_2= pd.DataFrame(states_app_1).reset_index().head(10)

    fig_states_app= px.bar(states_app_2, x= "states", y= "App_opened", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_states_app)

def question_6():
    states_app= map_users[["states", "App_opened"]]
    states_app_1= states_app.groupby("states")["App_opened"].sum().sort_values(ascending=True)
    states_app_2= pd.DataFrame(states_app_1).reset_index().head(10)

    fig_states_app= px.bar(states_app_2, x= "states", y= "App_opened", title="lowest 10 States With App_Opened",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_states_app)

def question_7():
    state_trans_c= Aggregated_transaction[["states", "Trans_count"]]
    state_trans_c_1= state_trans_c.groupby("states")["Trans_count"].sum().sort_values(ascending=True)
    state_trans_c_2= pd.DataFrame(state_trans_c_1).reset_index()

    fig_state_trans_c= px.bar(state_trans_c_2, x= "states", y= "Trans_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_state_trans_c)

def question_8():
    state_trans_c= Aggregated_transaction[["states", "Trans_count"]]
    state_trans_c_1= state_trans_c.groupby("states")["Trans_count"].sum().sort_values(ascending=False)
    state_trans_c_2= pd.DataFrame(state_trans_c_1).reset_index()

    fig_state_trans_c= px.bar(state_trans_c_2, x= "states", y= "Trans_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_state_trans_c)

def question_9():
    high_trans= Aggregated_transaction[["states", "Trans_amount"]]
    high_trans_1= high_trans.groupby("states")["Trans_amount"].sum().sort_values(ascending= False)
    high_trans_2= pd.DataFrame(high_trans_1).reset_index().head(10)

    fig_high_trans= px.bar(high_trans_2, x= "states", y= "Trans_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_high_trans)

def question_10():
    dist_trans= map_transaction[["Dist_name", "Trans_amount"]]
    dist_trans_1= dist_trans.groupby("Dist_name")["Trans_amount"].sum().sort_values(ascending=True)
    dist_trans_2= pd.DataFrame(dist_trans_1).reset_index().head(50)

    fig_dist_trans= px.bar(dist_trans_2, x= "Dist_name", y= "Trans_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dist_trans)
   
#streamlit part:
st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")  # set title

with st.sidebar:
    select = option_menu("Main_menu",["Home","Data Exploration","Top Charts"]) # set the side bar

if select=="Home":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("BEST MONEY TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("LINK DEBIT & CREDIT CARD WITH ONE TAP")
        st.write("EASY Balance check")
        st.write("UPI Authorization")
        st.download_button("DOWNLOAD", "https://www.phonepe.com/app-download/")

elif select=="Data Exploration":
    tab1,tab2,tab3 = st.tabs(["Aggregated Data","Map Data","Top Data"]) #tabs like chrome tabs

    with tab1: 
        method= st.radio("select method",["Aggre-Transaction Data","Aggre-User Data"]) # radio button is for 'select'ing the method

        if method =="Aggre-Transaction Data":

            col1,col2=st.columns(2)

            with col1:
            
                years=st.slider("select year", Aggregated_transaction["years"].min(),Aggregated_transaction["years"].max(),
                                Aggregated_transaction["years"].min())

            Vary_1= Trans_countamount_Y_G(Aggregated_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                quarter=st.slider("select quarter", Vary_1["quarter"].min(),Vary_1["quarter"].max(),
                                Vary_1["quarter"].min())

            Trans_countamount_Y_Q(Vary_1,quarter)

        elif method == "Aggre-User Data":
            col1,col2=st.columns(2)
            with col1:
                aggre_user_year= st.selectbox("Select the Year",Aggregated_users["years"].unique())
            agg_user_Y= AguS_Y_B(Aggregated_users,aggre_user_year)

            col1,col2=st.columns(2)
            with col1:
                aggre_user_quarter= st.selectbox("Select the Quarter",agg_user_Y["quarter"].unique())
            agg_user_Y_Q= AguS_Q_B(agg_user_Y,aggre_user_quarter)

            col1,col2=st.columns(2)
            with col1:
                aggre_user_state= st.selectbox("Select the State",agg_user_Y["states"].unique())
            Aggre_user_S(agg_user_Y_Q,aggre_user_state)

    with tab2:
        method_1= st.radio("select method",["Map Transaction Data","Map User Data"])

        if method_1 =="Map Transaction Data":
            
            col1,col2= st.columns(2)
            with col1:
                map_years= st.slider("Select the Year - MAP T", map_transaction["years"].min(), map_transaction["years"].max(),map_transaction["years"].min())

            df_map_tran_Y= map_trans_Y_G(map_transaction, map_years)
            
            col1,col2= st.columns(2)
            with col1:
                map_quarter= st.slider("Select the Quarter- MAP T", df_map_tran_Y["quarter"].min(), df_map_tran_Y["quarter"].max(),df_map_tran_Y["quarter"].min())

            df_map_tran_Y_Q= map_trans_Q_G(df_map_tran_Y, map_quarter)

        elif method_1 == "Map User Data":

            col1,col2= st.columns(2)
            with col1:
                map_year= st.selectbox("Select the Year for MAP_USER",map_users["years"].unique())

            map_user_Y= map_user_1(map_users, map_year)

            col1,col2= st.columns(2)
            with col1:
                map_quarter= st.selectbox("Select the Quarter for MAP_USER",map_user_Y["quarter"].unique())

            map_user_Y_Q= map_user_2(map_user_Y,map_quarter)

            col1,col2= st.columns(2)
            with col1:
                map_state= st.selectbox("Select the State for MAP_USER",map_user_Y_Q["states"].unique())

            map_user_3(map_user_Y_Q, map_state)

    with tab3:
        method_2= st.radio("select method",["Top Transaction Data","Top User Data"])

        if method_2 =="Top Transaction Data":
            col1,col2= st.columns(2)
            with col1:
                top_years= st.slider("Select the Year for TOP T", top_transaction["Year"].min(), top_transaction["Year"].max(),
                                        top_transaction["Year"].min())
 
            df_top_tran_Y= top_trans_Y_G(top_transaction,top_years)

            
            col1,col2= st.columns(2)
            with col1:
                top_quarter= st.slider("Select the Quarter for TOP T", df_top_tran_Y["quarter"].min(), df_top_tran_Y["quarter"].max(),
                                        df_top_tran_Y["quarter"].min())

            df_top_tran_Y_Q= top_trans_Q_G(df_top_tran_Y, top_quarter)

        elif method_2 == "Top User Data":

            col1,col2= st.columns(2)
            with col1:
                top_years= st.selectbox("Select the Year for TOP USER", top_users["years"].unique())

            df_top_user_Y= top_user_1(top_users,top_years)

            col1,col2= st.columns(2)
            with col1:
                top_quarter= st.selectbox("Select the Quarter for TOP USER", top_users["quarter"].unique())

            df_top_user_Q= top_user_2(df_top_user_Y,top_quarter)

            col1,col2= st.columns(2)
            with col1:
                top_state= st.selectbox("Select the State for TOP USER", df_top_user_Q["states"].unique())

            df_top_user_Y_S= top_user_3(df_top_user_Q,top_state)



elif select=="Top Charts":
    question= st.selectbox("Select the Question", ('1. Top Brands Of Mobiles Used',
                                                    '2. States With Lowest Transaction Amount',
                                                    '3. Districts With Highest Transaction Amount',
                                                    '4. Top 10 Districts With Lowest Transaction Amount',
                                                    '5. Top 10 States With App_Opened',
                                                    '6. Least 10 States With App_Opened',
                                                    '7. States With Lowest Transaction Count',
                                                    '8. States With Highest Transaction Count',
                                                    '9. States With Highest Transaction Amount',
                                                    '10. Top 50 Districts With Lowest Transaction Amount'))
    
    if question== "1. Top Brands Of Mobiles Used":
       question_1()

    elif question=="2. States With Lowest Transaction Amount":
        question_2()

    elif question=="3. Districts With Highest Transaction Amount":
        question_3()

    elif question=="4. Top 10 Districts With Lowest Transaction Amount":
        question_4()

    elif question=="5. Top 10 States With App_Opened":
        question_5()

    elif question=="6. Least 10 States With App_Opened":
        question_6()

    elif question=="7. States With Lowest Transaction Count":
        question_7()

    elif question=="8. States With Highest Transaction Count":
        question_8()

    elif question=="9. States With Highest Transaction Amount":
        question_9()

    elif question=="10. Top 50 Districts With Lowest Transaction Amount":
        question_10()
