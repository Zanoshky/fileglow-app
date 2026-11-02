#!/usr/bin/env python3
"""Builds the guide pages in docs/ from the bodies below. Run after any edit and commit docs/. Fails on any dash.

The look is the Zanoshky Standard, the same as fileglow.zanoski.com: docs/tokens.css is a copy of the house
tokens (never edit it here), docs/style.css the guide's own parts. Both are inlined into every page so no
stylesheet holds up the first paint. Every screenshot in docs/img is a real capture of the app."""
import re
from pathlib import Path

D = Path(__file__).parent / "docs"
REPO = "https://github.com/Zanoshky/fileglow-app"
PLAY = "https://play.google.com/store/apps/details?id=com.zanoshky.fileglow"
SITE = "https://fileglow.zanoski.com"
MAIL = "support@zanoski.com"
NAV = [("index.html", "Home"), ("guide.html", "Guide"), ("faq.html", "Questions"), ("report.html", "Report a bug")]

CSS = "\n".join((D / f).read_text() for f in ("tokens.css", "style.css"))
CSS = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S)
CSS = re.sub(r"\s*\n\s*", "\n", CSS).strip()


def shot(img, alt, name, line, lazy=True):
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high"'
    stem = img.rsplit(".", 1)[0]
    # The jpg stays for the README on GitHub; pages pick a small webp, about half the bytes.
    src = f'srcset="img/{stem}-300.webp 300w, img/{stem}-540.webp 540w" sizes="(min-width: 840px) 260px, 45vw"'
    return (f'<figure><img src="img/{img}" {src} alt="{alt}" width="540" height="1200" {load}>'
            f'<figcaption>{name}<span>{line}</span></figcaption></figure>')


def tv(img, alt, name, line):
    stem = img.rsplit(".", 1)[0]
    src = f'srcset="img/{stem}-480.webp 480w, img/{stem}-960.webp 960w" sizes="(min-width: 1140px) 540px, (min-width: 640px) 48vw, 100vw"'
    return (f'<li><figure class="tv"><img src="img/{img}" {src} alt="{alt}" width="960" height="540" loading="lazy" decoding="async">'
            f'<figcaption>{name}<span>{line}</span></figcaption></figure></li>')


def page(name, title, desc, body):
    for bad in ("\u2014", "\u2013", " - "):
        if bad in body:
            raise SystemExit(f"{name}: dash {bad!r} in copy")
    nav = "".join(f'<a class="hide-s" href="{h}"{" aria-current=\"page\"" if h == name else ""}>{t}</a>' for h, t in NAV)
    foot = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == name else ""}>{t}</a>' for h, t in
                   [(SITE, "Home"), ("index.html", "User guide"), ("faq.html", "Questions"), ("report.html", "Report a bug"),
                    (f"{SITE}/privacy", "Privacy"), (f"{SITE}/terms", "Terms")])
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · Fileglow user guide</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#f6f7f9" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
<meta property="og:title" content="{title} · Fileglow user guide">
<meta property="og:description" content="{desc}">
<link rel="icon" href="img/icon.svg" type="image/svg+xml">
<link rel="preload" href="fonts/jetbrains-mono-bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/inter-regular.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="bar">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="img/icon.svg" alt="" width="34" height="34"><span>Fileglow</span></a>
    <nav aria-label="Guide pages">{nav}<a class="key" href="{PLAY}">Get the app</a></nav>
  </div>
</header>
<main id="main" class="page">
  <div class="wrap">
{body}
  </div>
</main>
<footer>
  <div class="wrap">
    <span>Fileglow by <a href="https://zanoski.com">Marko Zanoski</a></span>
    <nav aria-label="Footer">{foot}</nav>
    <p class="lic">Guide text and images are shared under CC BY 4.0. The Fileglow app itself is proprietary.</p>
  </div>
