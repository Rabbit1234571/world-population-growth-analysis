import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="World Population Dashboard", page_icon="🌍", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("world pop.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()
year_columns = ["1970 Population", "1980 Population", "1990 Population", "2000 Population", "2010 Population", "2015 Population", "2020 Population", "2022 Population"]
years = [int(c.split()[0]) for c in year_columns]

st.title("🌍 World Population Growth Analysis")
st.markdown("Explore population patterns by continent, country, and year. Use the sidebar filters to update **all charts and KPIs together**.")

# Global filters: every chart below uses filtered_df and selected_year.
st.sidebar.header("Dashboard Filters")
continents = sorted(df["Continent"].dropna().unique().tolist())
selected_continents = st.sidebar.multiselect("Select continent(s)", continents, default=continents)
selected_year = st.sidebar.selectbox("Population year", years, index=years.index(2022))
top_n = st.sidebar.slider("Number of top countries", min_value=5, max_value=30, value=10, step=5)
min_population = int(df[year_columns[-1]].min())
max_population = int(df[year_columns[-1]].max())
pop_range = st.sidebar.slider("2022 population range", min_value=min_population, max_value=max_population, value=(min_population, max_population), step=1000000)
search_country = st.sidebar.text_input("Search country (optional)").strip().lower()

selected_pop_col = f"{selected_year} Population"
filtered_df = df[df["Continent"].isin(selected_continents)].copy()
filtered_df = filtered_df[filtered_df["2022 Population"].between(pop_range[0], pop_range[1])]
if search_country:
    filtered_df = filtered_df[filtered_df["Country/Territory"].str.lower().str.contains(search_country, na=False)]

if filtered_df.empty:
    st.warning("No countries match these filters. Please change the sidebar selections.")
    st.stop()

# KPIs
world_population = int(filtered_df[selected_pop_col].sum())
country_count = len(filtered_df)
avg_growth = filtered_df["Growth Rate"].mean()
avg_density = filtered_df["Density (per km²)"].mean()
k1, k2, k3, k4 = st.columns(4)
k1.metric(f"Population ({selected_year})", f"{world_population:,}")
k2.metric("Countries / territories", f"{country_count:,}")
k3.metric("Average growth rate", f"{avg_growth:.3f}")
k4.metric("Average density / km²", f"{avg_density:,.1f}")

st.divider()

# Chart 1: population by continent for the selected year
continent_pop = filtered_df.groupby("Continent", as_index=False)[selected_pop_col].sum().sort_values(selected_pop_col, ascending=False)
fig1 = px.bar(continent_pop, x="Continent", y=selected_pop_col, color="Continent", title=f"Population by Continent ({selected_year})", labels={selected_pop_col: "Population"})
fig1.update_layout(showlegend=False, yaxis_tickformat=",d")

# Chart 2: top countries in the selected year
top_countries = filtered_df.nlargest(top_n, selected_pop_col).sort_values(selected_pop_col, ascending=True)
fig2 = px.bar(top_countries, x=selected_pop_col, y="Country/Territory", orientation="h", color="Continent", title=f"Top {min(top_n, len(top_countries))} Countries by Population ({selected_year})", labels={selected_pop_col: "Population", "Country/Territory": "Country"})
fig2.update_layout(xaxis_tickformat=",d")

c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(fig1, use_container_width=True)
with c2:
    st.plotly_chart(fig2, use_container_width=True)

# Chart 3: historical trend, all filtered countries aggregated by year
trend_data = []
for year, col in zip(years, year_columns):
    trend_data.append({"Year": year, "Population": int(filtered_df[col].sum())})
trend_df = pd.DataFrame(trend_data)
fig3 = px.line(trend_df, x="Year", y="Population", markers=True, title="Population Growth Over Time (filtered countries)")
fig3.update_layout(yaxis_tickformat=",d")

# Chart 4: density vs population scatter
fig4 = px.scatter(filtered_df, x="Density (per km²)", y=selected_pop_col, color="Continent", size="World Population Percentage", hover_name="Country/Territory", title=f"Population vs Density ({selected_year})", labels={selected_pop_col: "Population", "Density (per km²)": "Density per km²"})
fig4.update_layout(yaxis_tickformat=",d")

c3, c4 = st.columns(2)
with c3:
    st.plotly_chart(fig3, use_container_width=True)
with c4:
    st.plotly_chart(fig4, use_container_width=True)

# Chart 5: growth rate by country
rate_data = filtered_df.nlargest(top_n, "Growth Rate").sort_values("Growth Rate", ascending=True)
fig5 = px.bar(rate_data, x="Growth Rate", y="Country/Territory", orientation="h", color="Continent", title=f"Top {min(top_n, len(rate_data))} Growth Rates", labels={"Growth Rate": "Growth rate", "Country/Territory": "Country"})
st.plotly_chart(fig5, use_container_width=True)

with st.expander("View filtered dataset"):
    st.dataframe(filtered_df, use_container_width=True)
    st.download_button("Download filtered data as CSV", filtered_df.to_csv(index=False).encode("utf-8"), file_name="filtered_world_population.csv", mime="text/csv")

st.caption("Data source: the CSV file included with this project. Population totals shown are for the countries currently selected in the sidebar, not necessarily the entire world.")
