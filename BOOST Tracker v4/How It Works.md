# BOOST Tracker v4: how it works

Two files:

| File | What it's for |
|---|---|
| **BOOST Tracker v4.xlsx** | The real one. Empty, with your nine events already listed (dates to fill in). |
| **BOOST Tracker v4 - DEMO.xlsx** | The same workbook filled with **fictional** people, for showing how it works. Every name, email and phone in it is made up (`@example.com`, `555-01xx`). |

The **Start Here** tab inside the workbook says the same as this page, in shorter form.

---

## The idea in one line

**A person is a number and two letters.** `P-0012 · JD`. Names, emails and phones stay in the Microsoft Forms response sheet. They appear in exactly one place, **Contact Card**, one person at a time, when you need to make the call.

That means People, Follow-Ups, Event Report and Dashboard can be put on a screen, printed or emailed without exposing anyone.

---

## The day, start to finish

**1. Before the event: Events tab.** Add a row with an Event ID and a **date**. The date is what links sign-ups to the event.

**2. At the table.** They scan the QR and fill in the form. You don't type anything.
*Walk-up without the form?* Add a People row: type the date in *Registered On*, their initials, and a Contact Type. The Event ID fills from the date.

**3. After the event: New Sign-Ups tab.** Lists every form response with initials, the event it matched, and a marker: **→ add** if it isn't on People yet, **✓ logged** if it is. The orange number at the top is how many are still to add.

**4. People tab.** For each **→ add**, go to the next empty row and type the **Response ID** into column U (the orange header). The teal columns fill themselves: event, date, initials, contact type, organization, region, situation, apprentice status, trade and consent. Then write the navy columns: **Service Level, Main Need, Stage, Conversation Notes**, materials, follow-up.

**5. Follow-Ups tab.** Tick *Follow-Up Needed* on People and give it a due date. Follow-Ups lists everyone you owe a call, **soonest first**: red when overdue, amber when due in the next 7 days. When it's done, put the date in *Follow-Up Done* and it drops off the list.

**6. Event Report tab.** Pick the Event ID from the dropdown. Totals and the list of people at that event fill themselves (**initials only**). Write your note to the reader in the yellow box, then File → Print → Save as PDF. The print area sizes itself to the number of people, so you get no blank pages.

**When you need to call someone: Contact Card.** Type the Participant #. Name, email, phone and city appear, along with a red warning if they said **no** to contact. Clear the box when you're done.

---

## The tabs

| Tab | You type here? | What it does |
|---|---|---|
| Start Here | — | How-to, on one page |
| **People** | ✔ | One row per person. The heart of the file |
| **New Sign-Ups** | — | Form responses not yet on People |
| **Follow-Ups** | — | Who you owe a call, soonest first |
| **Events** | ✔ | One row per event. ID and date first |
| **Event Report** | Event ID + note | The printable report, initials only |
| **Dashboard** | — | Totals, progress against commitments, and a table by event |
| Contact Card | Participant # | The only tab showing names and contact details |
| Setup | Rarely | Tells the tracker which form column is which |
| Lists | Rarely | Dropdown values. Add at the bottom |
| Sheet1 | Paste only | The form's responses (see *Connecting the form*) |

### Colours

* **Teal header**: fills itself from the form. You can type over it, and that row keeps what you typed.
* **Navy header**: yours.
* **Grey header**: counts itself. Leave it alone.
* **Orange header**: the link, *Form Response ID*.
* **Yellow cell**: type here.
* **Red on Event ID**: no event matched that date. Add the event's date on Events, or type the ID.
* **Amber on Event ID**: two events on the same day, so check this row's ID.
* **Light grey cell**: doesn't apply to this contact type (e.g. Organization for a Trade person).

---

## Privacy rules built in

1. **No names, emails or phones on People.** Initials only, worked out from the form's *Full name*.
2. **Self-identification never lands on a person's row.** The Dashboard counts it straight from the form as totals (KPI 2, KPI 26).
3. **Consent = No** shows in red on People and on Contact Card.
4. **Event Report shows initials only** and has a footer saying contact details are held separately.
5. **Contact Card prints nothing.** Its print area is a single blank cell.
6. **In Conversation Notes**, write what they need and what you agreed, not who they are. No health details or diagnoses, no SIN, no dates of birth, no addresses.

---

## Connecting the form

