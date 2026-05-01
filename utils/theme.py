# utils/theme.py
# Single source of truth for all colors and Plotly layout.
# Information Theory × Finance series — github.com/information-theory-finance

# ── Palette ─────────────────────────────────────────────────────────────────
NAVY_DARKEST = "#0a0e1a"
NAVY_DARK    = "#0f1629"
NAVY_MID     = "#1a2444"
NAVY_LIGHT   = "#243060"
SILVER_MID   = "#b0bccc"
SILVER_LIGHT = "#d4dce8"
AMBER        = "#f5a623"
AMBER_LIGHT  = "#fbbf45"
GREEN_UP     = "#a3be8c"
RED_DOWN     = "#f08030"
BLUE_ACCENT  = "#88c0d0"
TEXT_PRIMARY = "#e8edf5"
TEXT_MUTED   = "#8a9ab8"
BORDER       = "#2a3a5c"


def plotly_layout(title: str = "", x_title: str = "", y_title: str = "") -> dict:
    """Return a base Plotly layout dict consistent with the app theme."""
    return dict(
        title=dict(text=title, font=dict(color=TEXT_PRIMARY, size=15)),
        paper_bgcolor=NAVY_DARKEST,
        plot_bgcolor=NAVY_DARK,
        font=dict(color=TEXT_PRIMARY, family="JetBrains Mono, monospace", size=12),
        xaxis=dict(
            title=dict(text=x_title, font=dict(color=SILVER_LIGHT)),
            gridcolor=BORDER,
            zerolinecolor=BORDER,
            color=SILVER_MID,
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(color=SILVER_LIGHT)),
            gridcolor=BORDER,
            zerolinecolor=BORDER,
            color=SILVER_MID,
        ),
        legend=dict(
            bgcolor=NAVY_MID,
            bordercolor=BORDER,
            borderwidth=1,
            font=dict(color=SILVER_LIGHT),
        ),
        margin=dict(l=60, r=30, t=55, b=55),
        hovermode="x unified",
    )
