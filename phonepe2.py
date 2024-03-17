import json
import pandas as pd
import psycopg2
import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu


mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      password="Nuttertool@12",
                      database="phonepe_data",
                      port="5432"
                      )
cursor=mydb.cursor()



#Streamlit Part
st.title(':red[PhonePe Pulse]')
SELECT = option_menu(
    menu_title=None,
    options= ["Home","Top Charts","Data Exploration"],
    icons=["House","none","bar-chart"],
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white","size":"cover", "width": "100"},
        "icon": {"color": "black", "font-size": "20px"},
            
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#BDE6BA"},
        "nav-link-selected": {"background-color": "#BDE6BA"}})




#Top Charts

if SELECT == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    option1=st.selectbox('select type',('Transaction','User','Insurance'))
    option2=st.slider("**Year**", min_value=2018, max_value=2023)
    option3=st.slider("Quarter", min_value=1, max_value=4)
    st.write('You have selected:',option2,"-","Q",option3,"-",option1)

    #Top in Transactions

    if option1 == 'Transaction':
         # Top 10 States by Transaction Amount
        
        st.markdown("### :red[State]")
        cursor.execute(f"select states, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) as Total_Transaction_Amount from aggregated_transaction  where years = {option2} and quarter = {option3} group by states order by Total_Transaction_Amount DESC limit 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
        fig = px.pie(df, values='Total_Amount',
                            names='State',
                            title='Top 10 States by Transaction Amount',
                            color_discrete_sequence=px.colors.sequential.Mint,
                            hover_data=['Transactions_Count'],
                            labels={'Transactions_Count':'Transactions_Count'})
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)



