# -*- coding: utf-8 -*-



import pandas as pd #pandas is hierbij geïnstalleerd
import streamlit as st #streamlit is hierbij geïnstalleerd
import plotly.express as px #plotly-express is hierbij geïnstalleerd

st.set_page_config(page_title="Markteffect Dashboard",
                   layout="wide"
) #Hiermee heb ik het dashboard een titel gegeven en ervoor gezorgd dat het dashboard er groot uitziek
st.title("Markteffect Dashboard")

#Hier verander ik de naam van het bestand om het iets makkelijker te maken
Excelbestand = r"C:\Users\huubd\Documents\Smart Cities\Binnenstadsmeting Eindhoven 2022 (data Fontys) 2.1.xlsx"



df = pd.read_excel(            #Hierbij wordt het excelbestand gelezen
    io=Excelbestand,
    engine='openpyxl',
    sheet_name='Datasetje',
    usecols='A:CK',
    nrows=642,
)



#Hieronder gaan we verder met het aanpassen van het dashboard

#Hier komt een filter voor de locatie in Eindhoven

#Eerst een aantal afkortingen wijzigen
afkorting_gebied_Eindhoven = {
    'STDO': 'Stadsoord',
    'BER': 'Berenkuil',
    '18SP': '18 Septemberplein',
    'DMR': 'Dommelstraat',
    'HECA': 'Heuvel Galerie',
    'MA R': 'Markt',
    'STE': 'Stationsplein',
    'NWES': 'Nieuwe Emmasingel',
    'STRPS': 'Stratumseind'
}

df['Locatie'] = df['Locatie'].replace(afkorting_gebied_Eindhoven)

#Deze zijn nu in de tabel ook aangepast

#Nu ga ik verder met het filter/slicer.
st.sidebar.header("Filter")
city = st.sidebar.multiselect(
    "Locatie in Eindhoven",
    options=df['Locatie'].unique(),
    default=df['Locatie'].unique(),
)

#Dit is een filter/slicer voor hoe vaak een stad wordt bezocht

Frequentie_bezoek = st.sidebar.multiselect(
                  "Frequentie bezoek Eindhoven",
                  options=df['Frequentiebezoek'].unique(),
                  default=df['Frequentiebezoek'].unique())


#Hier komt een filter/slicer voor de opleidng


Opleiding = st.sidebar.multiselect(
          "Opleiding respondenten",
          options=df['Opleiding'].unique(),
          default=df['Opleiding'].unique())

#Hieronder ga ik de filters/slicers werkend maken

df_selection = df.query("Locatie == @city & "
                     "Frequentiebezoek == @Frequentie_bezoek &"
                       "Opleiding == @Opleiding")

st.dataframe(df_selection)

#Hieronder ga ik eerste grafiek proberen te maken
#De code hieronder is om een lege regel in het dashboard te krijgen
st.markdown('##')

#Dit is om een titel neer te zetten in het dashboard
st.title(":bar_chart: Opleidingen van respondenten")


#Hieronder ga ik proberen een grafiek te maken met hoeveel mensen één opleiding doen

Totaal_aantal_opleiding = df_selection.groupby(by=["Opleiding"]).nunique()["Response id"] 
Figuur_aantal_opleiding = px.bar(
    Totaal_aantal_opleiding,
    x=Totaal_aantal_opleiding.index,
    y="Response id",
    title="<b>Aantal opleidingen</b>",
    color_discrete_sequence=["#2CA02C"] * len(Totaal_aantal_opleiding),
    template="plotly_white",
)

#Hieronder doe ik aanpassingen aan de grafiek zodat de naam van de y-as anders wordt en de kleur van de staven veranderen.
Figuur_aantal_opleiding.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor = 'LightGreen',  title='Aantal respondenten'),
)


st.plotly_chart(Figuur_aantal_opleiding)

#Hieronder ga ik een cirkeldiagram maken met hoevaak mensen Eindhoven bezoeken in procenten
st.markdown('##')

st.title(":pie: Percentuele weergave van herhaaldelijke bezoeken in Eindhoven")
            

#Dit is om procenten te krijgen
df_percentage = df_selection['Frequentiebezoek'].value_counts(normalize=True) * 100

#Hiermee maak ik de cirkeldiagram
Cirkel_bezoek = px.pie(df_percentage, values=df_percentage, names=df_percentage.index, 
                       title='', 
                       color_discrete_sequence=px.colors.sequential.Greens_r)#Dit is om de kleuren te veranderen


#Hiermee komt het cikreldiagram te voorschijn
st.plotly_chart(Cirkel_bezoek)


#Nu ga ik een staafgrafiek maken waarbij te zien is wat de meest bezochten plekken zijn
st.markdown('##')

st.title("🏙️ Respondenten per wijk")

#Hierbij kan ik ongeveer hetzelfde neerzetten als bij de eerdere staafgrafiek
Totaal_bezoeken_in_wijk = df_selection.groupby(by=['Locatie']).nunique()["Response id"]
Grafiek_bezoeken_in_wijk = px.bar(
    Totaal_bezoeken_in_wijk,
    x=Totaal_bezoeken_in_wijk.index,
    y="Response id",
    color_discrete_sequence=["#2CA02C"] * len(Totaal_aantal_opleiding),
    template="plotly_white")

#Hiermee verander ik het uiterlijk van de grafiek
Grafiek_bezoeken_in_wijk.update_layout(
    xaxis=dict(tickmode='linear'),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGreen', title='Aantal respondenten'))

st.plotly_chart(Grafiek_bezoeken_in_wijk)


#Ik ga nog een cirkeldiagram toevoegen met hoe aangenaam de respondenten het bezoek in de binnenstad vonden
st.markdown('##')

st.title("☺️ Genoegen bezoek Eindhoven")

#Eerst de naam van een kolom wijzigen
df_aangenaam = df.rename(columns={"In hoeverre vindt u het bezoek aan de binnenstad van Eindhoven aangenaam, rekening houdend met de getroffen maat-regelen m.b.t. Covid-19?":
                   "Aangenaam"})
    
#Nu het percentage erin zetten
df_percentage_2 = df_aangenaam['Aangenaam'].value_counts(normalize=True) * 100

#Nu wordt de cirkeldiagram gemaakt
Cirkel_aangenaam = px.pie(df_percentage_2, values=df_percentage_2, names=df_percentage_2.index,
                          title='',
                          color_discrete_sequence=px.colors.sequential.Greens_r)

st.plotly_chart(Cirkel_aangenaam)

     











