import streamlit as st
from datetime import datetime

# --- Page Setup ---
st.set_page_config(layout="wide")

# --- Reserve Top Space for Play Result ---
result_container = st.empty()

# --- Initialize Session State ---
if "start_line" not in st.session_state:
    st.session_state.start_line = None
if "end_line" not in st.session_state:
    st.session_state.end_line = None
if "current_down" not in st.session_state:
    st.session_state.current_down = 1
if "distance_to_go" not in st.session_state:
    st.session_state.distance_to_go = 10
if "direction" not in st.session_state:
    st.session_state.direction = "Left to Right"
if "play_ready" not in st.session_state:
    st.session_state.play_ready = False

# --- Display Down & Distance ---
st.markdown(f"### 📍 Play Down and Distance: **{st.session_state.current_down} & {st.session_state.distance_to_go}**")

# --- Play Result Logic (Only if play_ready is True) ---
start = st.session_state.start_line
end = st.session_state.end_line

if st.session_state.play_ready and start and end:
    def yard_value(label):
        if label == "50":
            return 50
        side = label[0]
        num = 0 if label[1:] == "G" else int(label[1:])
        raw = num if side == "L" else 100 - num
        return raw if st.session_state.direction == "Left to Right" else 100 - raw

    start_val = yard_value(start)
    end_val = yard_value(end)
    yards_gained = end_val - start_val

    first_down = yards_gained >= st.session_state.distance_to_go
    no_gain = yards_gained == 0
    color = "#28a745" if first_down else "#dc3545" if no_gain else "#5c5b5b"
    message = "✅ First Down!" if first_down else "⛔ No Gain" if no_gain else "Play Recorded"

    new_down = 1 if first_down else st.session_state.current_down + 1
    new_distance = 10 if first_down else st.session_state.distance_to_go - yards_gained
    if new_down > 4:
        new_down = 1
        new_distance = 10  # Placeholder for turnover logic

    result_container.markdown(f"""
        <div style="background-color:{color}; padding:20px; border-radius:10px; box-shadow:2px 2px 10px rgba(0,0,0,0.2); text-align:center;">
            <h2 style="color:white; margin-bottom:10px;">{message}</h2>
            <h1 style="color:white;">Yards Gained: {yards_gained}</h1>
            <h3 style="color:white;">Next Down: {new_down} & Distance: {new_distance}</h3>
            <h4 style="color:white;">Ball Spot: {end}</h4>
        </div>
    """, unsafe_allow_html=True)

    st.session_state.current_down = new_down
    st.session_state.distance_to_go = new_distance
    st.session_state.play_ready = False  # Reset flag after result shown

# --- Inline Controls Row ---
st.markdown("### ⚙️ Controls")
control_cols = st.columns([2, 1, 1, 1, 1, 1])
with control_cols[0]:
    st.session_state.direction = st.radio("Offensive Direction", ["Left to Right", "Right to Left"], horizontal=True)
with control_cols[1]:
    if st.button("🔄 Reset Play"):
        st.session_state.start_line = None
        st.session_state.end_line = None
        st.session_state.play_ready = False
with control_cols[2]:
    if st.button("🧹 Reset Game"):
        st.session_state.start_line = None
        st.session_state.end_line = None
        st.session_state.current_down = 1
        st.session_state.distance_to_go = 10
        st.session_state.play_ready = False
with control_cols[3]:
    if st.button("➕ New Play"):
        if st.session_state.end_line:
            st.session_state.start_line = st.session_state.end_line
            st.session_state.end_line = None
            st.session_state.play_ready = False
with control_cols[4]:
    if st.button("⛔ No Gain"):
        st.session_state.end_line = st.session_state.start_line
        st.session_state.play_ready = True


# --- Yard Line Button Handler ---
def handle_yard_selection(label):
    if st.session_state.start_line is None:
        st.session_state.start_line = label
    elif st.session_state.end_line is None:
        st.session_state.end_line = label
        st.session_state.play_ready = True


# --- Yard Line Matrix Renderer ---
def render_matrix():
    st.markdown("### 🏟️ Yard Line Matrix")
    st.markdown(f"**Offense {st.session_state.direction}**")

    for row_start in [0, 10, 20, 30, 40]:
        left_labels = [f"L{'G' if i == 0 else i}" for i in range(row_start, row_start + 10)]
        right_labels = [f"R{'G' if i == 0 else i}" for i in range(49 - row_start, 39 - row_start, -1)]
        cols = st.columns(21)

        for i, label in enumerate(left_labels):
            if label == st.session_state.start_line:
                cols[i].markdown(f"<div style='background-color:#add8e6; padding:6px; border-radius:6px; text-align:center; font-weight:bold;'>{label}</div>", unsafe_allow_html=True)
            elif label == st.session_state.end_line:
                cols[i].markdown(f"<div style='background-color:#ffa500; padding:6px; border-radius:6px; text-align:center; font-weight:bold;'>{label}</div>", unsafe_allow_html=True)
            else:
                if cols[i].button(label, key=f"left_{label}"):
                    handle_yard_selection(label)

        if row_start == 0:
            label = "50"
            if label == st.session_state.start_line:
                cols[10].markdown(f"<div style='background-color:#add8e6; padding:6px; border-radius:6px; text-align:center; font-weight:bold;'>{label}</div>", unsafe_allow_html=True)
            elif label == st.session_state.end_line:
                cols[10].markdown(f"<div style='background-color:#ffa500; padding:6px; border-radius:6px; text-align:center; font-weight:bold;'>{label}</div>", unsafe_allow_html=True)
            else:
                if cols[10].button(label, key="mid_50"):
                    handle_yard_selection(label)
        else:
            cols[10].markdown("")

        for i, label in enumerate(right_labels):
            if label == st.session_state.start_line:
                cols[i + 11].markdown(f"<div style='background-color:#add8e6; padding:6px; border-radius:6px; text-align:center; font-weight:bold;'>{label}</div>", unsafe_allow_html=True)
            elif label == st.session_state.end_line:
                cols[i + 11].markdown(f"<div style='background-color:#ffa500; padding:6px; border-radius:6px; text-align:center; font-weight:bold;'>{label}</div>", unsafe_allow_html=True)
            else:
                if cols[i + 11].button(label, key=f"right_{label}"):
                    handle_yard_selection(label)

render_matrix()