</footer>
</body>
</html>
"""
    (D / name).write_text(html)
    print(name)


HOME_ALT = "Fileglow Home in Black: internal storage 30% used with a coloured bar, tiles for Photos, Videos, Audio, Docs, Download and Apps, Recent pictures and Jumps, with Home, Files, Find and Settings in the bar at the foot."
FILES_ALT = "Files on Internal storage: a list of folders such as Alarms, Android, Audiobooks, DCIM, Documents, Download, Movies and Music, each with its size and date, and the Select and More keys in the header."
MENU_ALT = "The More sheet of a folder: App data with Shizuku, New folder, New text file, Select all, Sort photos into folders, Find duplicates, Mirror to a share, Pin to Home and Refresh."
SETTINGS_ALT = "Settings: a Files card with Look, Home, files and trash, and Pro, an App card with Privacy and Help and feedback, then More apps, each row saying what is set now."
LOOK_ALT = "The Look page: Follow the phone, Light, Dark and Black tiles with Dark chosen, the Match my launcher switch, and launcher looks such as Blue light and Hyper drawn as little file lists."
PRIVACY_ALT = "Privacy: red ban chips No ads, No tracking, No analytics, No crash reports, No error reports, No account and No AI, then All files access, Internet, Photo locations and Network state with the reason for each."
DELETE_ALT = "A sheet over the folder list in Light: Delete for good? DCIM will be gone, not in the trash. This cannot be undone. With Cancel and Delete."
TERMINAL_ALT = "Fileglow Home in a blue Phosphor terminal look: internal storage 1.87 GB free, the kind tiles, Recent and Jumps in glowing mono type, with lowercase labels in the bar."

page("index.html", "Home", "The user guide for Fileglow, the private and reliable file manager for Android phones, tablets and TVs.", f"""
    <p class="lbl">User guide</p>
    <h1>Fileglow</h1>
    <p class="lede">A file manager built on privacy first, then reliability, then simplicity. No ads, no account, no tracking, and it never writes over your files. Free, with one optional Pro payment for the power tools. On phones, tablets, Android TV and Google TV.</p>
    <div class="keys">
      <a class="key filled" href="guide.html">Read the guide</a>
      <a class="key tonal" href="report.html">Report a bug or ask for a feature</a>
    </div>
    <ul class="shots">
      <li>{shot("home.jpg", HOME_ALT, "Home", "Storage, kinds, recent and jumps.", lazy=False)}</li>
      <li>{shot("files.jpg", FILES_ALT, "Files", "A list or a grid per folder.")}</li>
      <li>{shot("menu.jpg", MENU_ALT, "More", "Everything a folder can do.")}</li>
      <li>{shot("settings.jpg", SETTINGS_ALT, "Settings", "The last item in the bar.")}</li>
    </ul>
    <ul class="tvshots">
      {tv("tv-files.jpg", "Fileglow on a TV: the side rail on the left, a Holiday folder as a grid with one photo in the blue focus ring, and beside it a This file panel with Actions and Select over a large preview.", "On a TV", "A side rail and the remote.")}
      {tv("tv-actions.jpg", "A sheet from the right on a TV for the photo bled.jpg: Open in focus, then Open with, Copy, Move and Rename, over the dimmed folder.", "Actions", "Sheets come in from the right.")}
    </ul>
