"""Copy your existing tracker into the v4 layout, on your own Mac.

    python3 move_my_data.py "OLD TRACKER.xlsx" "BOOST Tracker v4.xlsx"

Writes a NEW file next to the v4 template ("BOOST Tracker v4 - with my data.xlsx").
Neither input file is changed. Nothing is sent anywhere, and the script prints
counts only, never names or notes.

What comes across
  Events tab        Event ID, date, name, type, host, city, region, staff, notes
  Each people tab   Form Response ID, Event ID and date (if you typed them),
                    organization, what they need, materials, notes, follow-up, consent.
                    The tab it was on becomes its Contact Type.
What deliberately does NOT come across
  First / last name, email, phone, title. Rows without a Form Response ID get
  initials made from the first and last name instead, and nothing else about who they are.
"""
import shutil
import sys
from pathlib import Path

import openpyxl
from openpyxl.workbook.defined_name import DefinedName

TAB_TYPES = {"trade": "Trade", "employer": "Employer & Union", "union": "Employer & Union",
             "college": "College & Agency", "agenc": "College & Agency", "other": "Other",
             "connection": None, "participant": None, "contact": None, "people": None}


def norm(v):
    return str(v or "").strip().lower()


def header_row(ws, must):
    for r in range(1, 15):
        vals = [norm(c.value) for c in ws[r]]
        if any(must in v for v in vals):
            return r, {v: i for i, v in enumerate(vals) if v}
    return None, {}


def col(hdr, *names, exclude=()):
    for n in names:
        for h, i in hdr.items():
            if n in h and not any(x in h for x in exclude):
                return i
    return None


def typed(cell_f, cell_v):
    """Value only if the person typed it (not a formula result)."""
    f = cell_f.value
    if isinstance(f, str) and f.startswith("="):
        return None
    return cell_v.value if cell_v.value not in ("", None) else None


