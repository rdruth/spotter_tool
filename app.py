import streamlit as st

# Inject custom CSS to reduce button height and prevent text wrapping
st.markdown("""
    <style>
    div.stButton > button {
        height: 40px;
        padding: 4px 12px;
        font-size: 16px;
        white-space: nowrap;
    }
    </style>
""", unsafe_allow_html=True)

# Option 1: Inline label (e.g., "L12")
st.button("L12")

# Option 2: Stacked label (e.g., "L" on top, "12" below)
st.button("L<br>12", unsafe_allow_html=True)

# Optional layout control using columns
col1, col2, col3 = st.columns(3)
with col1:
    st.button("L<br>12", unsafe_allow_html=True)
with col2:
    st.button("R<br>34", unsafe_allow_html=True)
with col3:
    st.button("C<br>56", unsafe_allow_html=True)

