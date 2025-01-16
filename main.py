import pandas as pd
import folium
from SPARQLWrapper import SPARQLWrapper, JSON
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime



# ------------------------------------------fonction pour reccuper les données -------------------------------------------------
def get_parks_ecosystem_data():
    """Récupère les données des parcs avec indicateurs indirects de biodiversité"""
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    
    query = """
    SELECT DISTINCT ?park ?parkLabel ?countryLabel ?location ?description ?inception 
           ?area ?elevation ?biome ?biomeLabel ?climate ?climateLabel
    WHERE {
      ?park wdt:P31/wdt:P279* wd:Q46169.  # Parc national
      ?park wdt:P17 ?country.              # Pays
      ?park wdt:P625 ?location.            # Coordonnées
      ?country wdt:P30 wd:Q15.             # En Afrique

      OPTIONAL { ?park schema:description ?description. FILTER(LANG(?description) = "en") }           
      OPTIONAL { ?park wdt:P571 ?inception. }  # Date de création
      OPTIONAL { ?park wdt:P2046 ?area. }      # Superficie
      OPTIONAL { ?park wdt:P2044 ?elevation. } # Élévation
      OPTIONAL { 
        ?park wdt:P1435 ?biome.            # Écosystème/Biome
      }
      OPTIONAL {
        ?park wdt:P197 ?climate.           # Zone climatique
      }
      
      SERVICE wikibase:label {
        bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".
      }
    }
    ORDER BY ?parkLabel
    """
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    parks_data = []
    for result in results["results"]["bindings"]:
        location_str = result["location"]["value"]
        coords = location_str.replace("Point(", "").replace(")", "").split()
        
        # Traitement des données
        inception_date = None
        if "inception" in result:
            try:
                inception_date = pd.to_datetime(result["inception"]["value"])
            except:
                pass
                
        # Extraction des indicateurs environnementaux
        area = float(result["area"]["value"]) if "area" in result else None
        elevation = float(result["elevation"]["value"]) if "elevation" in result else None
        biome = result.get("biomeLabel", {}).get("value", None)
        climate = result.get("climateLabel", {}).get("value", None)
        
        parks_data.append({
            'park': result["parkLabel"]["value"],
            'country': result["countryLabel"]["value"],
            'description': result.get("description", {}).get("value", ""),
            'latitude': float(coords[1]),
            'longitude': float(coords[0]),
            'creation_date': inception_date,
            'area_km2': area,
            'elevation_m': elevation,
            'biome': biome,
            'climate': climate
        })
    
    return pd.DataFrame(parks_data)




# ------------------------------------------fonction pour créer l'histogramme  de la distribution des parcs-------------------------------------------------

def create_parks_distribution(df):
    """Crée un histogramme de la distribution des parcs par pays"""
    plt.figure(figsize=(15, 8))
    country_counts = df['country'].value_counts()
    
    sns.barplot(x=country_counts.values, y=country_counts.index)
    plt.title('Distribution des Parcs Nationaux par Pays Africain')
    plt.xlabel('Nombre de Parcs')
    plt.ylabel('Pays')
    
    return plt






# ------------------------------------------fonction pour créer la serie temporelle  -------------------------------------------------
def create_temporal_analysis(df):
    """Crée des visualisations pour l'analyse temporelle"""
    df_with_dates = df.dropna(subset=['creation_date']).copy()
    
    # Création de la colonne décennie
    df_with_dates['decade'] = df_with_dates['creation_date'].dt.year // 10 * 10
    parks_by_decade = df_with_dates['decade'].value_counts().sort_index()
    
    plt.figure(figsize=(15, 6))
    plt.subplot(1, 2, 1)
    parks_by_decade.plot(kind='bar')
    plt.title('Création de Parcs Nationaux par Décennie')
    plt.xlabel('Décennie')
    plt.ylabel('Nombre de Parcs Créés')
    plt.xticks(rotation=45)
    
    plt.subplot(1, 2, 2)
    df_sorted = df_with_dates.sort_values('creation_date')
    cumulative = pd.DataFrame({
        'date': df_sorted['creation_date'],
        'cumulative_count': range(1, len(df_sorted) + 1)
    })
    plt.plot(cumulative['date'], cumulative['cumulative_count'])
    plt.title('Création Cumulative des Parcs Nationaux')
    plt.xlabel('Année')
    plt.ylabel('Nombre Total de Parcs')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    return plt






