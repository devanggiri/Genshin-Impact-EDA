import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset with caching
@st.cache_data
def load_data():
    df = pd.read_csv("genshin_characters_v1.csv")
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["release_date"])
    df["release_year"] = df["release_date"].dt.year
    df["star_rarity"] = df["star_rarity"].astype(str)
    return df

genshin = load_data()

# Define category lists
elements = ["Cryo", "Pyro", "Electro", "Hydro", "Anemo", "Geo", "Dendro"]
regions = ["Mondstadt", "Liyue", "Inazuma", "Sumeru", "Fontaine", "Snezhnaya"]
weapons = ["Sword", "Bow", "Catalyst", "Polearm", "Claymore"]
rarity_colors = ['#9565DC', '#F2B145']

# Streamlit UI
st.title("Genshin Impact Character Analysis")
# Add an image below the title
st.image("genshin.png")
st.markdown("Let's enter the world of Tevyat")
st.write(" ")
st.write(" ")

# Sidebar filter
st.sidebar.header("Filters")
selected_plot = st.sidebar.selectbox("Select Visualization", [
    "Number of Characters by Rarity",
    "Total Characters Released Per Year",
    "Character Count by Region",
    "Character Count by Vision",
    "Character Count by Weapon",
    "Star Rarity Distribution Across Regions",
    "Vision Distribution Across Regions",
    "Weapon Type Distribution Across Regions",
    "Character Model Type Distribution"
])

# Visualization Logic
fig, ax = plt.subplots(figsize=(8, 5))

if selected_plot == "Number of Characters by Rarity":
    fourStars = genshin[genshin['star_rarity'] == "4"]
    fiveStars = genshin[genshin['star_rarity'] == "5"]
    ax.bar(["4 Stars", "5 Stars"], [len(fourStars), len(fiveStars)], color=rarity_colors)
    ax.set_title("Number of Characters by Rarity")
    ax.set_xlabel("Rarity")
    ax.set_ylabel("Character Count")

elif selected_plot == "Total Characters Released Per Year":
    yearly_counts = genshin["release_year"].value_counts().sort_index()
    ax.bar(yearly_counts.index.astype(str), yearly_counts.values, color="skyblue", edgecolor="black")
    ax.set_title("Total Characters Released per Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Character Count")
    ax.set_xticklabels(yearly_counts.index, rotation=45)

elif selected_plot == "Character Count by Region":
    regionCount = [len(genshin[genshin['region'] == region]) for region in regions]
    ax.pie(regionCount, labels=regions, autopct='%1.1f%%', startangle=10)
    ax.set_title("Character Count per Region")

elif selected_plot == "Character Count by Vision":
    visionCount = genshin["vision"].value_counts()
    elements = ["Cryo", "Pyro", "Electro", "Hydro", "Anemo", "Geo", "Dendro"]
    element_colors = ('#33E0FF', '#FF7133', '#7B45F9', '#1480F3', '#5FE9DD', '#F3C127', '#B1DE26')
    
    ax.bar(elements, visionCount.reindex(elements, fill_value=0), color=element_colors)
    ax.set_title("Range of Characters per Element")
    ax.set_xlabel("Element")
    ax.set_ylabel("Character Count")

elif selected_plot == "Character Count by Weapon":
    weaponCount = genshin["weapon_type"].value_counts()
    weapons = ['Sword', 'Claymore', 'Polearm', 'Bow', 'Catalyst'] # Ensure weapons are in the desired order
    weapon_colors = ('#33E0FF', '#FF7133', '#7B45F9', '#1480F3', '#5FE9DD') # Example color choices
    
    ax.bar(weapons, weaponCount.reindex(weapons, fill_value=0), color=weapon_colors)
    ax.set_title("Range of Characters per Weapon")
    ax.set_xlabel("Weapon")
    ax.set_ylabel("Character Count")

elif selected_plot == "Star Rarity Distribution Across Regions":
    star_rarity_distribution = genshin.groupby('region')['star_rarity'].value_counts().unstack().fillna(0)
    star_rarity_distribution.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Star Rarity Distribution Across All Regions')
    ax.set_xlabel('Region')
    ax.set_ylabel('Number of Characters')

elif selected_plot == "Vision Distribution Across Regions":
    vision_distribution = genshin.groupby('region')['vision'].value_counts().unstack().fillna(0)
    vision_distribution.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Vision Distribution Across All Regions')
    ax.set_xlabel('Region')
    ax.set_ylabel('Number of Characters')

elif selected_plot == "Weapon Type Distribution Across Regions":
    weapon_distribution = genshin.groupby('region')['weapon_type'].value_counts().unstack().fillna(0)
    weapon_distribution.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Weapon Type Distribution Across All Regions')
    ax.set_xlabel('Region')
    ax.set_ylabel('Number of Characters')
    
elif selected_plot == "Character Model Type Distribution":
    bodyTypes = ["Medium Male", "Tall Male", "Medium Female", "Tall Female", "Short Female"]
    bodyTypeCounts = [len(genshin[genshin["model"] == bt]) for bt in bodyTypes]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(bodyTypes, bodyTypeCounts, color=['#1699BF', '#0CB990', '#2F79FB', '#FB382F', '#C9F164'])
    ax.set_title("Range of Characters per Body Type")
    ax.set_xlabel("Character Body Type")
    ax.set_ylabel("Character Count")    
