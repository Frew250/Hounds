---
name: ops-gmail-triage
description: >
  Reads Gmail inbox, sent folder, and labels to produce a two-part report:
  (1) a prioritised inbox triage of what needs attention today, and (2) a CRM
  Pulse showing the health of active deals, client relationships, cold threads,
  and what's waiting on other people. Use this skill whenever the user wants to
  process their email, get a relationship/pipeline overview, see what needs
  attention, do a CRM check-in, or asks "what do I need to deal with?" — even
  if they don't say "triage" or "CRM". Triggers on: "triage my email", "check
  my inbox", "what emails need attention", "go through my email", "catch up on
  email", "what do I need to deal with", "email roundup", "inbox check", "CRM
  check", "who should I follow up with", "who have I not heard back from".
  Does NOT trigger for sending email, composing drafts, or managing labels.
---

# Gmail Triage + CRM Pulse

Read the inbox, sent folder, and CRM labels to give a complete picture: what to act on today, and how every key relationship is tracking.

## Outcome

A two-part report shown in the conversation:

**Part 1 — Inbox Triage:** threads grouped by urgency and action type  
**Part 2 — CRM Pulse:** relationship health grouped by label and status

No files saved. Read-only — no actions taken unless the user asks.

## Context Needs

| File | Load level | Purpose |
|------|-----------|---------|
| `context/learnings.md` | `## ops-gmail-triage` section | Sender rules, label mappings, CRM preferences |

No brand context needed.

## Skill Relationships

- No upstream skill dependencies
- Downstream: could feed into a future `ops-gmail-reply` skill for drafting follow-ups

---

## Step 1: Read Labels and Identify CRM Labels

Call `mcp__claude_ai_Gmail__list_labels` to get all Gmail labels.

Scan the label names and classify each as:
- **CRM label** — names suggesting relationship tracking: anything containing words like `client`, `prospect`, `deal`, `lead`, `customer`, `partner`, `investor`, `vendor`, `project`, `contract`, or custom names that look like company/person names
- **System label** — Gmail built-ins (INBOX, SENT, UNREAD, STARRED, etc.) — skip these
- **Other labels** — everything else, include if they look like they contain useful threads

Store the identified CRM labels. If none are found, note this and proceed — the CRM Pulse will rely on sent/inbox analysis instead.

## Step 2: Fetch Inbox, Sent, and Labeled Threads

Run these searches in order. For each, fetch up to 50 threads unless clearly limited:

1. **Inbox**: `mcp__claude_ai_Gmail__search_threads` with query `in:inbox`
2. **Sent (recent)**: `mcp__claude_ai_Gmail__search_threads` with query `in:sent newer_than:30d`
3. **Per CRM label**: for each CRM label identified in Step 1, search `label:{label-name} newer_than:30d`

Deduplicate across results — a thread can appear in multiple searches (e.g. inbox + labeled). Track each thread's presence across sources; it's useful context.

Use `mcp__claude_ai_Gmail__get_thread` to read full thread content when:
- The snippet is too short to categorise confidently
- You need to determine who sent the last message
- The thread looks important for the CRM Pulse and you need the full history

## Step 3: Categorise for Inbox Triage

For every **inbox** thread, assign it to one bucket:

| Bucket | Signals |
|--------|---------|
| 🔴 **Action Today** | Words like "urgent", "today", "ASAP", "deadline", "by end of day"; legal/financial/contract senders; calendar invites expiring today; direct questions from key contacts |
| 🟡 **Reply Needed** | Direct question or request addressed to the user; "following up", "let me know", "when can we"; thread where a response is expected but no deadline |
| ⏳ **Waiting / Sent Last** | The user's email is the sender of the most recent message — ball is in the other person's court |
| 📖 **FYI Only** | Newsletters, confirmations, automated updates, CC'd threads, no action expected |
| 🗑️ **Can Archive** | Promotional, order receipts, resolved threads, unsubscribe candidates |

When uncertain between 🔴 and 🟡, default to 🟡 — urgency should be clear, not inferred.

## Step 4: Build CRM Pulse

This section maps relationship health, not individual email urgency. Work across all fetched threads (inbox + sent + labeled).

Group into four CRM views:

### 4a — Active Deals & Prospects
Threads labeled as prospect/lead/deal labels OR recent sent+inbox threads with companies/individuals that look like active business conversations. Show: contact name, what stage the conversation is at, last touchpoint date.

### 4b — Client Relationships
Threads labeled as client/customer labels OR frequent contacts who appear in multiple recent threads. Show: client name, last interaction, any open asks or pending items.

### 4c — Waiting on Them
Threads (from inbox OR sent) where:
- The user's email sent the last message
- No reply has been received
- Last sent message was within the last 30 days

These are people Craig is waiting on. Show: contact, what was asked, how long ago it was sent.

### 4d — Gone Cold (> 1 week)
Threads where:
- Last activity was more than 7 days ago (see Rules for threshold)
- The relationship looks like it should still be active (is labeled, or was a substantive back-and-forth)
- No recent follow-up has been sent

These are relationships that need a nudge. Show: contact, last touchpoint, what the thread was about.

## Step 5: Present the Report

### Part 1: Inbox Triage

Open with a one-line count summary:

```
📬 Inbox Triage — {date}
{N} threads · {A} action today · {R} need replies · {W} waiting · {F} FYI · {X} archivable
```

Render each non-empty bucket in order (🔴 → 🟡 → ⏳ → 📖 → 🗑️). For each thread:

```
{N}. **{Subject}** — {Sender} · {relative date}
   {One sentence: what action is needed or why it's in this bucket}
```

Collapse 🗑️ if more than 10 items — just show the count.

---

### Part 2: CRM Pulse

Open with a header and counts:

```
🔗 CRM Pulse — {N} active · {W} waiting · {C} gone cold
Labels tracked: {list of CRM labels found}
```

Then render each non-empty CRM view in order (Active → Clients → Waiting → Cold). For each contact/thread:

```
**{Contact / Company}** · last touch: {relative date}
{One sentence: status, what was discussed, what's needed next}
```

For Gone Cold specifically, end each entry with a suggested next action in italics:
> *Suggested: quick check-in — "Hey {name}, wanted to follow up on..."*

---

After both sections, ask: "Anything you want to dig into, or would you like me to draft a follow-up for any of these?"

---

## Rules

- Read `context/learnings.md` (`## ops-gmail-triage`) before starting — it may contain sender-specific priority rules, confirmed label mappings, or CRM contact classifications.
- **user_email**: `craigfrew4@gmail.com` — used to detect "Waiting on Them" threads where Craig sent the last message.
- **stale_threshold**: 7 days — threads with no activity beyond this are flagged as Gone Cold.
- **crm_labels**: Store confirmed CRM label names here after first run, e.g. `clients, prospects, CampMatch`
- Don't take actions (label, archive, reply, delete) unless the user explicitly asks.
- Don't fabricate urgency. If unclear whether something is urgent, use 🟡.

## Self-Update

If the user corrects a categorisation, confirms a label as CRM-relevant, or adjusts the stale threshold, update the `## Rules` section immediately with a dated entry. Format:

```
- {YYYY-MM-DD}: {Rule — e.g. "Emails from noreply@stripe.com always → Archive", "Label 'campMatch' is a CRM label", "stale_threshold changed to 14 days"}
```
