# Estilos compartidos para la sección de Academia

OLIVE       = "#5B733A"
OLIVE_DARK  = "#3E5228"
OLIVE_LIGHT = "#7A9A4E"
CARD_BG     = "rgba(255,255,255,0.96)"
NAV_BG      = "#3E5228"
TEXT_DARK   = "#1a1a1a"
TEXT_MID    = "#444"
GRAY_LIGHT  = "#f0f0f0"
BADGE_GREEN = "#28a745"
BADGE_RED   = "#e53e3e"
BADGE_GRAY  = "#555"

CARD_STYLE = dict(
    background=CARD_BG,
    border_radius="16px",
    box_shadow="0 8px 32px rgba(0,0,0,0.18)",
)

BTN_PRIMARY_BASE = dict(
    background=OLIVE,
    color="white",
    border_radius="8px",
    font_weight="600",
    cursor="pointer",
    _hover={"background": OLIVE_DARK},
)

BTN_SECONDARY_BASE = dict(
    background="white",
    color=OLIVE,
    border="2px solid " + OLIVE,
    border_radius="8px",
    font_weight="600",
    cursor="pointer",
    _hover={"background": OLIVE, "color": "white"},
)

BTN_BACK_BASE = dict(
    background="rgba(255,255,255,0.15)",
    color="white",
    border="1px solid rgba(255,255,255,0.4)",
    border_radius="8px",
    cursor="pointer",
    _hover={"background": "rgba(255,255,255,0.3)"},
)
