import streamlit as st
from datetime import datetime

st.set_page_config(layout="wide")
st.title("🏈 Sideline Spotter Tool")

# Initialize session state
if "start_line" not in st.session_state:
    st.session_state.start_line = None
if "end_line" not in st.session_state:
    st.session_state.end_line = None
if "current_down" not in st.session_state:
    st.session_state.current_down = 1
if "distance_to_go" not in st.session_state:
    st.session_state.distance_to_go = 10
if "play_log" not in st.session_state:
    st.session_state.play_log = []
if "direction" not in st.session_state:
    st.session_state.direction = "Left to Right"

# Sidebar controls
with st.sidebar:
    st.header("Controls")
    st.session_state.direction = st.radio("Offensive Direction", ["Left to Right", "Right to Left"])
    if st.button("🔄 Reset Play Only"):
        st.session_state.start_line = None
        st.session_state.end_line = None
    if st.button("🧹 Reset Game"):
        st.session_state.start_line = None
        st.session_state.end_line = None
        st.session_state.current_down = 1
        st.session_state.distance_to_go = 10
        st.session_state.play_log = []

# Yard line button handler
def handle_yard_selection(label):
    if st.session_state.start_line is None:
        st.session_state.start_line = label
    elif st.session_state.end_line is None:
        st.session_state.end_line = label
    else:
        st.session_state.start_line = label
        st.session_state.end_line = None

# Convert yard label to football-aware value
def yard_value(label):
    if label == "50":
        return 50
    side = label[0]
    num = 0 if label[1:] == "G" else int(label[1:])
    raw = num if side == "L" else 100 - num
    return raw if st.session_state.direction == "Left to Right" else 100 - raw

# Yard line matrix renderer
def render_matrix():
    st.markdown("### 🏟️ Yard Line Matrix")
    st.markdown(f"**Offense {st.session_state.direction}**")

    for row_start in [0, 10, 20, 30, 40]:
        left_labels = [f"L{'G' if i == 0 else i}" for i in range(row_start, row_start + 10)]
        right_labels = [f"R{'G' if i == 0 else i}" for i in range(49 - row_start, 39 - row_start, -1)]

        cols = st.columns(21)

        # Left side
        for i, label in enumerate(left_labels):
            if label == st.session_state.start_line:
                cols[i].markdown(f"<div style='background-color:#add8e6; padding:6px; border-radius:6px; text-align:center; font-weight:bold;'>{label}</div>", unsafe_allow_html=True)
            elif label == st.session_state.end_line:
                cols[i].markdown(f"<div style='background-color:#ffa500; padding:6px; border-radius:6px; text-align:center; font-weight:bold;'>{label}</div>", unsafe_allow_html=True)
            else:
                if cols[i].button(label, key=f"left_{label}"):
                    handle_yard_selection(label)

        # Midfield
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

        # Right side
        for i, label in enumerate(right_labels):
            if label == st.session_state.start_line:
                cols[i + 11].markdown(f"<div style='background-color:#add8e6; padding:6px; border-radius:6px; text-align:center; font-weight:bold;'>{label}</div>", unsafe_allow_html=True)
            elif label == st.session_state.end_line:
                cols[i + 11].markdown(f"<div style='background-color:#ffa500; padding:6px; border-radius:6px; text-align:center; font-weight:bold;'>{label}</div>", unsafe_allow_html=True)
            else:
                if cols[i + 11].button(label, key=f"right_{label}"):
                    handle_yard_selection(label)

render_matrix()

# Display current down & distance before play
st.markdown(f"### 🧭 Current Situation: **{st.session_state.current_down} & {st.session_state.distance_to_go}**")

# Display play result
start = st.session_state.start_line
end = st.session_state.end_line

if start and end:
    start_val = yard_value(start)
    end_val = yard_value(end)
    yards_gained = end_val - start_val

    # Determine result
    first_down = yards_gained >= st.session_state.distance_to_go
    no_gain = yards_gained == 0
    color = "#28a745" if first_down else "#dc3545" if no_gain else "#5c5b5b"
    message = "✅ First Down!" if first_down else "⛔ No Gain" if no_gain else "Play Recorded"

    # Update down & distance BEFORE logging
    new_down = 1 if first_down else st.session_state.current_down + 1
    new_distance = 10 if first_down else st.session_state.distance_to_go - yards_gained
    if new_down > 4:
        new_down = 1
        new_distance = 10  # Placeholder for turnover logic

    # Stylized container
    st.markdown(
        f"""
        <div style="background-color:{color}; padding:20px; border-radius:10px; box-shadow:2px 2px 10px rgba(0,0,0,0.2); text-align:center;">
            <h2 style="color:white; margin-bottom:10px;">{message}</h2>
            <h1 style="color:white;">Yards Gained: {yards_gained}</h1>
            <h3 style="color:white;">Next Down: {new_down} & Distance: {new_distance}</h3>
            <h4 style="color:white;">Ball Spot: {end}</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Log the play with updated down/distance
    st.session_state.play_log.append({
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "start": start,
        "end": end,
        "yards": yards_gained,
        "down": new_down,
        "distance": new_distance,
        "spot": end
    })

    # Apply new down & distance
    st.session_state.current_down = new_down
    st.session_state.distance_to_go = new_distance

    # Reset yard line selections
    st.session_state.start_line = None
    st.session_state.end_line = None

# Display play log
if st.session_state.play_log:
    st.markdown("### 📒 Play Log")
    for entry in reversed(st.session_state.play_log):
        st.markdown(
            f"- `{entry['timestamp']}` | {entry['start']} → {entry['end']} | Yards: **{entry['yards']}** | Down: {entry['down']} & Distance: {entry['distance']} | Ball Spot: {entry['spot']}"
        )
