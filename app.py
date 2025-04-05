# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="COVID Dashboard", layout="wide")

# Load cleaned data
df = pd.read_csv("cleaned_data/cleaned_covid_data.csv")
df['Date'] = pd.to_datetime(df['Date'])

# Sidebar Filters
st.sidebar.header("📅 Filter Options")
selected_date = st.sidebar.date_input("Select Date", value=df['Date'].max())
selected_countries = st.sidebar.multiselect(
    "Select Country", 
    options=df['Country/Region'].unique(), 
    default=["India"]
)

# Filter data
filtered = df[(df['Date'] == pd.to_datetime(selected_date)) & 
              (df['Country/Region'].isin(selected_countries))]

# Section: Title
st.markdown("<h1 style='text-align: center; color: #1f77b4;'>🦠 COVID-19 Dashboard</h1>", unsafe_allow_html=True)
st.markdown(f"**Date Selected:** {selected_date.strftime('%d %B %Y')}")

# Section: BAR CHART
# Section: BAR CHART
st.markdown("### 📊 Bar Graph: Confirmed, Deaths, and Recovered by Country")
if not filtered.empty:
    fig1, ax1 = plt.subplots(figsize=(8, 4), dpi=150, facecolor='none')
    ax1.set_facecolor('none')
    
    sns.barplot(data=filtered, x='Country/Region', y='Confirmed', color='skyblue', label='Confirmed', ax=ax1)
    sns.barplot(data=filtered, x='Country/Region', y='Deaths', color='red', label='Deaths', ax=ax1)
    sns.barplot(data=filtered, x='Country/Region', y='Recovered', color='green', label='Recovered', ax=ax1)
    
    ax1.set_ylabel("Cases")
    ax1.set_title("COVID-19 Cases by Country", color='white')
    ax1.legend()
    
    # Make axis labels white to match dark theme
    ax1.tick_params(colors='white')
    ax1.spines['bottom'].set_color('white')
    ax1.spines['left'].set_color('white')
    ax1.yaxis.label.set_color('white')
    ax1.xaxis.label.set_color('white')
    
    st.pyplot(fig1, clear_figure=True)
else:
    st.warning("No data available for selected date and countries.")

# Section: PIE CHART

st.markdown("### 🧩 Pie Chart of Confirmed Cases")
if not filtered.empty:
    fig2, ax2 = plt.subplots(figsize=(4, 4), dpi=350, facecolor='none')
    ax2.set_facecolor('none')

    labels = filtered['Country/Region']
    values = filtered['Confirmed']
    
    if len(labels) <= 5:
        wedges, texts, autotexts = ax2.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    else:
        wedges, texts, autotexts = ax2.pie(values, labels=None, autopct='%1.1f%%', startangle=90)
        ax2.legend(labels, loc="upper right", fontsize="small")
    
    ax2.axis('equal')
    fig2.tight_layout(pad=0.1)
    
    st.pyplot(fig2, clear_figure=True)


# Section: METRICS
st.markdown("### 📌 Country-wise Summary Stats")
if selected_countries:
    cols = st.columns(len(selected_countries)) if selected_countries else []
    for i, country in enumerate(selected_countries):
        c_data = filtered[filtered['Country/Region'] == country]
        if not c_data.empty:
            with cols[i]:
                st.metric(f"{country} - Confirmed", int(c_data['Confirmed'].values[0]))
                st.metric(f"{country} - Deaths", int(c_data['Deaths'].values[0]))
                st.metric(f"{country} - Recovered", int(c_data['Recovered'].values[0]))
else:
    st.info("Please select at least one country to see summary statistics.")

# Section: TABLE
st.markdown("### 📑 Filtered Data Table")
st.dataframe(filtered)

# Section: Download
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download as CSV", csv, "filtered_covid_data.csv", "text/csv")

# Section: LINE CHART
st.markdown("### 📈 Trend of Confirmed Cases Over Time")
trend_data = df[df['Country/Region'].isin(selected_countries)]
trend_chart = trend_data.pivot_table(index='Date', columns='Country/Region', values='Confirmed', aggfunc='sum')
st.line_chart(trend_chart)
