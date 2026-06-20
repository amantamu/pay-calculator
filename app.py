import streamlit as st
import calendar
from datetime import date, timedelta
from pay import weekly_breakdown, monthly_totals

st.title("My Streamlit App")

year = st.number_input("Year", min_value=2026, max_value=2030, value=2026)
month = st.number_input("Month", min_value=1, max_value=12, value=6)

num_days = calendar.monthrange(int(year), int(month))[1]

worked = []
for day in range(1, num_days + 1):
    d = date(int(year), int(month), day)
    label = d.strftime("%a %d/%m")
    if st.checkbox(label, key=str(d)):
        worked.append(d)

if worked:
    st.header("Your Pay")

    for friday, pay in weekly_breakdown(worked).items():
        st.subheader(f"Pay day: {friday.strftime('%d/%m/%Y')}")
        st.write(f"Gross : £{pay['gross']:.2f}")
        st.write(f"Tax : £{pay['tax']:.2f}")
        st.write(f"NI : £{pay['ni']:.2f}")
        st.write(f"Net : £{pay['net']:.2f}")

    st.header("Monthly totals")
    st.caption(f"Pay received in {calendar.month_name[int(month)]} {year}")
    totals = monthly_totals(worked, int(year), int(month))
    st.write(f"Gross : £{totals['gross']:.2f}")
    st.write(f"Tax : £{totals['tax']:.2f}")
    st.write(f"NI : £{totals['ni']:.2f}")
    st.write(f"Net : £{totals['net']:.2f}")
