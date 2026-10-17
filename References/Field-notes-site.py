"""Reference file from github.com/ARKlight-Test-Collections/Field-Notes
(entry file, site.py). Vendored verbatim for the real multi-file
route-registration pattern (SKILL.md gotcha #3) and site.style(...)/
site.style_selector(...) usage at real-project scale. Use `arklight
search <name>` for anything this file's own version might lag."""

# include <stdlib.ARKlight>

from pages.about import field_guide
from pages.home import home

site = Site(
    name="Field Notes Supply",
    max_width="100%",
    bg="#f1f0e8",
    font_family="'Trebuchet MS', 'Gill Sans', sans-serif",
    grid_min="15rem",
    grid_space="1.15rem",
    sidebar_width="21rem",
    sidebar_space="2rem",
)

STYLES = {
    "site-frame": {"width": "100%", "margin": "0 auto"},
    "site-header": {"display": "flex", "flex-wrap": "wrap", "align-items": "center", "justify-content": "space-between", "gap": "1.2rem", "min-height": "5.5rem", "border-bottom": "1px solid #c9c9bd"},
    "brand-lockup": {"display": "flex", "align-items": "center", "gap": "0.8rem"},
    "brand-mark": {"display": "grid", "place-items": "center", "width": "2.5rem", "height": "2.5rem", "background": "#e29a42", "color": "#1b3028", "font-family": "'DM Mono', monospace", "font-size": "1.15rem", "font-weight": "700"},
    "brand-copy": {"display": "flex", "flex-direction": "column", "gap": "0.1rem"},
    "brand-name": {"color": "#1b3028", "font-family": "Georgia, serif", "font-size": "1.08rem", "font-weight": "600", "line-height": "1.1"},
    "brand-caption": {"color": "#69716a", "font-family": "'DM Mono', monospace", "font-size": "0.59rem"},
    "main-nav": {"display": "flex", "align-items": "center", "gap": "1.6rem"},
    "nav-item": {"color": "#45574d", "font-size": "0.83rem", "text-decoration": "none"},
    "nav-kit-link": {"padding": "0.55rem 0.8rem", "border": "1px solid #9da79c", "color": "#1b3028", "font-family": "'DM Mono', monospace", "font-size": "0.68rem", "text-decoration": "none"},
    "app-content": {"padding": "1.4rem 0 3rem"},
    "intro-band": {"display": "flex", "padding": "0 0 1.25rem", "border-bottom": "1px solid #c9c9bd"},
    "intro-copy-column": {"display": "flex", "flex-direction": "column", "justify-content": "center", "gap": "0.45rem"},
    "eyebrow": {"color": "#8b5728", "font-family": "'DM Mono', monospace", "font-size": "0.67rem", "font-weight": "500"},
    "page-title": {"max-width": "24ch", "margin": "0", "color": "#1b3028", "font-family": "Georgia, serif", "font-size": "2.4rem", "font-weight": "500", "line-height": "1.08"},
    "intro-copy": {"max-width": "32rem", "color": "#59645c", "font-size": "0.9rem", "line-height": "1.5"},
    "collection-stamp": {"display": "flex", "flex-direction": "column", "gap": "0.25rem", "margin-top": "0.75rem", "padding-left": "0.8rem", "border-left": "3px solid #e29a42"},
    "collection-label": {"color": "#767c72", "font-family": "'DM Mono', monospace", "font-size": "0.6rem"},
    "collection-value": {"color": "#1b3028", "font-family": "'DM Mono', monospace", "font-size": "0.68rem"},
    "feature-figure": {"position": "relative", "min-height": "21rem", "margin": "0", "overflow": "hidden", "background": "#d1d2c7"},
    "feature-image": {"width": "100%", "height": "100%", "min-height": "21rem", "object-fit": "cover"},
    "feature-caption": {"position": "absolute", "right": "0.8rem", "bottom": "0.8rem", "padding": "0.45rem 0.6rem", "background": "#f1f0e8", "color": "#46554b", "font-family": "'DM Mono', monospace", "font-size": "0.58rem"},
    "app-layout": {"align-items": "start", "padding-top": "2rem"},
    "catalog-column": {"min-width": "0"},
    "catalog-tools": {"display": "flex", "flex-wrap": "wrap", "align-items": "end", "justify-content": "space-between", "gap": "1rem", "margin-bottom": "1.35rem"},
    "catalog-heading": {"display": "flex", "flex-direction": "column", "gap": "0.45rem"},
    "catalog-status": {"color": "#1b3028", "font-family": "Georgia, serif", "font-size": "1.7rem"},
    "search-row": {"display": "flex", "align-items": "center", "gap": "0.5rem", "min-width": "min(100%, 22rem)"},
    "search-input": {"width": "100%", "min-width": "0", "padding": "0.75rem 0.85rem", "border": "1px solid #bbc0b5", "border-radius": "0", "background": "#fbfaf5", "color": "#1b3028", "font-family": "'Trebuchet MS', sans-serif", "font-size": "0.82rem"},
    "clear-button": {"padding": "0.7rem 0.8rem", "border": "1px solid #b7bdb2", "border-radius": "0", "background": "transparent", "color": "#31463a", "font-family": "'DM Mono', monospace", "font-size": "0.67rem"},
    "category-row": {"display": "flex", "flex-wrap": "wrap", "gap": "0.45rem", "width": "100%"},
    "category-button": {"padding": "0.55rem 0.78rem", "border": "1px solid #c4c6bb", "border-radius": "0", "background": "transparent", "color": "#44554b", "font-family": "'DM Mono', monospace", "font-size": "0.65rem"},
    "product-grid": {"grid-template-columns": "repeat(auto-fit, minmax(min(100%, 14rem), 1fr))", "align-items": "stretch", "gap": "1.15rem"},
    "product-card": {"display": "flex", "flex-direction": "column", "min-width": "0", "overflow": "hidden", "border": "1px solid #d3d3c8", "background": "#fbfaf5"},
    "product-figure": {"position": "relative", "display": "block", "aspect-ratio": "4 / 3", "margin": "0", "overflow": "hidden", "background": "#d8d9cf"},
    "product-image": {"display": "block", "width": "100%", "height": "100%", "object-fit": "cover", "transition": "transform 240ms ease"},
    "image-caption": {"position": "absolute", "right": "0.55rem", "bottom": "0.55rem", "padding": "0.35rem 0.45rem", "background": "#f1f0e8", "color": "#4c5b50", "font-family": "'DM Mono', monospace", "font-size": "0.56rem"},
    "product-copy": {"display": "flex", "flex-direction": "column", "align-items": "start", "gap": "0.65rem", "padding": "1rem"},
    "product-overline": {"display": "flex", "align-items": "center", "justify-content": "space-between", "gap": "0.5rem", "width": "100%"},
    "product-badge": {"color": "#a25928", "font-family": "'DM Mono', monospace", "font-size": "0.58rem"},
    "product-category": {"color": "#767c72", "font-family": "'DM Mono', monospace", "font-size": "0.58rem"},
    "product-name": {"margin": "0", "color": "#1b3028", "font-family": "Georgia, serif", "font-size": "1.42rem", "font-weight": "500", "line-height": "1.15"},
    "product-description": {"min-height": "3.2rem", "margin": "0", "color": "#59645c", "font-size": "0.8rem", "line-height": "1.5"},
    "product-details": {"width": "100%", "padding-top": "0.6rem", "border-top": "1px solid #e1e0d7", "color": "#48584d", "font-size": "0.75rem"},
    "spec-copy": {"color": "#667068", "font-family": "'DM Mono', monospace", "font-size": "0.65rem", "line-height": "1.5"},
    "product-action-row": {"display": "flex", "align-items": "center", "justify-content": "space-between", "gap": "0.6rem", "width": "100%", "margin-top": "0.3rem"},
    "product-price": {"color": "#1b3028", "font-family": "'DM Mono', monospace", "font-size": "0.9rem", "font-weight": "500"},
    "add-button": {"padding": "0.68rem 0.75rem", "border": "1px solid #1b3028", "border-radius": "0", "background": "#1b3028", "color": "#f8f5eb", "font-family": "'DM Mono', monospace", "font-size": "0.64rem"},
    "search-note": {"display": "flex", "flex-direction": "column", "align-items": "start", "gap": "0.6rem", "padding": "1.2rem 0", "color": "#667068", "font-size": "0.82rem"},
    "empty-title": {"color": "#1b3028", "font-family": "Georgia, serif", "font-size": "1.1rem"},
    "sidebar-stack": {"display": "flex", "flex-direction": "column", "gap": "1rem", "min-width": "0"},
    "kit-panel": {"padding": "1.25rem", "background": "#1b3028", "color": "#f1f0e8"},
    "kit-eyebrow": {"color": "#e7ad69"},
    "kit-heading": {"display": "flex", "align-items": "baseline", "justify-content": "space-between", "gap": "0.75rem", "margin-top": "0.75rem"},
    "kit-title": {"margin": "0", "color": "#f1f0e8", "font-family": "Georgia, serif", "font-size": "1.8rem", "font-weight": "500"},
    "kit-count-large": {"color": "#e7ad69", "font-family": "'DM Mono', monospace", "font-size": "1.25rem"},
    "kit-description": {"margin": "0.5rem 0 1rem", "color": "#c4cec4", "font-size": "0.78rem"},
    "kit-progress": {"width": "100%", "height": "0.4rem", "margin-bottom": "1rem", "accent-color": "#e29a42"},
    "kit-empty": {"padding": "1rem 0", "border-top": "1px solid #4d6154", "color": "#c4cec4", "font-size": "0.78rem", "line-height": "1.5"},
    "kit-filled": {"padding-top": "0.5rem"},
    "kit-row": {"display": "flex", "align-items": "center", "justify-content": "space-between", "gap": "0.5rem", "padding": "0.7rem 0", "border-top": "1px solid #4d6154"},
    "kit-item-name": {"color": "#f1f0e8", "font-size": "0.76rem"},
    "remove-button": {"padding": "0.3rem 0", "border": "0", "background": "transparent", "color": "#e7ad69", "font-family": "'DM Mono', monospace", "font-size": "0.59rem"},
    "kit-total": {"display": "flex", "justify-content": "space-between", "padding": "0.8rem 0", "border-top": "1px solid #4d6154"},
    "kit-total-label": {"color": "#c4cec4", "font-family": "'DM Mono', monospace", "font-size": "0.63rem"},
    "kit-total-number": {"color": "#f1f0e8", "font-family": "'DM Mono', monospace", "font-size": "0.83rem"},
    "clear-kit-button": {"padding": "0.55rem 0.7rem", "border": "1px solid #718174", "border-radius": "0", "background": "transparent", "color": "#f1f0e8", "font-family": "'DM Mono', monospace", "font-size": "0.62rem"},
    "field-note": {"padding": "1.1rem", "border": "1px solid #d2d2c8", "background": "#e6e7dc", "color": "#1b3028"},
    "note-title": {"margin": "0.65rem 0 0.35rem", "color": "#1b3028", "font-family": "Georgia, serif", "font-size": "1.22rem", "font-weight": "500"},
    "field-note-copy": {"color": "#536159", "font-size": "0.76rem", "line-height": "1.5"},
    "text-link": {"color": "#7d4d23", "font-family": "'DM Mono', monospace", "font-size": "0.7rem", "text-decoration": "none"},
    "site-footer": {"padding": "1.2rem 0", "border-top": "1px solid #c9c9bd"},
    "footer-inner": {"display": "flex", "flex-wrap": "wrap", "justify-content": "space-between", "gap": "0.6rem 1rem", "align-items": "center"},
    "footer-brand": {"color": "#1b3028", "font-family": "Georgia, serif", "font-size": "0.9rem"},
    "footer-copy": {"color": "#667068", "font-size": "0.7rem"},
    "footer-coordinate": {"color": "#8b5728", "font-family": "'DM Mono', monospace", "font-size": "0.58rem"},
    "guide-content": {"width": "min(100%, 74rem)", "margin": "0 auto", "padding": "2.5rem 0 4rem"},
    "guide-opening": {"display": "flex", "flex-direction": "column", "align-items": "start", "gap": "1rem"},
    "guide-title": {"max-width": "15ch", "margin": "0", "color": "#1b3028", "font-family": "Georgia, serif", "font-size": "2.8rem", "font-weight": "500", "line-height": "1.02"},
    "guide-intro": {"color": "#59645c", "font-size": "1rem"},
    "guide-image": {"display": "block", "width": "100%", "max-height": "34rem", "object-fit": "cover"},
    "guide-grid": {"display": "grid", "grid-template-columns": "repeat(auto-fit, minmax(min(100%, 18rem), 1fr))", "gap": "1.5rem", "padding": "2rem 0"},
    "guide-entry": {"padding-top": "1rem", "border-top": "2px solid #e29a42", "color": "#59645c", "font-size": "0.86rem", "line-height": "1.6"},
    "guide-section-title": {"margin": "0.8rem 0", "color": "#1b3028", "font-family": "Georgia, serif", "font-size": "1.55rem", "font-weight": "500", "line-height": "1.15"},
    "guide-checklist": {"padding": "1rem 0", "border-top": "1px solid #c9c9bd", "border-bottom": "1px solid #c9c9bd", "color": "#44554b"},
    "guide-return": {"display": "inline-block", "margin-top": "1.5rem"},
}