# Display plot
st.pyplot(fig)

# Additional Section: Best Characters Ranked by ATK (Filter by Vision)
st.header("Compare Best Characters' ATK Scaling by Vision")

# Define available elements (Visions)
visions = ["Cryo", "Pyro", "Electro", "Hydro", "Anemo", "Geo", "Dendro"]

# Dropdown to select element/vision
selected_vision = st.selectbox("Select an Element to Compare ATK Scaling", visions)

# Define ascension levels
ascension_levels = ["atk_20_20", "atk_40_40", "atk_60_60", "atk_80_80", "atk_90_90"]

# Function to find best characters based on ATK
def find_best_characters_by_atk(df, vision, ascension_levels):
    filtered_data = df[df["vision"] == vision]  # Filter by Vision (element)
    
    if filtered_data.empty:
        return pd.DataFrame(columns=["character_name"] + ascension_levels)  # Return empty DataFrame if no data
    
    columns = ["character_name"] + ascension_levels
    best_characters = filtered_data[columns]
    best_characters = best_characters.sort_values(by="atk_90_90", ascending=False)  # Sort by highest ATK
    return best_characters

# Get best characters based on selected vision
best_characters = find_best_characters_by_atk(genshin, selected_vision, ascension_levels)

# Check if there are characters to plot
if not best_characters.empty:
    # Plotting Characters' ATK Based on Selected Vision
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        data=best_characters,
        x="character_name",
        y="atk_90_90",
        palette="coolwarm",
        ax=ax
    )
    
    ax.set_title(f"Top {selected_vision} Characters Ranked by Base ATK at Level 90")
    ax.set_xlabel("Character")
    ax.set_ylabel("Base ATK at Level 90")
    ax.set_xticks(range(len(best_characters)))  # Ensure x-axis ticks match character count
    ax.set_xticklabels(best_characters["character_name"], rotation=45, ha="right")  # Fix missing x-labels
    
    st.pyplot(fig)
else:
    st.write(f"No characters found for {selected_vision}. Try another element!")

# New Section: Interactive Filters for Character Insights
st.sidebar.header("Filter Characters")

# Dropdown filters for Vision and Weapon Type
selected_vision = st.sidebar.selectbox("Select Element (Vision)", genshin["vision"].dropna().unique())
selected_weapon = st.sidebar.selectbox("Select Weapon Type", genshin["weapon_type"].dropna().unique())

# Star Rarity Filter (4★ or 5★)
selected_rarity = st.sidebar.radio("Select Star Rarity", ["All", "4★", "5★"])

# Filter dataset based on selections
filtered_genshin = genshin[(genshin["vision"] == selected_vision) & (genshin["weapon_type"] == selected_weapon)]

if selected_rarity == "4★":
    filtered_genshin = filtered_genshin[filtered_genshin["star_rarity"] == 4]
elif selected_rarity == "5★":
    filtered_genshin = filtered_genshin[filtered_genshin["star_rarity"] == 5]

st.subheader(f"Characters with {selected_vision} Vision and {selected_weapon}")

# Show filtered data
st.dataframe(filtered_genshin[["character_name", "star_rarity", "region", "birthday"]])

# Bar Chart: Number of Characters by Region
st.subheader("Distribution of Characters by Region")
fig, ax = plt.subplots(figsize=(8, 4))
region_counts = filtered_genshin["region"].value_counts()
ax.bar(region_counts.index, region_counts.values, color=['#FF5733', '#33A2FF', '#33FF57', '#FF33A8', '#A833FF'])
ax.set_xlabel("Region")
ax.set_ylabel("Number of Characters")
ax.set_title(f"Character Count in Each Region ({selected_vision} & {selected_weapon})")
st.pyplot(fig)

# Displaying Ascension and Talent Materials
st.subheader("Ascension & Talent Materials Insights")

# Ascension Specialty
st.write("### **Ascension Specialty**")
st.write(filtered_genshin[["character_name", "ascension_specialty"]])

# Ascension Boss Material
st.write("### **Ascension Boss Material**")
st.write(filtered_genshin[["character_name", "ascension_boss_material"]])

# Ascension Gems
st.write("### **Ascension Gems Required**")
st.write(filtered_genshin[["character_name", "ascension_gem_0-1"]])

# Talent Materials
st.write("### **Talent Materials Required**")
st.write(filtered_genshin[["character_name", "talent_material_1-2", "talent_weekly"]])

# Bar Chart: Most Used Ascension Materials
st.subheader("Most Used Ascension Boss Materials")
ascension_counts = filtered_genshin["ascension_boss_material"].value_counts().head(5)
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(ascension_counts.index, ascension_counts.values, color=['#FFA500', '#008080', '#FF4500', '#6A5ACD', '#2E8B57'])
ax.set_xlabel("Ascension Boss Material")
ax.set_ylabel("Count")
ax.set_title(f"Top 5 Ascension Boss Materials for {selected_vision} & {selected_weapon}")
st.pyplot(fig)

# Checkbox: Show Character Birthdays
if st.sidebar.checkbox("Show Character Birthdays"):
    st.subheader("Character Birthdays")
    st.write(filtered_genshin[["character_name", "birthday"]])

st.success("✅ Explore different characters by changing the filters in the sidebar!")
