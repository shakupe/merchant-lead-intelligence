import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

df = pd.read_csv("data.csv")
df.columns = df.columns.str.strip()

# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align: center;'>🚀 Lead Discovery Dashboard</h1>
<p style='text-align: center; color: gray;'>Find high-potential businesses instantly</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------- SEARCH ----------
search = st.text_input("🔍 Search (gym, salon, restaurant...)")

if search:
    filtered = df[
        df["Category"].str.lower().str.contains(search.lower()) |
        df["Business Name"].str.lower().str.contains(search.lower())
    ]

    if len(filtered) > 0:

        # ---------- TOP LEADS ----------
        st.subheader("🔥 Top Opportunities")

        top = filtered.sort_values(by="Score", ascending=False).head(3)

        cols = st.columns(3)

        for i, (_, row) in enumerate(top.iterrows()):
            with cols[i]:
                st.markdown(f"""
                <div style="padding:15px; border-radius:10px; background:#1e1e1e">
                    <h4>{row['Business Name']}</h4>
                    <p>{row['Category']} | {row['Location']}</p>
                    <p>⭐ {row['Rating (out of 5)']}</p>
                    <b style="color:red;">🔥 HIGH OPPORTUNITY</b>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # ---------- INSIGHTS ----------
        st.subheader("📊 Insights")

        high = filtered[filtered["Lead Priority"] == "HIGH"]

        st.write(f"👉 {len(high)} high-potential businesses found")
        st.write(
            f"👉 Focus sector: **{filtered['Category'].value_counts().idxmax()}**")

        st.markdown("---")

        # ---------- OPTIONAL TABLE ----------
        with st.expander("📋 View All Results"):
            st.dataframe(filtered, use_container_width=True)

    else:
        st.warning("No results found")

else:
    st.info("👆 Start by typing a category like 'gym'")