for style_name, rules in STYLES.items():
    site.style(style_name, rules)

site.style_selector(".product-card:hover .product-image", {"transform": "scale(1.035)"})
site.style_selector(".main-nav a:hover", {"color": "#a25928"})
site.style_selector(".category-button:hover", {"background": "#e2e2d8", "border-color": "#778276"})
site.style_selector(".add-button:hover", {"background": "#315446", "border-color": "#315446"})
site.style_selector(".text-link:hover", {"color": "#b6632d", "text-decoration": "underline"})
site.style_selector(".page-title", {"font-size": "2.2rem", "max-width": "24ch"}, allow_redefine=True)
site.style_selector(".catalog-section", {"padding-top": "1.2rem"}, allow_redefine=True)
site.style_selector(".catalog-tools", {"gap": "0.7rem", "margin-bottom": "0.9rem"}, allow_redefine=True)
site.style_selector(".catalog-heading", {"flex-direction": "row", "align-items": "baseline", "gap": "0.6rem"}, allow_redefine=True)
site.style_selector(".catalog-status", {"font-size": "1.3rem"}, allow_redefine=True)
site.style_selector(".app-layout", {"display": "flex", "flex-wrap": "wrap", "align-items": "flex-start", "gap": "2rem"}, allow_redefine=True)
site.style_selector(".catalog-column", {"flex": "999 1 40rem", "min-width": "0"}, allow_redefine=True)
site.style_selector(".sidebar-stack", {"flex": "1 1 18rem", "min-width": "0"}, allow_redefine=True)


# Real @site.page(...) decorators live here, not in pages/*.py --
# static discovery (arklight.parser.discover) only looks at the entry
# file's own source, so this is the one place routes must be declared.
# Each function below just delegates to the actual page-content
# function in pages/, which is free to import components/ and
# content/ however it likes.


@site.page("/")
def home_page():
    return home()


@site.page("/field-guide")
def field_guide_page():
    return field_guide()