def initials(first, last):
    parts = (str(first or "") + " " + str(last or "")).split()
    if not parts:
        return None
    return (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()


def main(old_path, template_path):
    old_path, template_path = Path(old_path), Path(template_path)
    out = template_path.with_name("BOOST Tracker v4 - with my data.xlsx")
    if out.exists():
        sys.exit(f"{out.name} already exists. Move or rename it first, so nothing is overwritten.")
    shutil.copy(template_path, out)

    old_f = openpyxl.load_workbook(old_path)                  # formulas
    old_v = openpyxl.load_workbook(old_path, data_only=True)  # last saved values
    new = openpyxl.load_workbook(out)
    allowed = {}
    lists = new["Lists"]
    for c in range(1, lists.max_column + 1):
        label = lists.cell(4, c).value
        allowed[label] = {str(lists.cell(r, c).value) for r in range(5, 61) if lists.cell(r, c).value}

    # ---------------------------------------------------------------- events
    ev_new = new["Events"]
    n_events = 0
    for ws in old_f.worksheets:
        name = ws.title.lower()
        if "event" not in name or "report" in name:
            continue
        hr, hdr = header_row(ws, "event id")
        if not hr:
            continue
        for r in range(5, 105):
            for c in "ABCDEFGHMN":
                ev_new[f"{c}{r}"].value = None
        m = {"A": col(hdr, "event id"), "B": col(hdr, "date"), "C": col(hdr, "event name", "name", "event", exclude=("id",)),
             "D": col(hdr, "type"), "E": col(hdr, "host", "partner", "organi"), "F": col(hdr, "city", "location", "venue"),
             "G": col(hdr, "region"), "H": col(hdr, "staff", "lead"), "N": col(hdr, "worked", "notes")}
        wsv = old_v[ws.title]
        dest = 5
        for r in range(hr + 1, ws.max_row + 1):
            if not ws.cell(r, m["A"] + 1).value:
                continue
            for letter, i in m.items():
                if i is not None:
                    ev_new[f"{letter}{dest}"].value = typed(ws.cell(r, i + 1), wsv.cell(r, i + 1))
            dest += 1
            n_events += 1
        break
    print(f"Events copied: {n_events}")

    # ---------------------------------------------------------------- people
    ppl = new["People"]
    dest = 5
    report, skipped_cols = [], set()
    for ws in old_f.worksheets:
        name = ws.title.lower()
        match = [t for k, t in TAB_TYPES.items() if k in name]
        if not match or "report" in name or "event" in name:
            continue
        hr, hdr = header_row(ws, "conversation notes")
        if not hr:
            hr, hdr = header_row(ws, "form response")
        if not hr:
            continue
        tab_type = match[0]
        wsv = old_v[ws.title]
        c = {k: col(hdr, *v) for k, v in {
            "rid": ("form response id", "response id"), "event": ("event id",), "reg": ("registered on",),
            "first": ("first",), "last": ("last",), "org": ("organization", "organisation", "company"),
            "need": ("what they need", "need"), "mat": ("materials",), "notes": ("conversation notes", "notes"),
            "fu": ("follow-up needed", "follow up needed"), "due": ("follow-up due", "due"),
            "consent": ("consent",), "type": ("contact type",), "orgtype": ("org type",)}.items()}
        c["need"] = col(hdr, "what they need", "need", exclude=("follow",))
        known = {i for i in c.values() if i is not None}
        skipped_cols |= {h for h, i in hdr.items() if i not in known}
        count = 0
        for r in range(hr + 1, ws.max_row + 1):
            get = lambda k: typed(ws.cell(r, c[k] + 1), wsv.cell(r, c[k] + 1)) if c[k] is not None else None  # noqa: E731
            notes, rid = get("notes"), get("rid")
            ini = initials(get("first"), get("last"))
            if not any([notes, rid, ini, get("org")]):
                continue
            if dest > 604:
                sys.exit("More than 600 people. Extend the People tab first.")
            row_type = tab_type or (get("type") if str(get("type")) in allowed["Contact Type"] else None)
            if rid is not None:
                ppl[f"U{dest}"] = rid
            else:
                ppl[f"D{dest}"] = ini
                if row_type:
                    ppl[f"E{dest}"] = row_type
                if get("reg") is not None:
                    ppl[f"C{dest}"] = get("reg")
            if rid is not None and row_type:
                ppl[f"E{dest}"] = row_type  # the tab you put them on beats the form's guess
            if get("event") is not None:
                ppl[f"B{dest}"] = get("event")
            if get("org") is not None and row_type in ("Employer & Union", "College & Agency", None):
                ppl[f"F{dest}"] = get("org")
            extra = []
            need = get("need")
            if need is not None:
                if str(need) in allowed["Main Need"]:
                    ppl[f"L{dest}"] = need
                else:
                    extra.append(f"Needs: {need}")
            if get("orgtype") is not None:
                extra.append(f"Org type: {get('orgtype')}")
            ppl[f"N{dest}"] = " | ".join([str(notes)] * bool(notes) + extra) or None
            if get("mat"):
                ppl[f"O{dest}"] = "✓"
            if get("fu"):
                ppl[f"P{dest}"] = "✓"
            if get("due") is not None:
                ppl[f"Q{dest}"] = get("due")
            consent = norm(get("consent"))
            if consent.startswith("y"):
                ppl[f"T{dest}"] = "Yes"
            elif consent.startswith("n"):
                ppl[f"T{dest}"] = "No"
            dest += 1
            count += 1
        report.append((ws.title, count))
    for t, n in report:
        print(f"People copied from '{t}': {n}")
    print(f"People total: {dest - 5}")
    if skipped_cols:
        print("Columns left behind on purpose or not recognised:", ", ".join(sorted(skipped_cols)))

    # openpyxl can't carry the self-sizing print areas through a load/save, so put them back
    for sheet, first, last, width in (("Follow-Ups", 7, 156, 9), ("Event Report", 18, 97, 9)):
        new[sheet].defined_names["_xlnm.Print_Area"] = DefinedName(
            "_xlnm.Print_Area",
            attr_text=f"OFFSET('{sheet}'!$A$1,0,0,{first - 1}+MAX(1,COUNT('{sheet}'!$K${first}:$K${last})),{width})")
    new.calculation.fullCalcOnLoad = True
    new.save(out)
    print(f"\nSaved: {out}\nOpen it, then check: Setup (all ✓), New Sign-Ups, and a few rows on People.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
