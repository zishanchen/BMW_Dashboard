import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import base64

# Stileinstellungen für bessere Visualisierungen
plt.style.use('ggplot')
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Arial'

# BMW-Farben definieren
bmw_blue = '#0166B1'
bmw_light_blue = '#1C69D3'
bmw_background = '#FFFFFF'
bmw_plot_bg = '#F5F5F5'

# Datensatz erstellen
data = {
    'Bestellnummer': [12345, 12346, 12347, 12348, 12349],
    'Artikel': ['Getriebe', 'Motoröl', 'Bremsbeläge', 'Reifen', 'Stoßdämpfer'],
    'Menge': [50, 100, 25, 80, 30],
    'Bestelldatum': ['01.01.2023', '02.01.2023', '05.01.2023', '10.01.2023', '15.01.2023'],
    'Lieferdatum': ['15.01.2023', '10.01.2023', '20.01.2023', '25.01.2023', '30.01.2023'],
    'Lieferstatus': ['Ausgeliefert', 'Ausgeliefert', 'Ausgeliefert', 'Ausgeliefert', 'Ausgeliefert']
}

# In DataFrame umwandeln
df = pd.DataFrame(data)

# Datumsangaben in Datetime-Objekte umwandeln
df['Bestelldatum'] = pd.to_datetime(df['Bestelldatum'], format='%d.%m.%Y')
df['Lieferdatum'] = pd.to_datetime(df['Lieferdatum'], format='%d.%m.%Y')

# Lieferzeit in Tagen berechnen
df['Lieferzeit'] = (df['Lieferdatum'] - df['Bestelldatum']).dt.days

# Kennzahlen berechnen
total_orders = len(df)
total_items = df['Menge'].sum()
avg_delivery_time = df['Lieferzeit'].mean()
fastest_delivery = df['Lieferzeit'].min()
slowest_delivery = df['Lieferzeit'].max()

print("=== Kernkennzahlen ===")
print(f"Gesamtbestellungen: {total_orders}")
print(f"Gesamtartikel: {total_items}")
print(f"Durchschnittliche Lieferzeit: {avg_delivery_time:.1f} Tage")
print(f"Schnellste Lieferung: {fastest_delivery} Tage")
print(f"Langsamste Lieferung: {slowest_delivery} Tage")
print()

# DataFrame mit Lieferzeit anzeigen
df['Bestelldatum'] = df['Bestelldatum'].dt.strftime('%d.%m.%Y')
df['Lieferdatum'] = df['Lieferdatum'].dt.strftime('%d.%m.%Y')
print("=== Bestellungsübersicht mit Lieferzeit ===")
print(df[['Bestellnummer', 'Artikel', 'Menge', 'Bestelldatum', 'Lieferdatum', 'Lieferzeit', 'Lieferstatus']])

