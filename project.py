import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

st.header(" COURIER SERVICE MANGEMENT SYSTEM")



@st.cache_resource
def get_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


@st.cache_resource
def query_db(sql: str):
    # print(f"Running query_db(): {sql}")

    db_info = get_config()

    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()
    print(data)

    column_names = [desc[0] for desc in cur.description]

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df


"#"
"### GET ALL ORDERS BY CUSTOMER NAME"

sql_customer_names = "SELECT c_name FROM customer;"
try:
    customer_names = query_db(sql_customer_names)["c_name"].tolist()
    customer_name = st.selectbox("Choose a Customer:-", customer_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

try:
    sql_q=f"""Select O.Order_ID as order_id,O.Product as product,O.Weight as weight,C.C_name as customer_name
        From CSM_Order O, Customer C
        Where (C.SSN=O.Sender_SSN
        Or C.SSN=O.Reciver_SSN)
        and C.C_Name='{customer_name}'
        group by C.C_Name,O.Order_ID
        order by O.Product;
        """
    st.dataframe(query_db(sql_q))
except:
    st.write(
            "Sorry! Something went wrong with your query, please try again."
    )


"### FEEDBACKS FOR ORDER"

sql_orderids = "SELECT order_id FROM Feedback;"
try:
    orderids = query_db(sql_orderids)["order_id"].tolist()
    orderid = st.selectbox("Choose a Order ID:-", orderids)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

try:
    sql_q=f"""Select O.Order_ID as order_id,O.Product as product,F.Description as feedback, F.Rating as rating, CS.C_Name as customer_name
From CSM_Order O, Feedback F,Feedback_Customer C,Customer CS
Where O.Order_ID=F.Order_ID
and F.Order_ID='{orderid}'
and F.Feedback_ID=C.Feedback_ID
and C.SSN=CS.SSN
order by O.Product;"""
    st.dataframe(query_db(sql_q))
except:
    st.write(
            "Sorry! Something went wrong with your query, please try again."
    )

"### AVAIBILITY OF VEHICLES BY ZIPCODES"

sql_szs = "SELECT source_zipcode FROM Vehicle;"
try:
    szs = query_db(sql_szs)["source_zipcode"].tolist()
    sz = st.selectbox("Choose a Source Zipcode:-",szs)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

sql_dzs = "SELECT destination_zipcode FROM Vehicle;"
try:
    dzs = query_db(sql_dzs)["destination_zipcode"].tolist()
    dz= st.selectbox("Choose a Destination Zipcode:-", dzs)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

try:
    sql_q=f"""Select V.Vehicle_ID as vehicle_id
From Vehicle V,CSM_Order O
Where V.Source_Zipcode='{sz}'
and V.Destination_Zipcode='{dz}'
and V.Source_Zipcode=O.Source_Zipcode
and V.Destination_Zipcode=O.Destination_Zipcode
and O.Weight<=V.Capacity
order by V.Vehicle_ID;"""
    st.dataframe(query_db(sql_q))
except:
    st.write(
            "Sorry! Something went wrong with your query, please try again."
    )

"### AVAIBILITY OF VEHICLES BY CARRIER"

sql_cns = "SELECT carrier_name FROM Carrier;"
try:
    cns= query_db(sql_cns)["carrier_name"].tolist()
    cn = st.selectbox("Choose a Carrier Name:-", cns)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

try:
    sql_count=f"""Select COUNT(V.Vehicle_ID)
    From Carrier C,Vehicle V
    Where C.Carrier_Name='{cn}'
    and C.Carrier_Code=V.Carrier_Code
    group by C.Carrier_Name
    Order by C.Carrier_Name;"""

    count=query_db(sql_count)
    st.write(
                f"Total Number of Vehicles by {cn} Carrier is {count}")

    sql_q=f"""Select C.Carrier_Name as carrier_name,V.Vehicle_ID as vehicle_id
    From Carrier C,Vehicle V
    Where C.Carrier_Name='{cn}'
    and C.Carrier_Code=V.Carrier_Code
    Order by C.Carrier_Name;"""
    st.dataframe(query_db(sql_q))
except:
    st.write(
            "Sorry! Something went wrong with your query, please try again."
)


"### SHIPPED ORDER DETAILS BY DATE & TIME"

sql_dts = "select delivery_date_time from transport;"
try:
    dts= query_db(sql_dts)["delivery_date_time"].tolist()
    dt = st.selectbox("Choose date & time:-", dts)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

try:
    sql_q=f"""Select O.Order_ID as order_id,O.Product as product,V.Vehicle_ID as vehicle_id,C.Carrier_Name as carrier_name
    From CSM_Order O,Vehicle V, Carrier C,Transport T,Shipping S
    Where T.Delivery_Date_Time='{dt}'
    and T.Transport_ID=S.Transport_ID
    and S.Vehicle_ID=V.Vehicle_ID
    and S.Order_ID=O.Order_ID
    and V.Vehicle_ID=S.Vehicle_ID
    and V.Carrier_CODE=C.Carrier_CODE
    order by O.Product;"""
    st.dataframe(query_db(sql_q))
except:
    st.write(
            "Sorry! Something went wrong with your query, please try again."
)

"### AVERAGE RATING OF CARRIERS"

try:
    sql_q=f"""Select C.Carrier_Name as carrier_name, round(avg(F.rating),0) as average_rating
    From CSM_Order O, Carrier C,Shipping S,Vehicle V,Feedback F
    Where F.Order_ID=O.Order_ID
    and O.Order_ID=S.Order_ID
    and S.Vehicle_ID=V.Vehicle_ID
    and V.Carrier_CODE=C.Carrier_CODE
    Group by C.Carrier_Name
    Order by C.Carrier_Name;"""
    st.table(query_db(sql_q))
except:
    st.write(
            "Sorry! Something went wrong with your query, please try again."
)
