import streamlit as st
from aux import *

import os
from dotenv import load_dotenv

load_dotenv()

# --- UI ---
st.set_page_config(page_title="Optimize Route", page_icon="🚗")
st.title(":oncoming_automobile: Route Optimizer with Google Maps (by time)")

# google_maps_api_key = st.sidebar.text_input(
#   'Google Maps API key', 
#   type='password', 
#   value="", 
#   help="Enter your Google Maps API key to use the service."
#   )
# st.sidebar.markdown(f"[Google Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/overview)", unsafe_allow_html=True)

google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")


st.markdown("Add addresses, choose the start and end point, and generate the best route based on estimated travel time.")

input_data = st.data_editor(
  {"Address": [""]},
  num_rows="dynamic",
  key="editor"
)

addresses = [addr.strip() for addr in input_data["Address"] if isinstance(addr, str) and addr.strip() != ""]

if len(addresses) >= 2:
  start = st.selectbox("Choose the starting point", addresses)
  end = st.selectbox("Choose the end point", addresses, index=len(addresses) - 1)

  travel_modes = {
    "Car": "driving",
    "Walking": "walking",
    "Biking": "bicycling",
    "Public transport": "transit"
  }

  select_mode_label = st.selectbox(
    "Choose the mode of transportation",
    list(travel_modes.keys()),
    index=0,
    help="Available modes: Car, Walking, Biking, Public transport"
  )

  travel_mode = travel_modes[select_mode_label]

  if st.button("Calculate best route"):
    try:
      # Calculates the best route based on time
      best_route = calculate_best_route_by_time(addresses, start, end, travel_mode, google_maps_api_key)

      if best_route:
        st.markdown("### :round_pushpin: Optimized Route:")
        st.write(" \u2794 ".join(best_route))

        # Generates and displays the link to Google Maps
        url = generate_google_maps_link(best_route, travel_mode)
        st.markdown(f"[Open in Google Maps]({url})", unsafe_allow_html=True)
        st.components.v1.iframe(generate_google_maps_embed_link(best_route, travel_mode, google_maps_api_key), width=700, height=500)
      else:
        st.error(
          "The route could not be calculated.  \n\n"
          "🔑 Check if the API key was entered correctly in the side menu.  \n"
          "📍 Also check that all addresses are valid and well formatted."
        )

    except ValueError as e:
      st.error(
        "The route could not be calculated.  \n\n"
        "🔑 Check the API key.  \n"
        f"🚗 Make sure the the transportation method '{select_mode_label}' is valid (try change it).  \n"
        "📍 Make sure the addresses are correct."
      )
      st.error(f"Error calculating route: {e}")

else:
  st.info("⚠️ Add at least two addresses to start route calculation.")

