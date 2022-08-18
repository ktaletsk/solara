"""
# Overview
Click on one of the items on the left.
"""

import inspect
import urllib.parse

from solara.kitchensink import react, sol, v

title = "API"


@react.component
def Page():
    return sol.Markdown(__doc__)


@react.component
def Layout(children=[], level=0):
    # note that we don't use children here, but we used route.module instead to ge the module
    # this is fine because all api/*.py files use the standard Page component, and do not add
    # a new Layout component
    route_current, all_routes = sol.use_route()
    if route_current is None:
        return sol.Error("Page not found")

    # keeps track of which routes we includes
    routes = {r.path: r for r in all_routes.copy()}

    def add(path):
        route = routes[path]
        with sol.Link(route):
            sol.ListItem(route.label, value=route.path)
        del routes[path]

    with sol.HBox(grow=True) as main:
        with v.NavigationDrawer(right=False, width="min-content", v_model=True, permanent=True):
            with v.List(dense=True):
                with v.ListItemGroup(v_model=route_current.path):
                    # sol.ListItem("Overview")
                    add("/")
                    with sol.ListItem("Input", icon_name="mdi-chevron-left-box"):
                        add("button")
                        add("slider")
                        add("togglebuttons")
                        add("file_browser")
                    with sol.ListItem("Output", icon_name="mdi-chevron-right-box"):
                        add("markdown")
                        add("markdown_editor")
                        add("html")
                        add("image")
                        # add("code")
                        add("sql_code")
                    with sol.ListItem("Viz", icon_name="mdi-chart-histogram"):
                        add("plotly")
                        add("plotly_express")
                    #     sol.ListItem("AltairChart")
                    with sol.ListItem("Layout", icon_name="mdi-page-layout-sidebar-left"):
                        add("hbox")
                        add("vbox")
                        add("griddraggable")
                        add("gridfixed")
                        # add("app")
                    with sol.ListItem("Data", icon_name="mdi-database"):
                        # sol.ListItem("DataTable")
                        add("datatable")
                        add("pivot_table")
                    with sol.ListItem("Hooks", icon_name="mdi-hook"):
                        # add("use_fetch")
                        # add("use_json")
                        add("use_thread")
                        add("use_exception")
                        add("use_previous")
                        add("use_state_or_update")
                    with sol.ListItem("Types", icon_name="mdi-fingerprint"):
                        # sol.ListItem("Action")
                        # sol.ListItem("ColumnAction")
                        # sol.ListItem("Route")
                        add("route")
                    with sol.ListItem("Routing", icon_name="mdi-router"):
                        add("use_route")
                        # add("use_router")
                        # add("use_route_level")

                        # add("resolve_path")
                        # add("use_pathname")

                        # add("generate_routes")
                        # add("generate_routes_directory")

                        # add("RenderPage")
                        # add("DefaultNavigation")
                        add("link")
        if routes:
            print(f"Routes not used: {list(routes.keys())}")  # noqa
        with sol.HBox(grow=True):
            with sol.Padding(4):
                if route_current.module:
                    WithCode(route_current.module)

    return main


@react.component
def WithCode(module):
    # e = react.use_exception_handler()
    # if e is not None:
    #     return sol.Error("oops")
    component = getattr(module, "Page", None)
    show_code, set_show_code = react.use_state(False)
    with v.Sheet() as main:
        with v.Dialog(v_model=show_code, on_v_model=set_show_code):
            with v.Sheet(class_="pa-4"):
                if component:
                    if hasattr(module, "sources"):
                        codes = [inspect.getsource(k) for k in module.sources]
                        code = "\n".join(codes)
                    else:
                        code = inspect.getsource(component.f)
                    code = code.replace("```", "~~~")
                    pre = ""
                    sol.MarkdownIt(
                        f"""
```python
{pre}{code}
```
"""
                    )
        # It renders code better
        sol.Markdown(module.__doc__ or "# no docs yet")
        if component:
            sol.Markdown("# Example")
            sol.Button("Show code", icon_name="mdi-eye", on_click=lambda: set_show_code(True), class_="ma-4")
            code = inspect.getsource(module)

            code_quoted = urllib.parse.quote_plus(code)
            url = f"https://test.solara.dev/try?code={code_quoted}"
            sol.Button("Run on solara.dev", icon_name="mdi-pencil", href=url, target="_blank")
            component()
    return main
