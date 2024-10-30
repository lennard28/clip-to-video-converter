import streamlit as st
import time

from create_video import create_video

def create_app():
    st.title("Link Verarbeitungs-App")

    links = st.text_area("Gib deine Links hier ein (einer pro Zeile):", height=200)

    link_list = links.splitlines()

    if st.button("Links verarbeiten"):
        if link_list:
            # TODO process
            create_video(link_list)
            progress_bar = st.progress(0)

            for i in range(len(link_list)):
                time.sleep(0.5)
                
                progress_bar.progress((i + 1) / len(link_list))
            
            filename = "links.txt"
            with open(filename, "w") as f:
                for link in link_list:
                    f.write(link + "\n")

            st.success("Die Links wurden verarbeitet! Du kannst die Textdatei hier herunterladen:")
        
        # Download-Button für die Textdatei
            with open(filename, "rb") as f:
                st.download_button("Download Textdatei", f, file_name=filename)
            st.success(f"Verarbeitung der Links abgeschlossen! Du kannst dein Video hier herunterladen:")

        else:
            st.warning("Bitte füge mindestens einen Link hinzu.")

    st.markdown("""
    ### Hinweise:
    - Gib jeden Link in eine neue Zeile ein.
    - Die Verarbeitung der Links wird in der Zukunft implementiert.
    """)