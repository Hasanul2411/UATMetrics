import streamlit as st
import os

# Ultimate Studio Visual Tokens - Neon Theme
STUDIO_COLORS = {
    "cyan": "#22d3ee",    # Cyan 400
    "indigo": "#6366f1",  # Indigo 500
    "emerald": "#10b981", # Emerald 500
    "amber": "#f59e0b",   # Amber 500
    "rose": "#f43f5e",    # Rose 500
    "slate_light": "#f8fafc",
    "slate_muted": "#94a3b8",
    "border": "#334155"
}

def get_studio_logo_svg():
    """Return an inline SVG logo for the studio."""
    # Compacted to single line to prevent Markdown parsing issues
    return f'<div style="display:flex; align-items:center;"><svg width="80" height="80" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="100" rx="16" fill="#1e293b"/><path d="M25 75L40 50L55 65L75 25" stroke="{STUDIO_COLORS['cyan']}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><circle cx="75" cy="25" r="5" fill="{STUDIO_COLORS['indigo']}"/></svg></div>'

def inject_custom_css():
    """Inject custom CSS for global styling."""
    st.markdown("""
    <style>
        /* Import Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
        
        :root {
            /* Ultimate Studio Palette - Dark Mode */
            --studio-bg: #0f172a;           /* Deep Slate Workspace */
            --studio-card: #1e293b;         /* Charcoal Primary Surface */
            --studio-sidebar: #0b0f19;      /* Pure Dark Sidebar */
            --studio-border: #334155;       /* Slate-700 Border */
            
            /* High Contrast Typography */
            --text-heading: #f8fafc;        /* Slate-50 White */
            --text-body: #cbd5e1;           /* Slate-300 readable Gray */
            --text-muted: #94a3b8;          /* Slate-400 */
            
            /* Vibrant Accents */
            --brand-primary: #6366f1;       /* Indigo 500 */
            --brand-glow: rgba(99, 102, 241, 0.15);
            --brand-cyan: #22d3ee;          /* Cyan 400 */
            --brand-cyan-glow: rgba(34, 211, 238, 0.1);
        }

        /* Global Defaults */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: var(--studio-bg) !important;
            color: var(--text-body);
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 5rem;
            max-width: 1200px;
        }

        /* Typography */
        h1, h2, h3, h4 {
            color: var(--text-heading);
            font-weight: 800 !important;
            letter-spacing: -0.04em !important;
        }
        
        h1 {
            font-size: 2.75rem !important;
            background: linear-gradient(to right, #f8fafc, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem !important;
        }

        /* Standard Studio Cards */
        div[data-testid="stMetric"] {
            background-color: var(--studio-card);
            border: 1px solid var(--studio-border);
            border-radius: 16px;
            padding: 24px !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
            transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
        }
        
        div[data-testid="stMetric"]:hover {
            transform: translateY(-4px);
            border-color: var(--brand-primary);
            box-shadow: 0 8px 30px rgba(99, 102, 241, 0.2);
        }
        
        div[data-testid="stMetric"] label {
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-size: 0.8rem;
        }
        
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: var(--brand-cyan) !important;
            font-weight: 900;
            font-size: 2.5rem !important;
            text-shadow: 0 0 20px var(--brand-cyan-glow);
        }

        /* Buttons - High Contrast Studio Style */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, var(--brand-primary) 0%, #4f46e5 100%);
            color: #ffffff;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.1);
            padding: 0.75rem 1.75rem;
            font-weight: 700;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
            transition: all 0.2s;
            text-transform: none;
            width: auto;
        }
        
        div.stButton > button:first-child:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.5);
            border-color: rgba(255,255,255,0.3);
        }

        /* Input Fields */
        div[data-baseweb="input"], div[data-baseweb="select"] {
            background-color: var(--studio-bg) !important;
            border: 1px solid var(--studio-border) !important;
            border-radius: 12px !important;
            color: var(--text-heading) !important;
        }
        
        div[data-baseweb="input"]:focus-within {
            border-color: var(--brand-primary) !important;
            box-shadow: 0 0 0 2px var(--brand-glow) !important;
        }

        /* Hide default Streamlit navigation */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* Sidebar - Elite Navigation */
        section[data-testid="stSidebar"] {
            background-color: var(--studio-sidebar) !important;
            border-right: 1px solid var(--studio-border);
            padding-top: 1rem;
        }
        
        section[data-testid="stSidebar"] [data-testid="stImage"] {
            padding: 0 20px;
            margin-bottom: 0.5rem;
        }

        section[data-testid="stSidebar"] img {
            border-radius: 12px;
            box-shadow: 0 0 20px var(--brand-glow);
        }

        section[data-testid="stSidebar"] .stMarkdown h2 {
            font-size: 1.1rem !important;
            color: var(--text-heading) !important;
            letter-spacing: 0.1em !important;
            text-transform: uppercase;
            font-weight: 900 !important;
            margin-bottom: 2rem !important;
            text-align: center;
        }
        
        /* Sidebar Navigation - Menu List style */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] {
            gap: 8px;
        }

        section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
            background-color: rgba(255, 255, 255, 0.02);
            border: 1px solid transparent;
            border-radius: 12px;
            padding: 12px 16px !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            color: var(--text-muted) !important;
            cursor: pointer;
            width: 100%;
            margin-bottom: 4px;
        }

        section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
            background-color: rgba(99, 102, 241, 0.05);
            border-color: rgba(99, 102, 241, 0.2);
            color: var(--text-heading) !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-selected="true"] {
            background-color: rgba(99, 102, 241, 0.1) !important;
            border-color: var(--brand-primary) !important;
            color: var(--brand-cyan) !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        /* Hide default Streamlit radio radio-circles */
        section[data-testid="stSidebar"] div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {
            font-size: 1rem !important;
            margin-bottom: 0 !important;
        }
        
        div[data-testid="stRadio"] input {
            display: none;
        }

        /* Sidebar Action Buttons (Logout, Admin) */
        section[data-testid="stSidebar"] div.stButton > button {
            background-color: rgba(255, 255, 255, 0.03);
            color: var(--text-muted);
            border: 1px solid var(--studio-border);
            border-radius: 12px;
            padding: 0.6rem 1rem;
            font-weight: 600;
            width: 100%;
            transition: all 0.2s;
            margin-top: 0.5rem;
        }
        
        section[data-testid="stSidebar"] div.stButton > button:hover {
            background-color: #ef444415; /* Tint of red for logout etc */
            color: #ef4444;
            border-color: #ef444440;
        }
        
        /* Specific override for Admin button if needed */
        section[data-testid="stSidebar"] div.stButton:nth-of-type(1) > button:hover {
             background-color: rgba(99, 102, 241, 0.1);
             color: var(--brand-primary);
             border-color: var(--brand-primary);
        }

        /* Tabs - Linear/Vercel Style */
        .stTabs [data-baseweb="tab-list"] {
            background-color: rgba(255,255,255,0.03);
            padding: 6px;
            border-radius: 14px;
            border: 1px solid var(--studio-border);
            margin-bottom: 2rem;
        }

        .stTabs [data-baseweb="tab"] {
            border: none;
            color: var(--text-muted);
            font-weight: 700;
            border-radius: 10px;
            padding: 8px 24px;
            transition: all 0.2s;
        }

        .stTabs [aria-selected="true"] {
            background-color: var(--studio-card);
            color: var(--brand-primary);
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }

        /* Dataframe Branding */
        div[data-testid="stDataFrame"] {
            background-color: var(--studio-card);
            border: 1px solid var(--studio-border);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: var(--shadow-lg);
        }

        /* Success/Error Styling */
        div[data-testid="stNotification"] {
            background-color: var(--studio-card) !important;
            border: 1px solid var(--studio-border) !important;
            border-radius: 12px !important;
            color: var(--text-heading) !important;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--studio-bg);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--studio-border);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-muted);
        }
    </style>
    """, unsafe_allow_html=True)