""")

page("guide.html", "Guide", "How to use Fileglow: Home, Files, Find and Settings, the file safety promise, the Pro tools and Android TV.", f"""
    <p class="lbl">Guide</p>
    <h1>How Fileglow works</h1>

    <div class="with-shot">
      <div class="doc">
        <h2>The first start</h2>
        <p>Fileglow asks for All files access, so it can show, copy, move and delete your files. It uses it for nothing else. On Android 10 and older, the storage permission does the same.</p>

        <h2>Four places in the bar</h2>
        <p>The bar at the foot of the screen has four places: Home, Files, Find and Settings. Tap one to go there; tap the one you are on to scroll back to its top. Settings is the last item, and its small pages open full screen with a Back arrow.</p>

        <h2>Home</h2>
        <p>Home shows your storage and what fills it, tiles for Photos, Videos, Audio, Docs, Download and Apps, the files you changed last under Recent, and the folders you open most under Jumps. Folders you pin, your network shares and, with Pro, your workspaces get their own cards. A card ends in See all; See all under Recent opens the full Recent list. The trash is a row on Home too.</p>
      </div>
      {shot("home.jpg", HOME_ALT, "Home", "Storage, kinds, recent and jumps.")}
    </div>

    <div class="with-shot">
      <div class="doc">
        <h2>Files</h2>
        <p>Files opens your storage as folders. Each folder is a list or a grid, sorted by name, date, size or type, and Fileglow remembers the choice per folder (Sort and view, in the folder's More). On a tablet or a phone on its side you get columns: the folder and a preview beside it.</p>
        <p>Tap a file to open it. Fileglow previews photos, videos, PDFs, music, text, code and what is inside a zip. Touch and hold a row, or tap the tick in the header, to pick files; tap more rows to add them.</p>
        <dl class="rows plate">
          <div><dt>On a file or picked files</dt><dd>Open with, Send to another app, Copy, Move, Rename, Zip, Unzip here, Move to the trash, Delete for good, Details, Copy the path and Pin to Home.</dd></div>
          <div><dt>Copy and move</dt><dd>Pick Copy or Move, open the folder you want, then tap Paste here (or Move here).</dd></div>
          <div><dt>Rename many</dt><dd>Pick several files and Rename: one name a line, or find and replace.</dd></div>
          <div><dt>In a folder's More</dt><dd>New folder, New text file, Select all, Sort and view, Refresh, and the Pro tools for that folder.</dd></div>
        </dl>
      </div>
      {shot("menu.jpg", MENU_ALT, "More", "What a folder can do.")}
    </div>

    <div class="with-shot">
      <div class="doc">
        <h2>It never writes over a file</h2>
        <p>Your files may be the only copy of your photos, so not losing them comes before everything else. All of this is free.</p>
        <dl class="rows plate">
          <div><dt>Names already here</dt><dd>When a paste meets names that are taken, Fileglow asks once: Keep both (the new ones get a number), Skip them, or Replace. Replace keeps the old file in the trash and merges folders; it is only offered on the phone's own storage.</dd></div>
          <div><dt>Trash and Undo</dt><dd>Move to the trash puts things in a trash on that volume, kept 7, 30 or 90 days (30 unless you change it). After a job a note offers Undo, and one Undo brings everything back.</dd></div>
          <div><dt>Delete for good</dt><dd>Always asks first, and cannot be undone.</dd></div>
          <div><dt>Checked copies</dt><dd>A copy is checked whole before its original is removed, and one file job runs at a time.</dd></div>
          <div><dt>A copy was cut short</dt><dd>If Fileglow was closed while it copied, zipped or unzipped, the half made copy goes to the trash next time, with a note. The originals are never touched.</dd></div>
        </dl>
      </div>
      {shot("delete.jpg", DELETE_ALT, "Delete for good", "The one step that always asks.")}
    </div>

    <div class="doc">
      <h2>Find</h2>
      <p>Find, in the bar, opens the jump box. Type a few letters of a folder or file name: folders come first, and a found file opens its folder with the file under the cursor. Type a folder path and it goes straight there. With Pro, Find also matches the words inside text, code and Office files.</p>

      <h2>For other apps</h2>
      <p>When another app asks you to pick a file, Fileglow can be the picker: tap a file to hand it back, or pick several with Select. In the share sheet it shows as Save a copy: open a folder and the shared files are saved there, with one Undo.</p>
    </div>

    <div class="doc">
      <h2>Pro</h2>
      <p>Fileglow is free with no ads. Pro is one optional payment through Google Play, yours for good: no subscription and no account. Browsing, previews, copy and move with Undo, the trash, zip and unzip, renaming many files at once, Find and Save a copy stay free, and so does every safety check. A Pro control says Pro under its name and opens the list below.</p>
      <dl class="rows plate">
        <div><dt>Network shares</dt><dd>Your NAS, PC or server over SMB, SFTP, FTP and WebDAV, as folders. Add one in Settings, Pro, Network shares and cloud drives, and press Try it before Save.</dd></div>
        <div><dt>Dropbox</dt><dd>Your Dropbox, as folders. You sign in on Dropbox's own page.</dd></div>
        <div><dt>Films from your shares</dt><dd>Play here plays them straight from the share, with subtitles beside the film; or Play in another app, or Fetch it whole, then open.</dd></div>
        <div><dt>Wi-Fi transfer</dt><dd>Files to and from a computer's browser. Off until you start it: open the address shown on the computer and type the PIN. One computer at a time; it stops on its own after 15 idle minutes, five wrong PINs, or when you leave Wi-Fi.</dd></div>
        <div><dt>Vault</dt><dd>Files sealed with a password of 15 or more characters and hidden from other apps. It locks two minutes after you leave Fileglow. A vault you made opens with its password, with or without Pro.</dd></div>
        <div><dt>Archives as folders</dt><dd>Open a zip, 7z, rar or tar as a folder, read only. Copy files out to change them.</dd></div>
        <div><dt>Search inside files</dt><dd>Find files by the words in them, from a private index on the phone.</dd></div>
        <div><dt>Two tiles</dt><dd>Two folders at once, side by side on a wide screen and stacked on a phone, with copy or move to the other tile; save them as a workspace on Home.</dd></div>
        <div><dt>Folder mirrors</dt><dd>A phone folder kept copied to a folder on your share, on Wi-Fi while charging. Each file is read back and checked, and nothing is ever deleted.</dd></div>
        <div><dt>Find duplicates</dt><dd>Files with the very same bytes, checked whole. The oldest stays; the rest go to the trash, so Undo puts them back.</dd></div>
        <div><dt>Sort photos</dt><dd>Into folders by where and when each was taken, from a place list inside the app. A preview shows the folder tree first and nothing moves until you press Sort; Put photos back, in the folder's More, undoes it, even days later.</dd></div>
        <div><dt>App data with Shizuku</dt><dd>Android/data and obb through the Shizuku app, on Android 11 and newer.</dd></div>
      </dl>
    </div>

    <div class="with-shot">
      <div class="doc">
        <h2>Settings</h2>
        <p>Settings is the last item in the bar: cards of rows, each saying what is set now. A row opens its own small page; the arrow at its top left takes you back.</p>
        <dl class="rows plate">
          <div><dt>Look</dt><dd>Follow the phone (Light by day, Dark at night), Light, Dark, or Black, true black for OLED. With Phosphor or Hyprtile as your home screen, Match my launcher takes its look; or pick a ready launcher look, and fine tune the theme, picture, glass and CRT tube.</dd></div>
          <div><dt>Home, files and trash</dt><dd>Show recent on Home, folders first, hidden files, light up the places you use most, the preview column, the text size of the lists, ask before moving to the trash, how long the trash keeps things, and Open the trash.</dd></div>
          <div><dt>Pro</dt><dd>The Pro tools and the buy key, then Network shares and cloud drives, Wi-Fi transfer and Folder mirrors.</dd></div>
          <div><dt>Privacy</dt><dd>The promises as red ban chips, every permission Fileglow holds and why, how shares and transfers are kept safe, and the privacy policy in full.</dd></div>
          <div><dt>Help and feedback</dt><dd>This guide, the report page, the privacy policy and the credits.</dd></div>
          <div><dt>More apps</dt><dd>Hyprtile and Phosphor, the launchers whose looks Fileglow can wear.</dd></div>
          <div><dt>Support the developer</dt><dd>If Fileglow helps you, you can support it: Buy me a coffee opens buymeacoffee.com/zanoshky.</dd></div>
          <div><dt>About</dt><dd>The version. Your files go only where you send them: Fileglow has no server of its own.</dd></div>
        </dl>
      </div>
      {shot("settings.jpg", SETTINGS_ALT, "Settings", "Cards of rows that say what is set.")}
    </div>

    <div class="with-shot">
      <div class="doc">
        <h2>Your launcher's look</h2>
        <p>With Hyprtile as your home screen you get tiles with gradient borders; with Phosphor, a glowing terminal on true black. Without them, pick Light, Dark, Black or any of 84 themes in Settings, Look.</p>
      </div>
      {shot("terminal.jpg", TERMINAL_ALT, "A terminal look", "From Phosphor, the launcher.")}
    </div>

    <div class="doc">
      <h2>On Android TV and Google TV</h2>
      <p>Fileglow runs on Android TV and Google TV too: open files from a USB drive in other apps, copy, move and delete with the remote, and reach your network shares.</p>
      <dl class="rows plate">
        <div><dt>The side rail</dt><dd>Home, Files, Find and Settings sit in a rail on the left instead of the bar. Right from the rail goes back to the row you left.</dd></div>
        <div><dt>The remote</dt><dd>Move with the arrows; a blue ring shows where you are. OK on a row opens it. Beside the files a panel for This file or This folder holds Actions and Select; the Menu key opens Actions too. In Select, OK on a row picks it.</dd></div>
        <div><dt>Sheets from the right</dt><dd>Menus and questions slide in from the right side. Back closes them and puts you where you were.</dd></div>
        <div><dt>Open with</dt><dd>Fileglow lists the apps on the TV that open the file. A TV has no share sheet, so Open with sends a file to one app.</dd></div>
        <div><dt>USB drives</dt><dd>Plug in a USB drive and it shows under Drives on Home, above This TV.</dd></div>
        <div><dt>Open on your phone</dt><dd>A TV has no browser, so links in Settings (this guide, the report page, the privacy policy) open a QR code. Point your phone's camera at it to open the page there.</dd></div>
        <div><dt>Look</dt><dd>Dark is where a TV starts; Follow the phone reads Follow the TV. Match my launcher and installing apps are not on a TV.</dd></div>
      </dl>
    </div>
    <ul class="tvshots">
      {tv("tv-home.jpg", "Fileglow Home on a TV with the side rail, a Drives card with This TV in focus and the line Plug in a USB drive and it shows here, Recent pictures, the kind tiles and Jumps.", "Home on a TV", "Drives, recent and jumps.")}
      {tv("tv-files.jpg", "A Holiday folder on a TV as a grid with one photo in the blue focus ring, and beside it a This file panel with Actions and Select over a large preview of a lake.", "Files", "Actions and Select beside the files.")}
      {tv("tv-open-with.jpg", "A sheet from the right on a TV titled Open Train tickets.pdf with, offering Pure Peek, over the dimmed Documents folder.", "Open with", "The apps on the TV that open it.")}
      {tv("tv-link-qr.jpg", "Help and feedback on a TV under a sheet from the right titled User guide, with a QR code, Open on your phone and the address zanoshky.github.io/fileglow-app, and a Done key.", "Open on your phone", "Links become QR codes.")}
    </ul>

    <div class="with-shot">
      <div class="doc">
        <h2>Privacy</h2>
        <p>No ads, no account, no tracking, no analytics, no crash reports and no AI. Fileglow goes online only for what you set up: your own shares and Dropbox, Wi-Fi transfer to your computer, and the Google Play purchase. Sort photos finds places with a list inside the app, so nothing about your photos goes online. Share passwords are kept encrypted with a key in Android's keystore, and an SFTP server whose key changed is refused. Fileglow never asks for location, contacts, camera or microphone.</p>

        <h2>Accessibility</h2>
        <p>TalkBack labels on every row, touch targets of at least 48 dp, and everything fits at 200% text size. The text size of the lists has its own setting in Home, files and trash.</p>
      </div>
      {shot("privacy.jpg", PRIVACY_ALT, "Privacy", "Every promise and permission.")}
    </div>
""")

page("faq.html", "Questions", "Answers to common questions about Fileglow, and what to try when something does not work.", f"""
    <div class="doc">
    <p class="lbl">Questions</p>
    <h1>Questions and fixes</h1>

    <h2>Why does it need All files access?</h2>
    <p>To show, copy, move and delete your files. It is used for nothing else. On Android 10 and older, the storage permission does the same.</p>

    <h2>Does Fileglow go online?</h2>
    <p>Only for what you set up: your own network shares and Dropbox, Wi-Fi transfer to your computer, and Google Play for the Pro purchase. Fileglow has no server of its own. See the <a href="{SITE}/privacy">privacy policy</a>.</p>

    <h2>I deleted something by mistake</h2>
    <p>Tap Undo in the note that shows after the job, or open the trash from Home (or Settings, Home, files and trash, Open the trash). Things stay there 7, 30 or 90 days, as you set. Only Delete for good skips the trash, and it always asks first. Network shares have no trash, so be careful there.</p>

    <h2>It says a copy was cut short</h2>
    <p>Fileglow was closed while it copied, zipped or unzipped. The half made copy was put in the trash and the originals were not touched, so you can copy or move again.</p>

    <h2>My network share will not connect</h2>
    <p>Fileglow says why in plain words. Could not find the server: check the address. It turned the connection down: check the address, the port, and that sharing is on. It did not answer: check that it is on and on the same network as the phone. Also check the user name, the password and the shared folder's name. An SFTP server whose key changed is refused on purpose: if you reinstalled the server, remove the share and add it again.</p>

    <h2>Where are Google Drive and OneDrive?</h2>
    <p>Not in Fileglow yet. Dropbox is the cloud drive you can connect today, with Pro.</p>

    <h2>I forgot my vault password</h2>
    <p>Nobody can open the vault without it, us included. That is what keeps it safe. Pick a password you can keep: a few words make a good one.</p>

    <h2>I bought Pro but it is still locked</h2>
    <p>Fileglow checks the purchase with Google Play. Make sure the Play Store is signed in with the Google account that bought Pro, then open Settings, Pro again.</p>

    <h2>Sort photos made no place folders</h2>
    <p>Only photos that carry a place get one. Fileglow may ask for Photo locations, only when no photo shows its place. Sort photos works on the phone's own storage; copy photos there first. Put photos back, in the folder's More, undoes a sort.</p>

    <h2>A folder mirror did not run</h2>
    <p>Mirrors run on Wi-Fi while the phone is charging, about every six hours; Mirror now runs one on Wi-Fi. If Android stops a run, the next one carries on. Nothing is ever deleted on either side.</p>

    <h2>Wi-Fi transfer stopped</h2>
    <p>It stops on its own after 15 idle minutes, after five wrong PINs, or when the phone leaves Wi-Fi, and it lets in one computer at a time. Start it again for a fresh PIN.</p>

    <h2>I cannot install an app file</h2>
    <p>Fileglow does not install apps itself. Install with Android's installer opens the folder in the phone's Files app; tap the file there. On a TV, use an app that installs apps, or get the app from Google Play.</p>

    <h2>Android/data is empty</h2>
    <p>Android keeps it closed. With Pro, App data with Shizuku opens it on Android 11 and newer, once Shizuku is installed and running and Fileglow is allowed in its list of apps.</p>

    <h2>No launcher look</h2>
    <p>Match my launcher needs Phosphor or Hyprtile as your home screen. Without them, pick a ready look in Settings, Look.</p>

    <h2>On a TV, how do I open a link?</h2>
    <p>A TV has no browser, so a link opens a QR code. Point your phone's camera at it to open the page on your phone.</p>
    </div>
""")

page("report.html", "Report a bug", "How to report a Fileglow bug or ask for a feature on GitHub.", f"""
    <div class="doc" style="max-width:none">
    <p class="lbl">Report</p>
    <h1>Report a bug or ask for a feature</h1>
    <p style="margin-top:16px">Found something broken, or have an idea? Tell us on GitHub. A free GitHub account is all you need.</p>
    <div class="cards">
      <div class="card plate"><h2 class="h3">Bug report</h2><p>Something does not work, looks wrong, or crashes.</p><a class="key filled" href="{REPO}/issues/new?template=bug_report.yml">Report a bug</a></div>
      <div class="card plate"><h2 class="h3">Feature request</h2><p>A tool or something you would like Fileglow to do.</p><a class="key tonal" href="{REPO}/issues/new?template=feature_request.yml">Ask for a feature</a></div>
    </div>
    </div>
    <div class="doc">
    <h2>Before you write</h2>
    <ul>
      <li>Search the <a href="{REPO}/issues">open issues</a> first. If yours is there, add a thumbs up or a comment.</li>
      <li>Check the <a href="faq.html">questions and fixes</a> page.</li>
      <li>One problem per report makes it faster to fix.</li>
    </ul>

    <h2>What helps</h2>
    <dl class="rows plate">
      <div><dt>App version</dt><dd>Settings, About, or Android settings, Apps, Fileglow.</dd></div>
      <div><dt>Device and Android version</dt><dd>Android settings, About phone (on a TV, Settings, System, About).</dd></div>
      <div><dt>Which screen or feature</dt><dd>Home, Files, Find, a file action, the trash, a share, a Pro tool, Settings, or the TV rail and remote.</dd></div>
      <div><dt>Steps</dt><dd>What you did, one step per line, so we can do the same.</dd></div>
      <div><dt>Expected and actual</dt><dd>What you thought would happen, and what happened.</dd></div>
      <div><dt>A picture or a recording</dt><dd>A screenshot or a short screen recording. Drag it into the form.</dd></div>
    </dl>
    <p style="margin-top:16px">Issues on GitHub are public. Before you attach a screenshot, crop or cover anything private: file names, share addresses and photos.</p>

    <h2>Other ways</h2>
    <p>Prefer not to use GitHub? Write to <span class="mail">{MAIL}</span> (<a href="mailto:{MAIL}">write an email</a>).</p>
    </div>
""")
