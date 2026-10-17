import streamlit as st

from screening.poverty_guidelines import screen

st.set_page_config(page_title="Benefits screener", page_icon="", layout="centered")

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] { background: #f5f6f1; }
    [data-testid="stAppViewContainer"] * { color: #000000 !important; }
    .main .block-container { max-width: 850px; padding-top: 3rem; padding-bottom: 4rem; }
    [data-testid="stHeader"] { background: transparent; }
    h1 { font-family: Georgia, serif; font-weight: 500; }
    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input { background: #ffffff; }
    [data-testid="stNumberInput"] button { background: #ffffff; }
    [data-testid="stForm"] {
        background: #ffffff;
        border: 1px solid #dfe5de;
        border-radius: 8px;
        padding: 1.25rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Find benefits that may fit")
st.caption("A quick, unofficial eligibility estimate for California households.")

with st.form("household_form"):
    size = st.number_input(
        "People in your household", min_value=1, max_value=20, value=4, step=1
    )
    income = st.number_input(
        "Total annual household income before taxes ($)",
        min_value=0,
        value=48000,
        step=1000,
    )
    ages_text = st.text_input(
        "Age of each person, separated by commas", "37, 35, 12, 8"
    )
    st.caption("Enter one age for each household member. We only check California programs.")
    submitted = st.form_submit_button("Check possible benefits", type="primary")

if submitted:
    try:
        ages = [int(part.strip()) for part in ages_text.split(",")]
        if any(age < 0 or age > 120 for age in ages):
            raise ValueError("Ages must be between 0 and 120.")
        if len(ages) != size:
            raise ValueError(f"Enter exactly {size} ages, one for each household member.")
    except ValueError as error:
        st.error(str(error) or "Enter ages as whole numbers separated by commas.")
    else:
        household = {
            "size": size,
            "annual_income": income,
            "state": "CA",
            "ages": ages,
        }

        results = screen(household)
        likely_count = sum(result["qualifies"] for result in results)
        st.divider()
        st.subheader("Your screening results")
        st.write(f"**{likely_count} of {len(results)} programs** may be a fit based on the rules checked.")

        for result in results:
            with st.container(border=True):
                st.markdown(f"#### {result['name']}")
                if result["qualifies"]:
                    st.success("Likely eligible based on the information entered")
                else:
                    st.info("May not meet the rules checked")
                for explanation in result["explanations"]:
                    st.text(explanation)
                st.link_button("Open application", result["apply_url"])

        st.caption(
            "This estimate is not an application or an eligibility decision. "
            "Program rules may include other requirements; confirm details with each agency."
        )