def get_studio_logo_svg(icon_type="default"):
    """Return an inline SVG logo for the studio based on type."""
    
    # Common styles
    rect_fill = "#1e293b"
    cyan = STUDIO_COLORS['cyan']
    indigo = STUDIO_COLORS['indigo']
    rose = STUDIO_COLORS['rose']
    amber = STUDIO_COLORS['amber']
    emerald = STUDIO_COLORS['emerald']
    
    # SVG Paths for different icons
    paths = {
        "default": f'<path d="M25 75L40 50L55 65L75 25" stroke="{cyan}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><circle cx="75" cy="25" r="5" fill="{indigo}"/>',
        "dashboard": f'<rect x="25" y="45" width="15" height="40" rx="4" fill="{indigo}"/><rect x="45" y="25" width="15" height="60" rx="4" fill="{cyan}"/><rect x="65" y="55" width="15" height="30" rx="4" fill="{emerald}"/>',
        "analytics": f'<path d="M20 80L40 50L60 65L85 20" stroke="{cyan}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><circle cx="85" cy="20" r="6" fill="{amber}"/><path d="M20 80H85" stroke="{indigo}" stroke-width="4" stroke-linecap="round" stroke-opacity="0.3"/>',
        "tracker": f'<circle cx="50" cy="50" r="30" stroke="{rose}" stroke-width="6"/><path d="M35 50L45 60L65 40" stroke="{rose}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>',
        "reports": f'<rect x="30" y="20" width="40" height="60" rx="4" stroke="{cyan}" stroke-width="4" fill="none"/><path d="M40 35H60" stroke="{indigo}" stroke-width="4" stroke-linecap="round"/><path d="M40 50H60" stroke="{indigo}" stroke-width="4" stroke-linecap="round"/><path d="M40 65H50" stroke="{indigo}" stroke-width="4" stroke-linecap="round"/>',
        "login": f'<circle cx="50" cy="40" r="15" stroke="{cyan}" stroke-width="6"/><path d="M50 55V75" stroke="{cyan}" stroke-width="6" stroke-linecap="round"/><rect x="40" y="65" width="20" height="20" rx="4" fill="{indigo}"/>'
    }
    
    selected_content = paths.get(icon_type, paths["default"])
    
    return f'<div style="display:flex; align-items:center;"><svg width="80" height="80" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="100" rx="20" fill="{rect_fill}"/>{selected_content}</svg></div>'


