import streamlit as st
import random

st.set_page_config(page_title="Monty Hall Game", page_icon="🚪", layout="centered")

st.title("🚪 Monty Hall Game")
st.markdown("Pick a door and try to win the 🚗!")

# Session state variables
if "doors" not in st.session_state:
    st.session_state.doors = ['goat'] * 3
    car_pos = random.randint(0, 2)
    st.session_state.doors[car_pos] = 'car'
    st.session_state.user_choice = None
    st.session_state.revealed = None
    st.session_state.final = None
    st.session_state.game_over = False

# Step 1: Pick a door
if st.session_state.user_choice is None:
    choice = st.radio("Choose a door:", [1, 2, 3])
    if st.button("Confirm Choice"):
        st.session_state.user_choice = choice - 1

# Step 2: Monty reveals a goat
if st.session_state.user_choice is not None and st.session_state.revealed is None:
    options = [i for i in range(3)
               if i != st.session_state.user_choice and st.session_state.doors[i] == 'goat']
    st.session_state.revealed = random.choice(options)

# Show current game state
if st.session_state.user_choice is not None:
    st.write(f"🚪 You chose Door {st.session_state.user_choice + 1}")
    if st.session_state.revealed is not None:
        st.write(f"🐐 Monty opened Door {st.session_state.revealed + 1} — it's a goat!")

# Step 3: Switch or Stay
if st.session_state.revealed is not None and not st.session_state.game_over:
    action = st.radio("Do you want to switch?", ["Stay", "Switch"])
    if st.button("Reveal Result"):
        if action == "Switch":
            st.session_state.final = [i for i in range(3)
                                      if i != st.session_state.user_choice and i != st.session_state.revealed][0]
        else:
            st.session_state.final = st.session_state.user_choice

        st.session_state.game_over = True
        result = st.session_state.doors[st.session_state.final]
        if result == 'car':
            st.success(f"🎉 You won the 🚗 CAR behind Door {st.session_state.final + 1}!")
        else:
            st.error(f"🐐 You got a GOAT behind Door {st.session_state.final + 1}.")

        if st.button("Play Again 🔁"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.experimental_rerun()