#Top 10 districts with highest transaction 
        

        st.markdown("### :violet[Districts]")
        if option2 == 2023 and option3 in [4]:
             st.markdown("#### Sorry No Data to Display for 2023 Quarter 4")
        cursor.execute(f"select District_name , sum(total_count) as Total_Transaction_Count, sum(total_amount) as Total_Transaction_Amount from map_transaction where years = {option2} and quarter = {option3} group by District_name order by Total_Transaction_Amount desc limit 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['District_name', 'Transaction_count','Transaction_amount'])
        fig = px.bar(df,x='District_name', y='Transaction_amount',color='District_name',
                     title='Top 10 Districts by Transaction Amount',
            labels={'Transaction_amount': 'Transaction Amount'},
            color_discrete_sequence=px.colors.sequential.Mint)
        
        st.plotly_chart(fig, use_container_width=True)

 # top pincodes with highest transaction

        st.markdown("### :violet[Pincodes]")
        cursor.execute(f"select pincodes, sum(total_count) as Total_Transaction_count,sum(total_amount) as Total_Transaction_Amount from top_transaction where years = {option2} and quarter = {option3} group by pincodes order by Total_Transaction_Amount DESC limit 10")
        df=pd.DataFrame(cursor.fetchall(),columns=['District_code','Transaction_Count','Transaction_Amount'])
        fig = go.Figure(data=[go.Table(
                            header=dict(values=["District_code","Total_Transaction_count","Total_Transaction_Amount"],align=['center'],line_color='darkslategray',
                                        fill=dict(color=['paleturquoise', 'white']),
                                        font_size=12,
                                        height=30),
                            cells=dict(values=[df.District_code, df.Transaction_Count, df.Transaction_Amount],align=["center"],line_color='darkslategray',
                                        fill=dict(color=['paleturquoise', 'white']),
                                        font_size=12,
                                        height=30))
                                        ])
        fig.update_layout(
        title="Top pincodes with highest transaction")
        st.plotly_chart(fig,use_container_width=True)

 #Top  in User
        
    if option1 == 'User':
        
    #Top 10 Brands
        
        st.markdown("### :violet[Brands]")
        cursor.execute(f"select Device_brand, sum(device_count) as Total_Users from aggregated_user where years = {option2} and quarter = {option3} group by Device_brand order by Total_Users DESC limit 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['Device_Name', 'No_Of_Users'])
        fig = px.bar(df,
                        title='Top 10 Brands',
                        x="Device_Name",
                        y="No_Of_Users",
                        color='Device_Name',
                        color_discrete_sequence=px.colors.sequential.Mint)
        st.plotly_chart(fig,use_container_width=True)


# Top 10 Districts with app opened
        
        st.markdown("### :violet[District]")
        cursor.execute(f"select district_name, sum(registeredusers) as Total_Users, sum(appopens) as Total_App_opens from map_user where years = {option2} and quarter = {option3} group by District_Name order by Total_Users desc limit 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['District_Name', 'Total_Users','Total_App_opens'])
        fig= px.pie(df, values='Total_Users',
                        names='District_Name',
                        title='Top 10 Districts with No of Users',
                        color_discrete_sequence=px.colors.sequential.Mint,
                        labels={'Total_Users':'Total_Users'}
                        )
        st.plotly_chart(fig,use_container_width=True)


# Top 10 States with app opened
        st.markdown("### :violet[State]")
        cursor.execute(f"select states, sum(appopens) as Total_App_opens from map_user where years = {option2} and quarter = {option3} group by states order by Total_App_opens DESC limit 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Total_App_opens'])
        fig = px.pie(df, values='Total_App_opens',
                            names='States',
                            title='Top 10 States with app opened',
                            color_discrete_sequence=px.colors.sequential.Mint,
                            hover_data=['Total_App_opens'],
                            labels={'Total_App_opens':'Total_App_opens'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True) 
        

#Top 10 in Insurance
            
    if option1 == 'Insurance':
            
            # Top 10 States with highest Insurance count 

            st.markdown("### :violet[State]")
            cursor.execute(f"select States, sum(transaction_count) as Total_insurance_count from aggregated_insurance group by States order by Total_insurance_count DESC limit 10")
            df=pd.DataFrame(cursor.fetchall(),columns=["States","Total_insurance_count"])
            fig = px.bar(df,title='Top 10 States with highest Insurance count ',
                                x="States",
                                y="Total_insurance_count",
                                color='States',
                                color_discrete_sequence=px.colors.sequential.Mint)
            st.plotly_chart(fig,use_container_width=True)

            
            #Top 10 Districts with highest Insurance amount 

            st.markdown("### :violet[Disttricts]")
            cursor.execute(f"select District_name , sum(total_amount) as Total_Insurance_Amount from map_insurance group by District_name order by Total_Insurance_Amount DESC limit 10")
            df=pd.DataFrame(cursor.fetchall(),columns=["District_name","Total_Insurance_Amount"])
            fig = px.bar(df,title='Top 10 Districts with highest Insurance amount ',
                                x="District_name",
                                y="Total_Insurance_Amount",
                                color='District_name',
                                color_discrete_sequence=px.colors.sequential.Mint)
            st.plotly_chart(fig,use_container_width=True)



#-------------------------------------------Data Exploration ------------------------------------------------------------
            
if SELECT == "Data Exploration":
    st.markdown("## :violet[Data Exploration]")
    option1=st.selectbox('select type',('Transaction','User'))
    option2 = st.slider("**Year**", min_value=2018, max_value=2023)
    option3 = st.slider("Quarter", min_value=1, max_value=4)
    st.write('You have selected:',option2,"-","Q",option3,"-",option1)


    if option1 == 'Transaction':
         
         # Map Data on Total Transaction Amount

        st.markdown("### :violet[State wise Data of Total Transaction Amount]")
        cursor.execute(f"select States, sum(total_count) as Total_Transactions_count, sum(total_amount) as Total_Transaction_amount from map_transaction where years={option2} and quarter = {option3} group by States order by States")
        df1=pd.DataFrame(cursor.fetchall(),columns=["States","Total_Transactions_count","Total_Transaction_amount"])
        df2 = pd.read_csv(r"C:\Users\vigne\Desktop\project 2\Statenames.csv")
        df1.States = df2
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='States',
                      color='Total_Transaction_amount',
                      color_continuous_scale='Viridis'
                      )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_geos(fitbounds="locations", visible=True)
        st.plotly_chart(fig,use_container_width=True)


        #Map Data on Total Transaction Count 

        st.markdown("### :violet[State wise Data of Total Transaction Count]")
        cursor.execute(f"select States, sum(total_count) as Total_Transactions_count, sum(total_amount) as Total_Transaction_amount from map_transaction where years={option2} and quarter = {option3} group by States order by States")
        df1=pd.DataFrame(cursor.fetchall(),columns=["States","Total_Transactions_count","Total_Transaction_amount"])
        df2 = pd.read_csv(r"C:\Users\vigne\Desktop\project 2\Statenames.csv")
        df1.States = df2
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='States',
                      color='Total_Transactions_count',
                      title="State wise Total Transaction Amount",
                      color_continuous_scale='Viridis'
                      )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_geos(fitbounds="locations", visible=True)
        st.plotly_chart(fig,use_container_width=True)

       
       
       #Data on Payment Type
        

        st.markdown("# ")
        st.markdown("### :violet[Payment Type]")
        cursor.execute(f"select Transaction_type, sum(Transaction_amount) as Total_Transaction_Amount, sum(Transaction_count) as Total_Transaction_count from aggregated_transaction where years={option2} and quarter = {option3} group by Transaction_type")
        df=pd.DataFrame(cursor.fetchall(),columns=["Transaction_type","Total_Transaction_Amount","Total_Transaction_count"])
        fig = px.bar(df,x="Transaction_type",
                        y="Total_Transaction_count",
                        color='Total_Transaction_Amount',
                        color_discrete_sequence=px.colors.sequential.Mint)
        st.plotly_chart(fig,use_container_width=True)



        #State wise Data on Transaction

        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        st.write("#### :violet[District wise Data]")
        cursor.execute(f"select states, district_name,years,quarter, sum(total_count) as Total_Transaction_Count, sum(total_amount) as Total_Transaction_amount from map_transaction where Years={option2} and Quarter = {option3} and States = '{selected_state}' group by States, District_name,Years,Quarter order by States,District_name")
        
        df1 = pd.DataFrame(cursor.fetchall(), columns=['States','District_name','Years','Quarter',
                                                         'Total_Transaction_Count','Total_Transaction_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District_name",
                     y="Total_Transaction_Count",
                     orientation='v',
                     color='Total_Transaction_amount',
                     color_continuous_scale=px.colors.sequential.Mint)
        st.plotly_chart(fig,use_container_width=True)


    if option1 == 'User':
        

        # Overall State Data - TOTAL APPOPENS - INDIA MAP

        st.markdown("## :violet[State Data - User App opening frequency]")
        cursor.execute(f"select States,sum(registeredUsers) as Total_Registered_Users,sum(appopens) as Total_App_Open_Count from map_user where Years={option2} and Quarter = {option3} group by States order by States")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['States', 'Total_Registered_Users','Total_App_Open_Count'])
        df2 = pd.read_csv(r"C:\Users\vigne\Desktop\project 2\Statenames.csv")
        df1.Total_App_Open_Count = df1.Total_App_Open_Count.astype(float)
        df1.States = df2
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='States',
                color='Total_App_Open_Count',
                color_continuous_scale='Viridis'
                )
        fig.update_layout(margin={"r":0.5,"t":0,"l":0.5,"b":0})
        fig.update_geos(fitbounds="locations", visible=True)
        st.plotly_chart(fig,use_container_width=True)



         # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        
        st.markdown("## :violet[Select any State to explore more on Registered Uses]")
        selected_state= st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        cursor.execute(f"select States,Years,Quarter,District_Name,sum(registeredusers) as Total_Registered_Users, sum(appopens) as Total_Appopens from map_user where Years={option2} and Quarter = {option3} and States = '{selected_state}' group by States, District_Name,Years,Quarter order by States,District_Name")
        
        df = pd.DataFrame(cursor.fetchall(), columns=['States','Years', 'Quarter', 'District_Name', 'Total_Registered_Users','Total_Appopens'])
        df.Total_Registered_Users = df.Total_Registered_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District_Name",
                     y="Total_Registered_Users",
                     orientation='v',
                     color='Total_Registered_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)        