# Dashboard erstellen
def create_dashboard(df):
    # Datumsangaben für die Visualisierung zurück in Datetime konvertieren
    df['Bestelldatum'] = pd.to_datetime(df['Bestelldatum'], format='%d.%m.%Y')
    df['Lieferdatum'] = pd.to_datetime(df['Lieferdatum'], format='%d.%m.%Y')
    
    # Subplot-Figur erstellen
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Bestellmenge nach Artikeltyp", 
            "Lieferzeit nach Artikeltyp",
            "Lieferzeit im Zeitverlauf",
            "Bestellvolumen nach Datum"
        ),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "bar"}]],
        vertical_spacing=0.12,
        horizontal_spacing=0.08
    )
    
    # 1. Balkendiagramm - Bestellmenge nach Artikeltyp
    df_sorted = df.sort_values('Menge', ascending=False)
    fig.add_trace(
        go.Bar(
            x=df_sorted['Artikel'],
            y=df_sorted['Menge'],
            marker_color=bmw_blue,
            name="Bestellmenge"
        ),
        row=1, col=1
    )
    
    # 2. Balkendiagramm - Lieferzeit nach Artikeltyp
    fig.add_trace(
        go.Bar(
            x=df['Artikel'],
            y=df['Lieferzeit'],
            marker_color=bmw_light_blue,
            name="Lieferzeit (Tage)"
        ),
        row=1, col=2
    )
    
    # Durchschnittslinie hinzufügen
    fig.add_shape(
        type="line",
        x0=-0.5,
        x1=4.5,
        y0=avg_delivery_time,
        y1=avg_delivery_time,
        line=dict(color="red", width=2, dash="dash"),
        row=1, col=2
    )
    
    # Anmerkung für Durchschnittslinie
    fig.add_annotation(
        x=4,
        y=avg_delivery_time,
        text=f"Ø {avg_delivery_time:.1f} Tage",
        showarrow=False,
        font=dict(color="red"),
        row=1, col=2
    )
    
    # 3. Liniendiagramm - Lieferzeit im Zeitverlauf
    df_time_sorted = df.sort_values('Bestelldatum')
    fig.add_trace(
        go.Scatter(
            x=df_time_sorted['Bestelldatum'],
            y=df_time_sorted['Lieferzeit'],
            mode='lines+markers',
            name="Lieferzeit im Zeitverlauf",
            line=dict(color=bmw_blue, width=3),
            marker=dict(size=10)
        ),
        row=2, col=1
    )
    
    # Durchschnittslinie hinzufügen
    fig.add_shape(
        type="line",
        x0=df_time_sorted['Bestelldatum'].min(),
        x1=df_time_sorted['Bestelldatum'].max(),
        y0=avg_delivery_time,
        y1=avg_delivery_time,
        line=dict(color="red", width=2, dash="dash"),
        row=2, col=1
    )
    
    # 4. Balkendiagramm - Bestellvolumen nach Datum
    fig.add_trace(
        go.Bar(
            x=df_time_sorted['Bestelldatum'],
            y=df_time_sorted['Menge'],
            marker_color=[bmw_blue, bmw_light_blue, '#3A8DDE', '#63A1E0', '#8FB6E3'],
            name="Bestellvolumen"
        ),
        row=2, col=2
    )
    
    # KPI-Indikatoren am oberen Rand hinzufügen
    fig.add_annotation(
        x=0.125, y=1.12,
        xref="paper", yref="paper",
        text=f"<b>Gesamtbestellungen</b><br>{total_orders}",
        showarrow=False,
        font=dict(size=14, color=bmw_blue),
        align="center",
        bgcolor="white",
        bordercolor=bmw_blue,
        borderwidth=2,
        borderpad=6,
        opacity=0.8
    )
    
    fig.add_annotation(
        x=0.375, y=1.12,
        xref="paper", yref="paper",
        text=f"<b>Gesamtartikel</b><br>{total_items}",
        showarrow=False,
        font=dict(size=14, color=bmw_blue),
        align="center",
        bgcolor="white",
        bordercolor=bmw_blue,
        borderwidth=2,
        borderpad=6,
        opacity=0.8
    )
    
    fig.add_annotation(
        x=0.625, y=1.12,
        xref="paper", yref="paper",
        text=f"<b>Ø Lieferzeit</b><br>{avg_delivery_time:.1f} Tage",
        showarrow=False,
        font=dict(size=14, color=bmw_blue),
        align="center",
        bgcolor="white",
        bordercolor=bmw_blue,
        borderwidth=2,
        borderpad=6,
        opacity=0.8
    )
    
    fig.add_annotation(
        x=0.875, y=1.12,
        xref="paper", yref="paper",
        text=f"<b>Lieferstatus</b><br>100% Ausgeliefert",
        showarrow=False,
        font=dict(size=14, color=bmw_blue),
        align="center",
        bgcolor="white",
        bordercolor=bmw_blue,
        borderwidth=2,
        borderpad=6,
        opacity=0.8
    )
    
     # Layout mit verbesserten Farben aktualisieren und hellen Hintergrund sicherstellen
    fig.update_layout(
        template="plotly_white",
        title={
            'text': "BMW Bestell- und Produktionssystem Dashboard",
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20, color=bmw_blue)
        },
        height=800,
        width=1200,
        showlegend=False,
        plot_bgcolor=bmw_plot_bg,  # Light gray for plot areas
        paper_bgcolor=bmw_background,  # White for main background
        margin=dict(t=120, b=20, l=60, r=40),
        font=dict(color='#333333')  # Dark gray for text to ensure visibility
    )
    
    # Raster- und Achsenfarben für bessere Sichtbarkeit festlegen
    fig.update_xaxes(gridcolor='rgba(211, 211, 211, 0.5)', tickfont=dict(color='#333333'))
    fig.update_yaxes(gridcolor='rgba(211, 211, 211, 0.5)', tickfont=dict(color='#333333'))
    
    # Benutzerdefinierte Beschriftungen und Styling hinzufügen
    fig.update_xaxes(title_text="Artikel", row=1, col=1)
    fig.update_yaxes(title_text="Menge (Stk.)", row=1, col=1)
    
    fig.update_xaxes(title_text="Artikel", row=1, col=2)
    fig.update_yaxes(title_text="Lieferzeit (Tage)", row=1, col=2)
    
    fig.update_xaxes(title_text="Bestelldatum", row=2, col=1)
    fig.update_yaxes(title_text="Lieferzeit (Tage)", row=2, col=1)
    
    fig.update_xaxes(title_text="Bestelldatum", row=2, col=2)
    fig.update_yaxes(title_text="Menge (Stk.)", row=2, col=2)
    
    # In HTML konvertieren und CSS hinzufügen, um hellen Modus zu erzwingen
    html_string = fig.to_html()
    
    # Meta-Tag und CSS hinzufügen, um den hellen Modus zu erzwingen
    html_string = html_string.replace('<head>', '''<head>
    <meta name="color-scheme" content="light">
    <style>
        body {
            background-color: white !important;
            color: #333333 !important;
        }
        .plotly-graph-div {
            background-color: white !important;
        }
        .js-plotly-plot {
            background-color: white !important;
        }
        .bg-base-100 {
            background-color: white !important;
        }
    </style>''')
    
    # Modifiziertes HTML speichern
    with open("bmw_dashboard.html", "w", encoding='utf-8') as f:
        f.write(html_string)
    
    # Figur anzeigen
    fig.show()
    
    return fig

# Dashboard generieren
dashboard = create_dashboard(df)

# Datenanalyse in eine Textdatei exportieren
with open('bmw_data_analysis.txt', 'w', encoding='utf-8') as f:
    f.write("BMW Bestell- und Produktionssystem Datenanalyse\n")
    f.write("==============================================\n\n")
    f.write("Kernkennzahlen:\n")
    f.write(f"- Gesamtbestellungen: {total_orders}\n")
    f.write(f"- Gesamtartikel: {total_items}\n")
    f.write(f"- Durchschnittliche Lieferzeit: {avg_delivery_time:.1f} Tage\n")
    f.write(f"- Schnellste Lieferung: {fastest_delivery} Tage\n")
    f.write(f"- Langsamste Lieferung: {slowest_delivery} Tage\n\n")
    
    f.write("Bestellübersicht:\n")
    f.write(df[['Bestellnummer', 'Artikel', 'Menge', 'Bestelldatum', 'Lieferdatum', 'Lieferzeit', 'Lieferstatus']].to_string(index=False))
    
print("\nDashboard und Analyse wurden erfolgreich erstellt!")
print("Dateien: bmw_dashboard.html, bmw_data_analysis.txt")