# ------------------------------------------fonction pour créer Distribution des Superficies des Parcs -------------------------------------------------
def analyze_ecosystem_indicators(df):
    """Analyse les indicateurs environnementaux des parcs"""
    plt.figure(figsize=(15, 10))
    
    # 1. Distribution des superficies
    plt.subplot(2, 2, 1)
    df['area_km2'].dropna().hist(bins=30)
    plt.title('Distribution des Superficies des Parcs')
    plt.xlabel('Superficie (km²)')
    plt.ylabel('Nombre de parcs')
    
    # 2. Distribution des élévations
    plt.subplot(2, 2, 2)
    df['elevation_m'].dropna().hist(bins=30)
    plt.title('Distribution des Élévations')
    plt.xlabel('Élévation (m)')
    plt.ylabel('Nombre de parcs')
    
    # 3. Distribution des biomes
    plt.subplot(2, 2, 3)
    if not df['biome'].isna().all():
        biome_counts = df['biome'].value_counts()
        sns.barplot(x=biome_counts.values, y=biome_counts.index)
        plt.title('Distribution des Biomes')
        plt.xlabel('Nombre de parcs')
    
    # 4. Évolution temporelle de la superficie protégée
    plt.subplot(2, 2, 4)
    df_with_dates = df.dropna(subset=['creation_date', 'area_km2']).copy()
    df_with_dates = df_with_dates.sort_values('creation_date')
    df_with_dates['cumulative_area'] = df_with_dates['area_km2'].cumsum()
    plt.plot(df_with_dates['creation_date'], df_with_dates['cumulative_area'])
    plt.title('Évolution de la Superficie Totale Protégée')
    plt.xlabel('Année')
    plt.ylabel('Superficie cumulée (km²)')
    
    plt.tight_layout()
    return plt



# ------------------------------------------fonction pour créer la carte interactive des parcs nationaux avec dates de création -------------------------------------------------

def create_parks_map(df):
    """Crée une carte interactive des parcs nationaux avec dates de création"""
    m = folium.Map(location=[0, 20], zoom_start=4)
    
    dates = df['creation_date'].dropna()
    min_year = dates.dt.year.min()
    max_year = dates.dt.year.max()
    
    for idx, row in df.iterrows():
        if pd.isna(row['creation_date']):
            color = 'gray'
        else:
            year = row['creation_date'].year
            intensity = (year - min_year) / (max_year - min_year)
            color = 'green' if intensity > 0.5 else 'orange'
        
        creation_info = f"<br>Date de création: {row['creation_date'].strftime('%Y-%m-%d')}" if pd.notna(row['creation_date']) else ""
        
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"{row['park']}<br>{row['country']}{creation_info}<br>{row['description'][:200]}...",
            icon=folium.Icon(color=color)
        ).add_to(m)
    
    return m



# ------------------------------------------fonction principale pour l'éxécution-------------------------------------------------
def main():
    print("Récupération des données...")
    df = get_parks_ecosystem_data()

    # Création de l'histogramme
    print("Création de l'histogramme...")
    plt = create_parks_distribution(df)
    plt.savefig('distribution_parcs.png', bbox_inches='tight')

    print("Création des analyses temporelles...")
    plt = create_temporal_analysis(df)
    plt.savefig('analyse_temporelle_parcs.png', bbox_inches='tight')
    
    print("\nCréation des analyses écosystémiques...")
    plt = analyze_ecosystem_indicators(df)
    plt.savefig('analyse_ecosystemes.png', bbox_inches='tight')
    
    print("Création de la carte...")
    map_parks = create_parks_map(df)
    map_parks.save('parcs_nationaux_afrique.html')
    
    print("\nStatistiques sur les parcs :")
    print(f"Nombre total de parcs : {len(df)}")
    print(f"Nombre de pays : {df['country'].nunique()}")
    print(f"Superficie totale protégée : {df['area_km2'].sum():,.0f} km²")
    print(f"Superficie moyenne des parcs : {df['area_km2'].mean():,.0f} km²")
    print("\nTop 5 des pays avec le plus de parcs :")
    print(df['country'].value_counts().head())    
    print("\nTop 5 des plus grands parcs :")
    print(df.nlargest(5, 'area_km2')[['park', 'country', 'area_km2']])



    print("\nStatistiques temporelles :")
    df_with_dates = df.dropna(subset=['creation_date'])
    print(f"Nombre de parcs avec dates connues : {len(df_with_dates)}")
    
    oldest_park = df_with_dates.loc[df_with_dates['creation_date'].idxmin()]
    newest_park = df_with_dates.loc[df_with_dates['creation_date'].idxmax()]
    
    print(f"Plus ancien parc : {oldest_park['park']} ({oldest_park['creation_date'].strftime('%Y-%m-%d')})")
    print(f"Parc le plus récent : {newest_park['park']} ({newest_park['creation_date'].strftime('%Y-%m-%d')})")
    
    print("\nDistribution par décennie :")
    decade_counts = (df_with_dates['creation_date'].dt.year // 10 * 10).value_counts().sort_index()
    print(decade_counts)
    
    if not df['biome'].isna().all():
        print("\nDistribution des biomes :")
        print(df['biome'].value_counts())

if __name__ == "__main__":
    main()