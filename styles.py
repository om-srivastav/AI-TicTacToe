CUSTOM_CSS = """
<style>

/* Remove top blank space */
.block-container{
    padding-top:0.8rem;
    padding-bottom:2rem;
}

/* Transparent Streamlit Header */
header[data-testid="stHeader"]{
    background:transparent;
}

/* Better Buttons */
.stButton>button{
    height:95px;
    font-size:32px;
    font-weight:bold;
    border-radius:16px;
}

/* Score Cards */
div[data-testid="stMetric"]{
    border-radius:12px;
    padding:10px;
}

</style>
"""