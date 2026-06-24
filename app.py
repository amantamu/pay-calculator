import streamlit as st
import calendar
from datetime import date
from pay import weekly_breakdown, monthly_totals

# calendar weeks start on Sunday, matching your Sun–Sat pay week
calendar.setfirstweekday(calendar.SUNDAY)

st.title("My Pay Calculator")

# --- memory that survives across months and reruns ---
if "worked" not in st.session_state:
    st.session_state.worked = set()
if "view_year" not in st.session_state:
    st.session_state.view_year = 2026
if "view_month" not in st.session_state:
    st.session_state.view_month = 6

worked = st.session_state.worked
year = st.session_state.view_year
month = st.session_state.view_month

# --- month navigation ---
prev_col, title_col, next_col = st.columns([1, 3, 1])

if prev_col.button("◀", width="stretch"):
    if month == 1:
        st.session_state.view_month = 12
        st.session_state.view_year = year - 1
    else:
        st.session_state.view_month = month - 1
    st.rerun()

title_col.subheader(f"{calendar.month_name[month]} {year}")

if next_col.button("▶", width="stretch"):
    if month == 12:
        st.session_state.view_month = 1
        st.session_state.view_year = year + 1
    else:
        st.session_state.view_month = month + 1
    st.rerun()

# --- weekday headers ---
day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
header_cols = st.columns(7)
for col, name in zip(header_cols, day_names):
    col.markdown(f"**{name}**")

# --- the calendar grid ---
for week in calendar.monthcalendar(year, month):
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day == 0:
            continue
        d = date(year, month, day)
        selected = d in worked
        if cols[i].button(
            str(day),
            key=f"day-{d}",
            type="primary" if selected else "secondary",
            width="stretch",
        ):
            if selected:
                worked.discard(d)
            else:
                worked.add(d)
            st.rerun()

# --- clear button ---
if st.button("Clear all"):
    st.session_state.worked = set()
    st.rerun()

# --- results ---
if worked:
    st.divider()
    st.header("Your Pay")

    for friday, pay in sorted(weekly_breakdown(worked).items()):
        st.subheader(f"Pay day: {friday.strftime('%d/%m/%Y')}")
        st.write(f"Gross : £{pay['gross']:.2f}")
        st.write(f"Tax : £{pay['tax']:.2f}")
        st.write(f"NI : £{pay['ni']:.2f}")
        st.write(f"Net : £{pay['net']:.2f}")

    st.divider()
    st.header(f"{calendar.month_name[month]} {year} total")
    st.caption("Pay received during this month")
    totals = monthly_totals(worked, year, month)
    st.write(f"Gross : £{totals['gross']:.2f}")
    st.write(f"Tax : £{totals['tax']:.2f}")
    st.write(f"NI : £{totals['ni']:.2f}")
    st.write(f"Net : £{totals['net']:.2f}")