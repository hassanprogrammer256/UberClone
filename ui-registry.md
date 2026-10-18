# UI Registry

## Administrator Dashboard Components

Files: `templates/components/administrator/` and `static/css/admin.css`
Last updated: 2026-10-18

| Property | Pattern |
| --- | --- |
| Background | Pale lavender-gray canvas `#f7f7fc`; white analytics surfaces |
| Border | Subtle neutral 1px borders |
| Border radius | 7-10px controls and panels; full pills for statuses |
| Text | Georgia for dashboard display and body; Inter for controls and compact metadata |
| Spacing | 8-14px component gaps; 14-20px panel padding |
| Hover state | Neutral surface shift; selected navigation uses charcoal |
| Shadow | Minimal ambient shadow on white panels |
| Accent usage | Black for navigation, blue for route/selection, green for live/success, red for low supply |

**Pattern notes:** Reuse the parameterized Django includes for metrics, section headings, demand clusters, status badges, and trip rows. Keep the administrator workspace information-dense and operational. On narrow screens, stack panels and allow dispatch tables to scroll horizontally rather than compressing columns.

## App Snackbar

Files: `templates/components/snackbar.html` and `static/css/snackbar.css`
Last updated: 2026-10-18

| Property | Pattern |
| --- | --- |
| Background | White surface with a colored status rail |
| Border | Subtle neutral border with variant-colored left edge |
| Border radius | 8px |
| Text | Dark title, muted message, Inter controls |
| Spacing | 12-16px internal padding; 10px between notices |
| Hover state | Neutral close-button background; pause timer while hovered/focused |
| Shadow | Soft elevated shadow for legibility over page content |
| Accent usage | Green success, red error, blue informational |

**Pattern notes:** Use the shared component from both base layouts. Keep to three visible notices, announce errors assertively and other notices politely, and use `window.showSnackbar({type, title, message, duration})` for client-side alerts.