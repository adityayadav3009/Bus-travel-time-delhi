import streamlit as st
import numpy as np
from tensorflow import keras
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
df = pd.read_csv("TRAIN_DATA.csv")
dict = np.load('file.npy', allow_pickle='TRUE').item()
dist = np.load('dist.npy', allow_pickle='TRUE').item()
st.title("Bus travel time")
start_stop = st.selectbox("Starting point", list(dict.keys()))
lst = dict[start_stop]
end_stop = st.selectbox(
    "Destination", [str(x[0])+"  , by route "+str(x[1]) for x in dict[start_stop]])

route_id = 0
num_stops = 0
for x in dict[start_stop]:
    if str(x[0])+"  , by route "+str(x[1]) == end_stop:
        route_id = x[1]
        num_stops = x[2]
        break

st.write("Route_id : {}".format(route_id))
st.write("Number of stops in route : {}".format(num_stops))
try:
    st.write("Distance travelled : {} km".format(round(dist[route_id], 2)))
    input_test = [num_stops, dist[route_id]]
    weekdays = ["Monday", "tuesday", "wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]
    day = st.selectbox("Day of travel", weekdays)
    for d in weekdays:
        if d == day:
            input_test.append(1)
        else:
            input_test.append(0)
    months = ["April", "May", "June", "July", "August"]
    month = st.selectbox("Month of travel", months)
    for m in months:
        if m == month:
            input_test.append(1)
        else:
            input_test.append(0)
    d_c = ["Afternoon", "Early morning", "Evening", "Morning", "Night"]
    departure_time = st.selectbox("Departing time", d_c)
    for d_t in d_c:
        if d_t == departure_time:
            input_test.append(1)
        else:
            input_test.append(0)
    # st.write(input_test)
    input_test = np.array(input_test).reshape(1, 19)
    model = keras.models.load_model("my_model.h5")
    model.compile(loss='mean_absolute_error', optimizer='adam')
    time = 0
    with st.spinner('Estimating time'):
        time = model.predict(input_test)[0][0]
        st.write("**TIME ESTIMATED : {}**".format(round(time), 2), " minutes")
    with st.spinner('Plotting graph'):
        fig, ax = plt.subplots(1, 1)
        sns.kdeplot(df[df["route_id"] == route_id]["travel_time"], ax=ax)
        ax.axvline(df[df["route_id"] == route_id]["travel_time"].mean(
        ), color="yellow", label="average time taken")
        ax.axvline(time, color="r")
        ax.legend()
        st.pyplot(fig=fig)
except:
    st.warning("Sorry data not available for this route")
