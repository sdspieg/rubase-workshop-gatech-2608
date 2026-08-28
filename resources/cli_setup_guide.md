# Getting a CLI AI assistant working — RuBase Workshop

**You need one of these working by Day 2.** Not three. One.

This guide gets you there. Windows users have **one preparation section** to work through **before you arrive**; everyone else
can do the whole thing in the lunch break on Day 1.

---

## Don't let the terminal intimidate you

If you normally work in a graphical interface, this is less of a change than it looks. Using a CLI
AI assistant is the same conversation you already have with ChatGPT, Claude or Gemini in a browser
— you are just typing it somewhere else.

You will:

1. Open a terminal (a text-based window)
2. Type your question in plain English
3. Press Enter

That is it. No programming required.

Instead of typing into a browser box:

> "Summarize the main themes in this research paper"

you type in a terminal:

```bash
claude "Summarize the main themes in this research paper"
```

The conversation is identical. Only the window changed.

## Why a terminal instead of a browser

1. **Your files, directly.** The tool reads files from your own disk. No more copy-pasting a PDF's
   text into a browser box one chunk at a time.
2. **Repeatable.** You can save what you ran, re-run it, and put it in a paper's methods section.
3. **Many files at once.** Ask one question of two hundred documents instead of two hundred questions.
4. **It composes.** The output can feed straight into other tools you already use.

> ### ⚠️ What this does *not* give you: privacy
>
> **Local execution is not local processing.** These tools read files on your laptop, but the
> prompts and file content they send as context go to the model provider — Anthropic, OpenAI or
> Google — for inference, exactly as they would from a browser.
>
> **Do not use confidential, personal, sensitive, embargoed or institutionally restricted research
> data** unless your institution has approved that provider, that account type and its
> data-processing terms. If in doubt, use published material for the workshop exercises.

---

## Before you arrive — Windows users only

**Windows participants must do this before Day 1. It cannot be done in the lunch break**, because
it requires a restart of your computer and an administrator account.

macOS users: skip this Windows section, but **do complete the macOS version check below** before Day 1.

### Install WSL (Windows Subsystem for Linux)

WSL gives Windows a Linux terminal, which is what these tools expect. You need Windows 11, or
Windows 10 version 2004 / build 19041 or later.

1. **Open PowerShell as Administrator.** Right-click the Start button, choose
   "Terminal (Admin)" or "PowerShell (Admin)". *You must be an administrator on the machine —
   see below if you are not.*

2. **Run one command:**
   ```powershell
   wsl --install
   ```
   This enables the required Windows features, installs WSL2, and installs Ubuntu.

3. **Restart your computer** when prompted. This is not optional.

4. **After the restart, open Ubuntu yourself.** Open the Start menu, search for `Ubuntu`, and
   launch it. The first launch may take a few minutes while it finishes installing. Create a
   username and password when asked. **Write them down** — the password is invisible as you type
   it, and you will need it later.

You are ready when you can open Ubuntu and get a prompt. **You do not need to install anything else
in advance** — all three assistants below install themselves with a single command.

### If `wsl --install` does not work

- **It printed a wall of help text instead of installing.** WSL is partly installed already. Run
  `wsl --list --online`, then `wsl --install -d Ubuntu`.
