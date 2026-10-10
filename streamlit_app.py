import streamlit as st

from screening.program_screener import screen

st.title("Benefits screener")
st.caption("This is an unofficial screening tool in progress")

size = st.number_input("How many people live in your household?", min_value=1, value=4)
income = st.number_input("Total yearly household income, before taxes ($)", min_value=0, value=48000)
ages_text = st.text_input("Everyone's ages, separated by commas", "37, 35, 12, 8")

if st.button("Check"):
    ages = []
    for part in ages_text.split(","):
        ages.append(int(part))

    household = {
        "size": size,
        "annual_income": income,
        "state": "CA",
        "ages": ages,
    }

    for result in screen(household):
        if result["qualifies"]:
            st.subheader("Likely yes: " + result["name"])
        else:
            st.subheader("Probably not: " + result["name"])
        for explanation in result["explanations"]:
            st.write(explanation)
        st.write("Apply: " + result["apply_url"])