import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Android Games Analytics",
    page_icon="🎮",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

FILE_PATH = "data/processed/cleaned_data.csv"

try:
    df = pd.read_csv(FILE_PATH)

except FileNotFoundError:
    st.error(
        "❌ cleaned_data.csv was not found."
    )
    st.info(
        "Make sure it is inside: data/processed/"
    )
    st.stop()


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)


# ============================================================
# TITLE
# ============================================================

st.title("🎮 Android Games Analytics Dashboard")

st.markdown(
    """
    **Interactive dashboard for Android game data**

    Explore games by genre, developer, monetization,
    advertising, multiplayer support, age rating,
    engine, platform and country.
    """
)

st.divider()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🎛️ Game Filters")

filtered_df = df.copy()


# ------------------------------------------------------------
# GENRE
# ------------------------------------------------------------

if "genre" in filtered_df.columns:

    genre_values = sorted(
        filtered_df["genre"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_genres = st.sidebar.multiselect(
        "🎮 Genre",
        genre_values,
        default=genre_values
    )

    if selected_genres:

        filtered_df = filtered_df[
            filtered_df["genre"]
            .astype(str)
            .isin(selected_genres)
        ]


# ------------------------------------------------------------
# SUB GENRE
# ------------------------------------------------------------

if "sub_genre" in filtered_df.columns:

    subgenre_values = sorted(
        filtered_df["sub_genre"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_subgenres = st.sidebar.multiselect(
        "🎯 Sub Genre",
        subgenre_values
    )

    if selected_subgenres:

        filtered_df = filtered_df[
            filtered_df["sub_genre"]
            .astype(str)
            .isin(selected_subgenres)
        ]


# ------------------------------------------------------------
# MONETIZATION
# ------------------------------------------------------------

if "monetization_model" in filtered_df.columns:

    monetization_values = sorted(
        filtered_df["monetization_model"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_monetization = st.sidebar.multiselect(
        "💰 Monetization Model",
        monetization_values,
        default=monetization_values
    )

    if selected_monetization:

        filtered_df = filtered_df[
            filtered_df["monetization_model"]
            .astype(str)
            .isin(selected_monetization)
        ]


# ------------------------------------------------------------
# ADS
# ------------------------------------------------------------

if "contains_ads" in filtered_df.columns:

    ads_values = sorted(
        filtered_df["contains_ads"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_ads = st.sidebar.multiselect(
        "📢 Contains Ads",
        ads_values,
        default=ads_values
    )

    if selected_ads:

        filtered_df = filtered_df[
            filtered_df["contains_ads"]
            .astype(str)
            .isin(selected_ads)
        ]


# ------------------------------------------------------------
# IN-APP PURCHASE
# ------------------------------------------------------------

if "has_in_app_purchases" in filtered_df.columns:

    iap_values = sorted(
        filtered_df["has_in_app_purchases"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_iap = st.sidebar.multiselect(
        "🛒 In-App Purchases",
        iap_values,
        default=iap_values
    )

    if selected_iap:

        filtered_df = filtered_df[
            filtered_df["has_in_app_purchases"]
            .astype(str)
            .isin(selected_iap)
        ]


# ------------------------------------------------------------
# MULTIPLAYER
# ------------------------------------------------------------

if "multiplayer_support" in filtered_df.columns:

    multiplayer_values = sorted(
        filtered_df["multiplayer_support"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_multiplayer = st.sidebar.multiselect(
        "🌐 Multiplayer",
        multiplayer_values,
        default=multiplayer_values
    )

    if selected_multiplayer:

        filtered_df = filtered_df[
            filtered_df["multiplayer_support"]
            .astype(str)
            .isin(selected_multiplayer)
        ]


# ------------------------------------------------------------
# AGE RATING
# ------------------------------------------------------------

if "age_rating" in filtered_df.columns:

    age_values = sorted(
        filtered_df["age_rating"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_age = st.sidebar.multiselect(
        "🔞 Age Rating",
        age_values,
        default=age_values
    )

    if selected_age:

        filtered_df = filtered_df[
            filtered_df["age_rating"]
            .astype(str)
            .isin(selected_age)
        ]


# ------------------------------------------------------------
# ENGINE
# ------------------------------------------------------------

if "engine_used" in filtered_df.columns:

    engine_values = sorted(
        filtered_df["engine_used"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_engine = st.sidebar.multiselect(
        "⚙️ Game Engine",
        engine_values
    )

    if selected_engine:

        filtered_df = filtered_df[
            filtered_df["engine_used"]
            .astype(str)
            .isin(selected_engine)
        ]


# ------------------------------------------------------------
# COUNTRY
# ------------------------------------------------------------

if "country_code_primary" in filtered_df.columns:

    country_values = sorted(
        filtered_df["country_code_primary"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_country = st.sidebar.multiselect(
        "🌍 Country",
        country_values
    )

    if selected_country:

        filtered_df = filtered_df[
            filtered_df["country_code_primary"]
            .astype(str)
            .isin(selected_country)
        ]


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 Key Statistics")

col1, col2, col3, col4 = st.columns(4)


# Total games

with col1:

    st.metric(
        "🎮 Total Games",
        f"{len(filtered_df):,}"
    )


# Developers

with col2:

    if "developer_name" in filtered_df.columns:

        developers = filtered_df[
            "developer_name"
        ].nunique()

        st.metric(
            "👨‍💻 Developers",
            f"{developers:,}"
        )


# Genres

with col3:

    if "genre" in filtered_df.columns:

        genres = filtered_df[
            "genre"
        ].nunique()

        st.metric(
            "🎯 Genres",
            f"{genres:,}"
        )


# Countries

with col4:

    if "country_code_primary" in filtered_df.columns:

        countries = filtered_df[
            "country_code_primary"
        ].nunique()

        st.metric(
            "🌍 Countries",
            f"{countries:,}"
        )


st.divider()


# ============================================================
# CHART 1
# GAMES BY GENRE
# ============================================================

st.subheader("🎮 Games by Genre")

if "genre" in filtered_df.columns:

    genre_count = (
        filtered_df["genre"]
        .value_counts()
        .reset_index()
    )

    genre_count.columns = [
        "Genre",
        "Games"
    ]

    fig = px.bar(
        genre_count,
        x="Genre",
        y="Games",
        title="Number of Games by Genre",
        text="Games"
    )

    fig.update_layout(
        height=500,
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CHART 2
# SUB GENRE
# ============================================================

st.subheader("🎯 Sub-Genre Distribution")

if "sub_genre" in filtered_df.columns:

    subgenre_count = (
        filtered_df["sub_genre"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    subgenre_count.columns = [
        "Sub Genre",
        "Games"
    ]

    fig = px.bar(
        subgenre_count,
        x="Games",
        y="Sub Genre",
        orientation="h",
        title="Top Sub-Genres"
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CHART 3
# MONETIZATION PIE
# ============================================================

st.subheader("💰 Monetization Model")

if "monetization_model" in filtered_df.columns:

    monetization = (
        filtered_df["monetization_model"]
        .value_counts()
        .reset_index()
    )

    monetization.columns = [
        "Model",
        "Games"
    ]

    fig = px.pie(
        monetization,
        names="Model",
        values="Games",
        hole=0.4,
        title="Monetization Model Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CHART 4
# ADS
# ============================================================

st.subheader("📢 Games Containing Advertisements")

if "contains_ads" in filtered_df.columns:

    ads = (
        filtered_df["contains_ads"]
        .value_counts()
        .reset_index()
    )

    ads.columns = [
        "Contains Ads",
        "Games"
    ]

    fig = px.pie(
        ads,
        names="Contains Ads",
        values="Games",
        title="Games With vs Without Ads"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CHART 5
# IN-APP PURCHASES
# ============================================================

st.subheader("🛒 In-App Purchases")

if "has_in_app_purchases" in filtered_df.columns:

    iap = (
        filtered_df["has_in_app_purchases"]
        .value_counts()
        .reset_index()
    )

    iap.columns = [
        "In-App Purchases",
        "Games"
    ]

    fig = px.bar(
        iap,
        x="In-App Purchases",
        y="Games",
        title="Games With vs Without In-App Purchases",
        text="Games"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CHART 6
# MULTIPLAYER
# ============================================================

st.subheader("🌐 Multiplayer Support")

if "multiplayer_support" in filtered_df.columns:

    multiplayer = (
        filtered_df["multiplayer_support"]
        .value_counts()
        .reset_index()
    )

    multiplayer.columns = [
        "Multiplayer",
        "Games"
    ]

    fig = px.pie(
        multiplayer,
        names="Multiplayer",
        values="Games",
        hole=0.4,
        title="Multiplayer Support"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CHART 7
# AGE RATING
# ============================================================

st.subheader("🔞 Age Rating Distribution")

if "age_rating" in filtered_df.columns:

    age = (
        filtered_df["age_rating"]
        .value_counts()
        .reset_index()
    )

    age.columns = [
        "Age Rating",
        "Games"
    ]

    fig = px.bar(
        age,
        x="Age Rating",
        y="Games",
        title="Games by Age Rating",
        text="Games"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CHART 8
# GAME ENGINE
# ============================================================

st.subheader("⚙️ Game Engine Usage")

if "engine_used" in filtered_df.columns:

    engines = (
        filtered_df["engine_used"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    engines.columns = [
        "Engine",
        "Games"
    ]

    fig = px.bar(
        engines,
        x="Engine",
        y="Games",
        title="Top Game Engines",
        text="Games"
    )

    fig.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CHART 9
# ART STYLE
# ============================================================

st.subheader("🎨 Art Style Distribution")

if "art_style" in filtered_df.columns:

    art = (
        filtered_df["art_style"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    art.columns = [
        "Art Style",
        "Games"
    ]

    fig = px.bar(
        art,
        x="Games",
        y="Art Style",
        orientation="h",
        title="Popular Art Styles"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CHART 10
# PUBLISHER TIER
# ============================================================

st.subheader("🏢 Publisher Tier")

if "publisher_tier" in filtered_df.columns:

    publisher = (
        filtered_df["publisher_tier"]
        .value_counts()
        .reset_index()
    )

    publisher.columns = [
        "Publisher Tier",
        "Games"
    ]

    fig = px.pie(
        publisher,
        names="Publisher Tier",
        values="Games",
        hole=0.35,
        title="Games by Publisher Tier"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CHART 11
# REGION
# ============================================================

st.subheader("🌍 Games by Country")

if "country_code_primary" in filtered_df.columns:

    country = (
        filtered_df["country_code_primary"]
        .value_counts()
        .head(20)
        .reset_index()
    )

    country.columns = [
        "Country",
        "Games"
    ]

    fig = px.bar(
        country,
        x="Games",
        y="Country",
        orientation="h",
        title="Top Countries by Number of Games"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# DEVELOPER ANALYSIS
# ============================================================

st.subheader("👨‍💻 Top Developers")

if "developer_name" in filtered_df.columns:

    developers = (
        filtered_df["developer_name"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    developers.columns = [
        "Developer",
        "Games"
    ]

    fig = px.bar(
        developers,
        x="Games",
        y="Developer",
        orientation="h",
        title="Developers with Most Games"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# DATA TABLE
# ============================================================

st.subheader("📋 Filtered Android Games")

st.write(
    f"Showing **{len(filtered_df):,} games** "
    "after applying the selected filters."
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=450
)


# ============================================================
# DOWNLOAD
# ============================================================

csv = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "⬇️ Download Filtered Data",
    csv,
    "filtered_android_games.csv",
    "text/csv"
)


st.divider()

st.success(
    "🎮 Android Games Dashboard loaded successfully!"
)