- **The download sat at 0.0%.** Run `wsl --install --web-download -d Ubuntu`.
- **It failed on permissions, or you cannot open an Administrator PowerShell.** This is common on a
  university- or employer-managed laptop, where WSL may be disabled by policy or virtualization may
  be switched off in firmware. **You cannot fix either yourself, and it is not something you did
  wrong.** Use this browser fallback, which is sufficient for the workshop:
  **Browser fallback, which needs nothing installed on your laptop:**
  1. Sign in to a personal Google account and open [Google Cloud Shell](https://shell.cloud.google.com).
  2. Authorize it when prompted and wait for Cloud Shell to open. **If you chose Antigravity, use
     Open Editor → Terminal → New Terminal** — Google warns that `agy` does not display correctly in
     the basic Cloud Shell terminal.
  3. **Antigravity is already installed there** — just run `agy`. For Claude or Codex, install with
     the one-line command from the next section; Cloud Shell is Linux, so both install normally.
  4. If `agy` shows a sign-in URL and a code, open the URL in another browser tab, sign in, and
     paste the code back into `agy`.
  5. Run the `tulip` test below **in that same terminal**.

  Cloud Shell gives you 50 hours a week and 5 GB of storage that persists between sessions. **Its
  files live in Google's cloud, not on your laptop** — only put workshop material there that your
  institution permits. Note that Cloud Shell's preinstalled `gemini` command no longer accepts free,
  Google AI Pro or Google AI Ultra personal sign-in; use `agy` there instead.

  Pairing with a neighbour is fine for following along in the room, but it does **not** leave you
  with a working setup for Day 2 — use the browser fallback for that.

  **Test whichever route applies before Day 1**, and tell a facilitator if both are blocked.

### macOS users

macOS already gives you a terminal and needs nothing installed in advance. Open **Terminal** (in
Applications → Utilities, or press ⌘-Space and type "Terminal") and go straight to the next section.

**Check your version first if your Mac is not new:** choose **Apple menu → About This Mac**.
**Claude Code requires macOS 13 or newer; Codex requires macOS 12 or newer.**
- **macOS 13+** — any of the three.
- **macOS 12** — choose Codex, or test Antigravity before Day 1.
- **macOS 11 or older** — use the browser fallback above. Google's Antigravity CLI documentation
  does not publish a minimum macOS version, so it cannot be relied on as a catch-all for old Macs.

Better to find this out now than during lunch.

---

## Pick exactly one

Do not install all three. Read the table, pick one, and stop reading the others.

| your situation | pick | cost |
|---|---|---|
| You have **Claude Pro or Max**, or an invited Teams / Enterprise / Console account | **Claude Code** | already covered |
| You already use **ChatGPT** at any tier, including free | **Codex CLI** | already covered |
| You pay for neither, and have a **Google account** | **Antigravity CLI** | free on the $0/month Individual plan |

**Two of these cost nothing.** Codex works on a free ChatGPT account, and Antigravity is free on its
$0/month generally available Individual plan. You do not have to buy anything for this workshop.

> **All three install with one command and need nothing else** — no Node.js, no npm, no Homebrew.
> If a guide anywhere tells you to install Node first, it is describing the older, harder route.

---

## Install your one tool

### Option A — Claude Code

Needs Claude Pro or Max, or an invited Claude for Teams, Enterprise
or Console account. Console usage is billed separately from a consumer subscription.

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Then **open a new terminal window** so your PATH updates, and run:

```bash
claude
```

It will open a browser to sign in.

Docs: [code.claude.com/docs](https://code.claude.com/docs/en/setup)

### Option B — Codex CLI

Works with any ChatGPT account, including free.

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

Then **open a new terminal window** and run:

```bash
codex
```

Choose **Sign in with ChatGPT** and follow the browser prompts.

Docs: [developers.openai.com/codex/cli](https://developers.openai.com/codex/cli/)

### Option C — Antigravity CLI

Google's terminal assistant, free on its **$0/month Individual plan**. The command is `agy`.

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

Then **open a new terminal window** and run:

```bash
agy
```

It opens a browser to sign in with your Google account.

Docs: [antigravity.google/docs/cli](https://antigravity.google/docs/cli/getting-started/)

> ### 🟥 Do not choose Gemini CLI for personal Google-account sign-in
>
> On **18 June 2026** Google ended Gemini CLI service for **free-tier, Google AI Pro and Google AI
> Ultra individual sign-ins**, and pointed those users to Antigravity CLI. The package still
> installs and still prints a version — `npm install -g @google/gemini-cli` succeeds and
> `gemini --version` works — and then sign-in is rejected with *"This client is no longer supported
> for Gemini Code Assist for individuals."*
>
> Reinstalling, clearing your config or trying a different personal Google account will not help;
> all three consumer tiers went on the same day. **Gemini CLI does remain supported** for Gemini
> Code Assist Standard/Enterprise seats and for **API-key** authentication — those are different
> routes with their own costs. **For this workshop's no-key, personal-account route, use `agy`.**

---

## The finish line

**You are not done when it installs. You are done when it answers a question about a file.**

`--version` only proves a program is on your PATH. It says nothing about whether you are signed in,
whether your account has access, or whether the tool can read your files — and signing in is the
step that actually goes wrong. The Gemini CLI shutdown above is exactly this failure: it installs,
it reports a version, and it is useless.

Run this:

```bash
mkdir -p ~/rubase-workshop-test
cd ~/rubase-workshop-test
printf 'The workshop test word is tulip.\n' > workshop-test.txt
```

Start your tool — `claude`, `codex`, or `agy` — and type:

> `Read workshop-test.txt. Reply with only the test word. Do not edit anything.`

**You are done when it replies `tulip`.**

That one exchange proves the installation, your PATH, your login, network access to the model, and
the tool's ability to read local files. Nothing less proves all five.

### Checklist

**Windows, before Day 1**
- [ ] WSL installed, computer restarted
- [ ] Ubuntu username and password created and written down
- [ ] Ubuntu opens and gives you a prompt

**Everyone, by end of Day 1**
- [ ] One tool installed — `claude`, `codex` or `agy` prints a version
- [ ] **Signed in** — the tool started and completed its browser login
- [ ] **It replied `tulip`** — the test above passed

---

## When it goes wrong

**"command not found" straight after installing.**
Open a *new* terminal window. Installers change your PATH, and an already-open terminal does not
know about it yet.

**"command not found" in PowerShell on Windows.**
You are in the wrong terminal. These tools live inside WSL — open Ubuntu, not PowerShell.

**Still "command not found" in a new terminal.**
The install directory is not on your PATH. All three installers use `~/.local/bin`:
```bash
echo 'PATH="$HOME/.local/bin:$PATH"' >> ~/.profile
source ~/.profile
```
On macOS, whose default shell is zsh, also run once:
```bash
echo 'source ~/.profile' >> ~/.zprofile
source ~/.zprofile
```

**The browser did not open, or it showed a code instead of returning to the terminal.**
This is common in WSL, and both tools document a way through it:
- **Claude Code:** press `c` to copy the login URL, open it in your normal browser, sign in, and
  paste the code back at the `Paste code here if prompted` prompt.
- **Codex:** run `codex login --device-auth`, open the link it shows, sign in, and enter the
  one-time code. Device-code login is in beta and may need enabling in your ChatGPT security
  settings, or by your workspace administrator.

**It installed but will not sign in.**
Check that the account you are signing in with is the one that has access — a work Google account
where you meant to use a personal one is one possible cause. Ask a facilitator; this is fast to fix in
the room and slow to fix alone.

**`curl … | bash` is blocked on your machine.**
Some managed laptops refuse to pipe a downloaded script into a shell. **Use the Google Cloud Shell
browser fallback described above — it works from macOS just as well as from Windows.** If Cloud
Shell is blocked too, tell a facilitator before Day 1.

---

## Access and limits

*Checked 28 August 2026. All three vendors change these often — the linked pages are authoritative
and this table is not. Prices are vendor list prices in **USD**; ChatGPT Go's $8 is the US price and
is localized in some markets, and Anthropic's displayed prices exclude applicable tax. Check the
linked page for your own country before buying anything.*

| tool | what it costs | limits |
|---|---|---|
| **Antigravity CLI** (`agy`) | **$0/month** on the generally available Individual plan | Free users get a **basic weekly** rate limit. Google AI Pro and Ultra get higher baseline quotas refreshing every five hours, plus weekly limits. Google does not publish exact request counts; they vary with capacity and how much work you ask for. See [Antigravity plans](https://antigravity.google/docs/plans). |
| **Codex CLI** | **Included in every ChatGPT plan, including Free.** Go $8/mo, Plus $20/mo, Pro $100/mo (5×) or $200/mo (20×) | Free and Go are limited but usable; Plus and above are substantially higher. |
| **Claude Code** | **Claude Pro $20/mo** ($17/mo billed annually); Max from $100/mo | Rolling session and weekly limits, shared with your Claude usage. |

**None of these is unlimited.** Each vendor applies its own limits over a different window — do not
assume a daily reset. Use the linked page and the tool's own usage display. Hitting a limit
mid-exercise is a normal event rather than a fault; if it happens on Day 2, switch to a neighbour's
screen and carry on.

API billing is separate from subscription allowances unless a product explicitly says otherwise.

---

## Appendix — `llm`, for afterwards

**This is not one of the three choices above and it will not do what Day 2 needs.** Simon
Willison's `llm` is a query client for comparing models, not a coding agent that works with your
files and folders. It is genuinely useful for comparative method work, and it is the wrong thing to
be installing under time pressure. Come back to it later.

```bash
pip install llm
llm install llm-anthropic
llm install llm-gemini
llm keys set openai
llm keys set anthropic
llm keys set gemini
llm models
```

Run a model using an exact identifier from `llm models` — model names change often enough that any
list printed in a handout is wrong within months. To continue a conversation, use `llm -c "..."` for
the most recent one, or `llm --conversation ID "..."` for a specific logged conversation.

---

## A note on everything above

Model names, prices, limits and even whole products go stale fast. The previous version of this
guide recommended Gemini CLI's free tier as the default choice for anyone not already paying for
something — **that tier had been switched off for two months**, and the package's own documentation
still advertised it.

So: when something here disagrees with what the tool tells you, **the tool is right**. `--help`, the
linked vendor pages, and what actually happens when you sign in are the current authority. This page
is a snapshot, and it says when it was taken.
