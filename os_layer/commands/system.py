from AppOpener import open
from core.registry import register
import os
import webbrowser


@register("open_app")
def open_app(args):
    app = args.get("app", "")
    if not app:
        return "App name missing."

    try:
        open(app, match_closest=True, throw_error=True)
        return f"Opening {app}..."
    except Exception as e:
        return f"Failed to open '{app}': {str(e)}"

@register("search_web")
def search_web(args):
    query = args.get("query", "")
    if not query:
        return "Search query is missing."

    
    search_url = f"https://www.google.com/search?q={query}"
    try:
        webbrowser.open(search_url)
        return f"Searching the web for: {query}"
    except Exception as e:
        return f"Failed to search for '{query}': {str(e)}"


@register("shutdown")
def shutdown(args):
    
    try:
        if os.name == 'nt':  # Windows
            os.system("shutdown /s /f /t 0")
        else:  # Unix-like (Linux, macOS)
            os.system("shutdown -h now")
        return "Shutting down the system..."
    except Exception as e:
        return f"Failed to shutdown: {str(e)}"