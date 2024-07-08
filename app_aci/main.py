import streamlit as st
import pandas as pd
import requests

st.title("Uploader un fichier Excel et le rendre accessible via une API")

uploaded_file = st.file_uploader("Choisissez un fichier Excel", type="xlsx")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df = df[['JournalCode', 'JournalLib']]
    st.write(len(df))
    st.write("Aperçu du DataFrame chargé:")
    st.write(df)

    if st.button("Envoyer le DataFrame à l'API"):
        # Remplacer les valeurs NaN par None
        df = df.where(pd.notnull(df), None)
        # Conversion du DataFrame en une liste de dictionnaires
        data = df.to_dict(orient='records')
        response = requests.post("http://127.0.0.1:8000/upload/", json=data)

        if response.status_code == 200:
            st.success("DataFrame envoyé avec succès à l'API")
        else:
            st.error(f"Erreur lors de l'envoi du DataFrame à l'API: {response.content}")

st.write("Utilisez l'API pour accéder aux données uploadées.")
