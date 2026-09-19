from __future__ import annotations

from typing import Any

from app.core.supabase_client import supabase


class EdgeSet:
    def __init__(self, key: str, ids: list[Any]) -> None:
        self.key = key
        self.ids = ids


def get_edges(key: str) -> list[str]:
    response = (
        supabase.table("edges")
        .select("member")
        .eq("key", key)
        .order("position")
        .execute()
    )

    return [row["member"] for row in (response.data or [])]


def set_edges_many(entries: list[EdgeSet]) -> None:
    if not entries:
        return

    keys = [entry.key for entry in entries]

    supabase.table("edges").delete().in_("key", keys).execute()

    rows = [
        {"key": entry.key, "member": f"{id_}", "position": position}
        for entry in entries
        for position, id_ in enumerate(entry.ids)
    ]

    if not rows:
        return

    supabase.table("edges").insert(rows).execute()


def set_edges(key: str, ids: list[Any]) -> None:
    set_edges_many([EdgeSet(key, ids)])


def remove_edges_many(keys: list[str]) -> None:
    if not keys:
        return

    supabase.table("edges").delete().in_("key", keys).execute()


def remove_edges(key: str) -> None:
    remove_edges_many([key])


def remove_edge(key: str, member: Any) -> None:
    supabase.table("edges").delete().eq("key", key).eq("member", f"{member}").execute()


class Edges:
    get = staticmethod(get_edges)
    set = staticmethod(set_edges)
    set_multiple = staticmethod(set_edges)
    set_many = staticmethod(set_edges_many)
    remove = staticmethod(remove_edge)
    remove_multiple = staticmethod(remove_edges)
    remove_many = staticmethod(remove_edges_many)


edges = Edges()