def render_page_header(title, subtitle=None, icon="default"):
    """Render a premium page header with the logo."""
    # Adjusted rendering to use SVG for perfect scalability and avoid white-square artifacts
    col1, col2 = st.columns([0.12, 0.88]) 
    with col1:
        st.markdown(get_studio_logo_svg(icon), unsafe_allow_html=True)
    with col2:
        st.title(title)
        if subtitle:
            # Using HTML for subtitle to ensure tighter spacing and proper color
            st.markdown(f'<p style="color:#94a3b8; font-size: 1.1rem; margin-top:-20px; font-weight: 500;">{subtitle}</p>', unsafe_allow_html=True)


def apply_chart_theme(fig):
    """Apply high-end studio theme to Plotly figures."""
    fig.update_layout(
        template="plotly_dark", # Force dark base template
        font_family="Inter",
        title_font_family="Inter",
        title_font_size=20,
        title_font_color="#f8fafc",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=60, l=20, r=20, b=20),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='#334155',
            gridcolor='rgba(51, 65, 85, 0.2)',
            tickfont=dict(color='#94a3b8', size=11),
            title_font=dict(color='#94a3b8')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(51, 65, 85, 0.3)',
            tickfont=dict(color='#94a3b8', size=11),
            zerolinecolor='#334155',
            title_font=dict(color='#94a3b8')
        ),
        legend=dict(
            title_font_family="Inter",
            font_family="Inter",
            font_color="#cbd5e1",
            bgcolor="rgba(15, 23, 42, 0.6)",
            bordercolor="#334155",
            borderwidth=1,
            orientation="h",       # Horizontal legend for better spacing
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            font_family="Inter",
            bgcolor="#1e293b", 
            font_size=14,
            font_color="#f8fafc",
            bordercolor="#6366f1"
        ),
        colorway=[
            STUDIO_COLORS["cyan"],
            STUDIO_COLORS["indigo"],
            STUDIO_COLORS["emerald"],
            STUDIO_COLORS["amber"],
            STUDIO_COLORS["rose"]
        ]
    )
    # Ensure transparency for all subplots if any
    fig.update_xaxes(showgrid=False, linecolor='#334155')
    fig.update_yaxes(showgrid=True, gridcolor='rgba(51, 65, 85, 0.3)')
    
    return fig