Microsoft Forms writes responses to **`Event Registration - Literacy Link South Central.xlsx`** (OneDrive → Documents), on a sheet called **Sheet1**. The tracker reads its own tab called **Sheet1**, so you have two ways to connect them:

**Option A: paste (simplest, recommended).** After each event: Forms → Responses → **Open in Excel**. Click the corner of that sheet to select it all, copy, and paste over the tracker's **Sheet1** at A1. It takes 30 seconds and always works, including offline.

**Option B: live.** Copy every tab **except Sheet1** into the Forms workbook (right-click a tab → Move or Copy → choose that workbook → tick *Create a copy*; do Lists and Setup first). Excel will point the formulas back at this file, so finish with **Data → Edit Links → Change Source** and choose the Forms workbook itself. Do it in Excel desktop, not the browser, and never re-upload the Forms workbook (the sync belongs to that exact file).

### Setup: if a column is worded differently

The **Setup** tab looks for each form question by a word or phrase from its heading (e.g. *"region"*, *"describes you"*). Column E shows the heading it found, or **✗ not found**. If you see ✗, type a word from the real heading into the yellow cell and it reconnects. Blank means "not used". The tracker carries on fine without any of the optional ones.

Two small keyword tables on Setup turn form answers into dropdown values: *"I'm an employer…"* → **Employer & Union**, and *"I'm working, but I'm not a journeyperson"* → **Incumbent worker**. Add a keyword in the yellow cells if an answer isn't being recognised. The lowest matching row wins.

### Tagging the event in the QR (optional, recommended)

If you add a question like *"Where are you signing up today?"* to the form and make one pre-filled link (and QR) per event with the Event ID as the answer, the tracker uses that **before** the date. That fixes the two weak spots of date matching: two events on one day, and people who fill in the form at home days later. Setup row *Event* is already looking for a heading containing *"signing up today"*.

---

## Moving your existing data across

You can do it by hand: copy your events onto Events, then for each person type the Response ID into People column U and paste the notes.

Or run the script in `tools/` on your Mac. It reads your old tracker and writes a **new** file, *BOOST Tracker v4 - with my data.xlsx*, leaving both originals untouched. It never copies names, emails or phones. For rows without a form response it makes initials. It prints counts only.

```
cd "path/to/BOOST Tracker v4/tools"
python3 move_my_data.py "path/to/old tracker.xlsx" "../BOOST Tracker v4.xlsx"
```

Then open the new file and check three things: Setup is all ✓ (after you paste in Sheet1), New Sign-Ups shows "✓ logged" for the people you had, and a handful of People rows look right.

---

## Don't

* Don't delete or rename **Sheet1**.
* Don't **delete** rows on People. Clear them instead, so Participant #s stay unique and never get reused.
* Don't edit the hidden helper columns (People W–Z; a few on the report tabs).
* Don't type over a Participant #.

Sorting and filtering People is fine: every row carries its own formulas.

---

## What changed from the September tracker, and why

| Before | Now | Why |
|---|---|---|
| Four people tabs (Trade / Employers / Colleges / Other) | **One People tab** with a Contact Type column. Columns that don't apply turn grey | One list to sort, filter and report on. No hidden cross-tab key column to break. Moving someone to the right type is a dropdown, not a cut-and-paste |
| Name, phone and email pulled onto every row (hidden) | **Initials only.** Contact details only on Contact Card | You asked to see initials and a number. It also makes the file safe to show and send |
| No way to see who signed up but wasn't logged | **New Sign-Ups** tab with a "→ add" counter | Nobody falls through the cracks after a busy event |
| Follow-up as a tick and a date | **Follow-Ups** tab, soonest first, with overdue in red, due-soon in amber, and a Done date | It's a to-do list, not just a column |
| Event Report listed name details | **Initials only**, sizes its own print area, adds the report's own totals | Safe to send to Vito, with no blank pages |
| Form columns hard-wired by letter | **Setup** finds them by heading | Rewording or adding a form question doesn't break the file |
| KPI dashboard removed | A light **Dashboard**: totals, a commitments table and a by-event table, all counted from what you already capture | Useful for meetings. Nothing extra to type. Delete the tab if you don't want it; nothing depends on it |
| Two events on one day: silent wrong guess | Event ID **turns amber** | You know which rows to check |

*Commitment targets on Setup came from the targets quoted in the sign-up form spec (from Performance Commitments 2026-27 V2.0). Check them against the source.*
