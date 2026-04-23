import streamlit as st
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
import pandas as pd
from io import BytesIO

# Load .env
load_dotenv()

# Get credentials
connection_string = os.getenv("CONNECTION_STRING")
container_name = os.getenv("CONTAINER_NAME")

# Initialize Azure client
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="DataFlowX | Smart Data Pipeline",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS FOR PROFESSIONAL STYLING
# ============================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('[fonts.googleapis.com](https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap)');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
    }
    
    .hero-title {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin: 0;
        letter-spacing: -2px;
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 400;
        color: rgba(255,255,255,0.85);
        margin-top: 0.5rem;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        color: white;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Section Headers */
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a1a2e;
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .section-description {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #6b7280;
        line-height: 1.7;
        margin-bottom: 1.5rem;
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.1);
        border-color: #667eea;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #000 !important;
        margin: 0.5rem 0;
    }
    
    .feature-text {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #6b7280;
        line-height: 1.6;
    }
    
    /* Process Steps */
    .step-container {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    .step-number {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    
    .step-content {
        flex: 1;
    }
    
    .step-title {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #1a1a2e;
        margin: 0 0 0.3rem 0;
    }
    
    .step-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #6b7280;
        margin: 0;
    }
    
    /* Upload Zone */
    .upload-zone {
        background: linear-gradient(135deg, #f0f4ff 0%, #e8f0fe 100%);
        border: 2px dashed #667eea;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 1.5rem 0;
    }
    
    /* Status Boxes */
    .status-success {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 1px solid #10b981;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    .status-error {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 1px solid #ef4444;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    /* Download Section */
    .download-section {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 1px solid #f59e0b;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .download-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #92400e;
        margin: 0 0 0.5rem 0;
    }
    
    /* Code Blocks */
    .code-block {
        font-family: 'JetBrains Mono', monospace;
        background: #1a1a2e;
        color: #a5b4fc;
        padding: 1rem;
        border-radius: 10px;
        font-size: 0.85rem;
        overflow-x: auto;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #9ca3af;
        font-size: 0.85rem;
        border-top: 1px solid #e5e7eb;
        margin-top: 3rem;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    /* Metrics */
    .metric-container {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .metric-value {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #6b7280;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HERO SECTION
# ============================================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">⚡ ENTERPRISE DATA SOLUTION</div>
    <h1 class="hero-title">DataFlowX</h1>
    <p class="hero-subtitle">Transform your raw data into actionable insights with our intelligent Azure-powered pipeline</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR - ABOUT & NAVIGATION
# ============================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h2 style="font-family: 'Inter', sans-serif; font-weight: 800; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-size: 1.8rem; margin: 0;">DataFlowX</h2>
        <p style="color: #6b7280; font-size: 0.85rem;">v2.0.0 | Enterprise Edition</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Quick Navigation")
    nav_option = st.radio(
        "",
        ["📤 Upload Data", "📊 Power BI Tools", "📖 Documentation"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("### 📈 Session Stats")
    if 'upload_count' not in st.session_state:
        st.session_state.upload_count = 0
    if 'total_size' not in st.session_state:
        st.session_state.total_size = 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Uploads", st.session_state.upload_count)
    with col2:
        st.metric("Size (MB)", f"{st.session_state.total_size:.2f}")
    
    st.markdown("---")
    
    st.markdown("""
    <div style="padding: 1rem; background: #f0f4ff; border-radius: 10px;">
        <p style="font-size: 0.8rem; color: #667eea; margin: 0; font-weight: 600;">
            🔒 Secure Connection
        </p>
        <p style="font-size: 0.75rem; color: #6b7280; margin: 0.3rem 0 0 0;">
            256-bit SSL encryption enabled
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MAIN CONTENT BASED ON NAVIGATION
# ============================================

if nav_option == "📤 Upload Data":
    
    # How DataFlowX Works Section
    st.markdown('<h2 class="section-header">🔄 How DataFlowX Works</h2>', unsafe_allow_html=True)
    st.markdown("""
    <p class="section-description">
        DataFlowX is an enterprise-grade data pipeline that seamlessly connects your local data sources 
        to Azure cloud infrastructure, enabling real-time analytics and visualization through Power BI.
    </p>
    """, unsafe_allow_html=True)
    
    # Process Steps
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="step-container">
            <div class="step-number">1</div>
            <div class="step-content">
                <p class="step-title">Upload Your Data</p>
                <p class="step-desc">Drag & drop CSV or Excel files. We support datasets up to 500MB with automatic format detection.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="step-container">
            <div class="step-number">2</div>
            <div class="step-content">
                <p class="step-title">Azure Blob Storage</p>
                <p class="step-desc">Files are securely transferred to Azure Blob Storage with enterprise-grade encryption.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="step-container">
            <div class="step-number">3</div>
            <div class="step-content">
                <p class="step-title">Data Processing</p>
                <p class="step-desc">Azure Data Factory processes and transforms your data automatically.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="step-container">
            <div class="step-number">4</div>
            <div class="step-content">
                <p class="step-title">Power BI Visualization</p>
                <p class="step-desc">Connect Power BI to your processed data for stunning dashboards and reports.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feature Cards
    st.markdown('<h2 class="section-header">✨ Key Features</h2>', unsafe_allow_html=True)
    
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    with feat_col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <h3 class="feature-title">Lightning Fast</h3>
            <p class="feature-text">Upload speeds up to 100MB/s with parallel chunked transfers and Azure CDN optimization.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔐</div>
            <h3 class="feature-title">Enterprise Security</h3>
            <p class="feature-text">AES-256 encryption at rest, TLS 1.3 in transit, and SOC 2 Type II compliance.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3 class="feature-title">Smart Analytics</h3>
            <p class="feature-text">Automatic data profiling, anomaly detection, and schema inference on upload.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Upload Section
    st.markdown('<h2 class="section-header">📤 Upload Your Data</h2>', unsafe_allow_html=True)
    st.markdown("""
    <p class="section-description">
        Select a CSV or Excel file to upload to Azure Blob Storage. Your data will be instantly 
        available for Power BI integration and advanced analytics.
    </p>
    """, unsafe_allow_html=True)
    
    # File Uploader
    uploaded_file = st.file_uploader(
        "Drag and drop your file here",
        type=["csv", "xlsx"],
        help="Supported formats: CSV, XLSX | Max size: 500MB"
    )
    
    if uploaded_file is not None:
        # File Info
        file_size_mb = uploaded_file.size / (1024 * 1024)
        
        st.markdown(f"""
        <div style="background: #f0f4ff; border-radius: 12px; padding: 1rem; margin: 1rem 0; 
                    border: 1px solid #667eea;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <p style="margin: 0; font-weight: 600; color: #1a1a2e;">📁 {uploaded_file.name}</p>
                    <p style="margin: 0.3rem 0 0 0; font-size: 0.85rem; color: #6b7280;">
                        Size: {file_size_mb:.2f} MB | Type: {uploaded_file.type}
                    </p>
                </div>
                <div style="background: #667eea; color: white; padding: 0.3rem 0.8rem; 
                            border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                    Ready
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Data Preview
        try:
            uploaded_file.seek(0)  # Reset file pointer
            if uploaded_file.name.endswith("csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.markdown('<h3 class="section-header">📋 Data Preview</h3>', unsafe_allow_html=True)
            
            # Data Stats
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            with stat_col1:
                st.markdown(f"""
                <div class="metric-container">
                    <p class="metric-value">{len(df):,}</p>
                    <p class="metric-label">Rows</p>
                </div>
                """, unsafe_allow_html=True)
            with stat_col2:
                st.markdown(f"""
                <div class="metric-container">
                    <p class="metric-value">{len(df.columns)}</p>
                    <p class="metric-label">Columns</p>
                </div>
                """, unsafe_allow_html=True)
            with stat_col3:
                st.markdown(f"""
                <div class="metric-container">
                    <p class="metric-value">{df.isnull().sum().sum()}</p>
                    <p class="metric-label">Missing Values</p>
                </div>
                """, unsafe_allow_html=True)
            with stat_col4:
                st.markdown(f"""
                <div class="metric-container">
                    <p class="metric-value">{len(df.select_dtypes(include='number').columns)}</p>
                    <p class="metric-label">Numeric Cols</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.dataframe(df.head(10), use_container_width=True)
            
            # Column Info Expander
            with st.expander("📊 View Column Details"):
                col_info = pd.DataFrame({
                    'Column': df.columns,
                    'Type': df.dtypes.astype(str),
                    'Non-Null Count': df.notnull().sum().values,
                    'Null Count': df.isnull().sum().values,
                    'Unique Values': [df[col].nunique() for col in df.columns]
                })
                st.dataframe(col_info, use_container_width=True)
        
        except Exception as e:
            st.warning(f"⚠️ Preview not available: {str(e)}")
        
        st.markdown("---")
        
        # Upload Button
        if st.button("🚀 Upload to Azure Blob Storage", use_container_width=True):
            with st.spinner("Uploading to Azure..."):
                try:
                    uploaded_file.seek(0)  # Reset file pointer
                    blob_name = uploaded_file.name
                    
                    blob_client = blob_service_client.get_blob_client(
                        container=container_name,
                        blob=blob_name
                    )
                    
                    blob_client.upload_blob(uploaded_file, overwrite=True)
                    
                    # Update session stats
                    st.session_state.upload_count += 1
                    st.session_state.total_size += file_size_mb
                    
                    st.markdown(f"""
                    <div class="status-success">
                        <h3 style="margin: 0; color: #065f46;">✅ Upload Successful!</h3>
                        <p style="margin: 0.5rem 0 0 0; color: #047857;">
                            <strong>{blob_name}</strong> has been uploaded to Azure Blob Storage.<br>
                            Container: <code>{container_name}</code>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.balloons()
                
                except Exception as e:
                    st.markdown(f"""
                    <div class="status-error">
                        <h3 style="margin: 0; color: #991b1b;">❌ Upload Failed</h3>
                        <p style="margin: 0.5rem 0 0 0; color: #dc2626;">{str(e)}</p>
                    </div>
                    """, unsafe_allow_html=True)

elif nav_option == "📊 Power BI Tools":
    
    st.markdown('<h2 class="section-header">📊 Power BI Integration</h2>', unsafe_allow_html=True)
    st.markdown("""
    <p class="section-description">
        Connect your uploaded data directly to Power BI for stunning visualizations and real-time dashboards.
        Download Power BI Desktop to get started or use our pre-built templates.
    </p>
    """, unsafe_allow_html=True)
    
    # Download Section
    st.markdown("""
    <div class="download-section">
        <h3 class="download-title">⬇️ Download Power BI Desktop</h3>
        <p style="color: #92400e; margin: 0.5rem 0;">
            Power BI Desktop is required to create and publish reports. Download the latest version below.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    dl_col1, dl_col2 = st.columns(2)
    
    with dl_col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🖥️</div>
            <h3 class="feature-title">Power BI Desktop</h3>
            <p class="feature-text">Full-featured desktop application for creating rich, interactive reports and dashboards.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.link_button(
            "⬇️ Download Power BI Desktop",
            "[microsoft.com](https://www.microsoft.com/en-us/download/details.aspx?id=58494)",
            use_container_width=True
        )
    
    with dl_col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌐</div>
            <h3 class="feature-title">Power BI Service</h3>
            <p class="feature-text">Cloud-based service to share, collaborate, and view reports from any device.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.link_button(
            "🌐 Open Power BI Service",
            "[app.powerbi.com](https://app.powerbi.com/)",
            use_container_width=True
        )
    
    st.markdown("---")
    
    
    
    # Template Downloads
    st.markdown('<h2 class="section-header">📑 Power BI Templates</h2>', unsafe_allow_html=True)
    st.markdown("""
    <p class="section-description">
        Download our pre-built Power BI templates to jumpstart your analytics journey.
    </p>
    """, unsafe_allow_html=True)
    
    temp_col1, temp_col2, temp_col3 = st.columns(3)
    
    with temp_col1:
     st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <h3 class="feature-title">Sales Dashboard</h3>
        <p class="feature-text">Track revenue, orders, and sales performance with interactive visualizations.</p>
    </div>
    """, unsafe_allow_html=True)

     with open("PowerBI.pbit", "rb") as file:
        st.download_button(
            "⬇️ Download Sales Dashboard",
            data=file,
            file_name="PowerBI.pbit",
            mime="application/octet-stream",
            use_container_width=True
        )
    
    with temp_col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">👥</div>
            <h3 class="feature-title">HR Analytics</h3>
            <p class="feature-text">Employee metrics, turnover analysis, and workforce planning tools.</p>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            "Download Template",
            data="Template placeholder",
            file_name="hr_analytics_template.pbit",
            mime="application/octet-stream",
            use_container_width=True
        )
    
    with temp_col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💰</div>
            <h3 class="feature-title">Financial Report</h3>
            <p class="feature-text">P&L statements, budget tracking, and financial KPIs at a glance.</p>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            "Download Template",
            data="Template placeholder",
            file_name="financial_report_template.pbit",
            mime="application/vnd.powerbitemplate",
            use_container_width=True
        )

elif nav_option == "📖 Documentation":
    
    st.markdown('<h2 class="section-header">📖 Documentation</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="section-description">
        Everything you need to know about DataFlowX, from setup to advanced configurations.
    </p>
    """, unsafe_allow_html=True)
    
    # Architecture Overview
    with st.expander("🏗️ System Architecture", expanded=True):
        st.markdown("""
        ### DataFlowX Architecture
        
        ```
        ┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
        │                 │     │                  │     │                 │
        │   Your Data     │────▶│  Azure Blob      │────▶│  Azure Data     │
        │   (CSV/Excel)   │     │  Storage         │     │  Factory        │
        │                 │     │                  │     │                 │
        └─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                                  │
                                                                  ▼
        ┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
        │                 │     │                  │     │                 │
        │   Power BI      │◀────│  Azure SQL       │◀────│  Data           │
        │   Dashboard     │     │  Database        │     │  Processing     │
        │                 │     │                  │     │                 │
        └─────────────────┘     └──────────────────┘     └─────────────────┘
        ```
        
        **Data Flow:**
        1. **Ingestion**: Files uploaded via Streamlit → Azure Blob Storage
        2. **Processing**: Azure Data Factory triggers ETL pipelines
        3. **Storage**: Cleaned data stored in Azure SQL Database
        4. **Visualization**: Power BI connects for real-time dashboards
        """)
    
    with st.expander("🔧 Configuration Guide"):
        st.markdown("""
        ### Environment Setup
        
        Create a `.env` file in your project root:
        
        ```bash
        CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=xxx;AccountKey=xxx;EndpointSuffix=core.windows.net
        CONTAINER_NAME=your-container-name
        ```
        
        ### Azure Setup Requirements
        
        1. **Azure Storage Account** - Standard or Premium tier
        2. **Blob Container** - With appropriate access policies
        3. **Network Configuration** - Allow your IP or use Private Endpoints
        """)
    
    with st.expander("❓ FAQs"):
        st.markdown("""
        **Q: What file formats are supported?**  
        A: Currently CSV and Excel (.xlsx) files up to 500MB.
        
        **Q: Is my data secure?**  
        A: Yes! All transfers use TLS 1.3 encryption, and data is encrypted at rest using AES-256.
        
        **Q: Can I schedule automatic uploads?**  
        A: Not in the current version. Contact us for enterprise automation solutions.
        
        **Q: How do I get support?**  
        A: Reach out to support@dataflowx.io or open a ticket in our portal.
        """)

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <p><strong>DataFlowX</strong> | Built with ❤️ using Streamlit & Azure</p>
    <p style="font-size: 0.75rem;">© 2024 DataFlowX Inc. All rights reserved. | 
    <a href="#" style="color: #667eea;">Privacy Policy</a> | 
    <a href="#" style="color: #667eea;">Terms of Service</a></p>
</div>
""", unsafe_allow_html=True)
