import pathlib
import time

import streamlit as st

from create_video import create_video


def create_app():
    st.title("Link Verarbeitungs-App")

    title = st.text_input("Titel")

    links = st.text_area("Gib deine Links hier ein (einer pro Zeile):", height=200)

    link_list = links.splitlines()

    if st.button("Links verarbeiten"):
        if link_list and title:
            video_file = create_video(link_list, title=title)

            # Download-Button für die Textdatei
            with pathlib.Path.open(video_file, "rb") as f:
                st.success(f"Verarbeitung der Links abgeschlossen! Du kannst dein Video hier herunterladen:")
                st.download_button("Download Videofile", f, file_name=video_file)

        else:
            st.warning("Bitte füge mindestens einen Link und einen Titel hinzu.")

    st.markdown("""
    ### Hinweise:
    - Gib jeden Link in eine neue Zeile ein.
    - Die Verarbeitung der Links wird in der Zukunft implementiert.
    """)
