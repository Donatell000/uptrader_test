from django import template
from django.urls import reverse, NoReverseMatch
from django.utils.html import format_html
from django.template.context import Context

from menu.models import MenuItem


register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context: Context, menu_name: str) -> str:
    request = context["request"]
    path = request.path

    items = list(
        MenuItem.objects.select_related("parent")
        .filter(menu_name=menu_name)
        .order_by("id")
    )

    active_item = _find_active_item(items, path)
    tree = _build_tree(items)
    html = _render_menu(tree, active_item)
    return format_html(html)


def _get_menu_item_url(item: MenuItem) -> str:
    if item.named_url:
        try:
            return reverse(item.named_url)
        except NoReverseMatch:
            return "#invalid_named_url"
    if item.custom_url:
        return item.custom_url
    try:
        return reverse("menu:page", kwargs={"slug": item.slug})
    except NoReverseMatch:
        return f"#{item.slug}"


def _find_active_item(items: list[MenuItem], path: str) -> MenuItem | None:
    for item in items:
        if _get_menu_item_url(item) == path:
            return item
    return None


def _build_tree(items: list[MenuItem]) -> list[dict]:
    item_dict: dict[int, dict] = {item.id: {"item": item, "children": []} for item in items}
    tree: list[dict] = []

    for item in items:
        if item.parent_id:
            parent = item_dict.get(item.parent_id)
            if parent:
                parent["children"].append(item_dict[item.id])
        else:
            tree.append(item_dict[item.id])

    return tree


def _render_menu(nodes: list[dict], active_item: MenuItem | None, level: int = 0) -> str:
    html = "<ul>"

    for node in nodes:
        item: MenuItem = node["item"]
        children: list[dict] = node["children"]
        is_active = item == active_item
        is_parent = _is_parent_of(item, active_item) if active_item else False

        if is_active:
            css_class = "active"
        elif is_parent:
            css_class = "active-parent"
        else:
            css_class = ""

        url = _get_menu_item_url(item)
        html += f"<li><a href='{url}' class='{css_class}'>{item.name}</a>"

        if children and (is_active or is_parent or level == 0):
            html += _render_menu(children, active_item, level + 1)

        html += "</li>"

    html += "</ul>"
    return html


def _is_parent_of(parent: MenuItem, child: MenuItem) -> bool:
    current = child.parent
    while current:
        if current == parent:
            return True
        current = current.parent
    return False
