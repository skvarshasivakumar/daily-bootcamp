Claude
AI_Engineering_Bootcamp_Days_1-10_EXPANDED.txt
AI_Engineering_Bootcamp_Days_1-10_
EXPANDED
.txt
TXT
help me ceate a daily mailed project wth all tis ike satrt from day 7 8 9 10 and then 1 2 3 4 5 6 .. sned to me in mail everyday... lets sautomate the process of sending mail.. give me a tech stack to develeoper this app make all tech stack simpla.e.

Ran 5 commands, read a file, shared files
I built the project and packaged it as daily-bootcamp.zip. I tested it with dry runs only, because I can’t send real email from here.

Order of emails: Day 7, 8, 9, 10, then 1, 2, 3, 4, 5, 6. The 11th email is a bonus made from the DevMind project, extra notes and glossary at the end of your file. After that the cycle starts again.

Tech stack

Need	Choice
Language	Python 3 (standard library only, nothing to install)
Sending email	Gmail SMTP with an App Password
Daily automation	GitHub Actions cron (free, no server needed)
Lesson content	Plain .txt files, one per day, in content/
What’s in the zip

send_daily.py picks today’s lesson from the date and emails it as plain text plus a readable HTML version.
content/ has your guide already split into day01.txt to day10.txt and day11_bonus.txt.
.github/workflows/daily.yml runs it every day at 7:00 AM India time. You can change the time by editing the cron line.
README.md has the setup steps and .env.example shows the settings you need.
Setup (about 10 minutes)

In your Google account, turn on 2-Step Verification, then create an App Password at myaccount.google.com/apppasswords.
Create a private GitHub repo and push the unzipped folder to it.
In the repo, go to Settings → Secrets and variables → Actions and add:
secrets GMAIL_ADDRESS, GMAIL_APP_PASSWORD and TO_EMAIL
a variable START_DATE (for example 2026-10-26, the day Day 7 should arrive)
Open the Actions tab and run “Daily bootcamp email” manually to test.
The script doesn’t send anything before START_DATE. If you’d rather use a different email provider or a different send time, tell me and I’ll change it.

Daily bootcamp
ZIP
in github how t setup workflow..? o triggerr everydY

Explaining simple steps to set up a GitHub workflow.
Explaining simple steps to set up a GitHub workflow.
You don’t need to create the workflow by hand. It’s already in the zip as .github/workflows/daily.yml, and GitHub runs it automatically once the file is in your repo. The only thing that matters is the folder structure.

1. Create the repo

Go to github.com → New repository.
Name it something like daily-bootcamp and choose Private.
Click Create repository.
2. Upload the files

Unzip daily-bootcamp.zip first. Then use whichever option is easier.

Option A, no git needed:

On the new repo page, click uploading an existing file.
Drag in the contents of the unzipped folder: send_daily.py, README.md, the content folder and the .github folder.
The .github folder is hidden on some computers. On Windows, turn on View → Hidden items. On Mac, press Cmd+Shift+. in Finder.
Click Commit changes.
Option B, git:

bash
cd daily-bootcamp
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/daily-bootcamp.git
git push -u origin main
Afterwards, check that the repo shows .github/workflows/daily.yml at the top level. If it’s inside another folder, GitHub won’t see it.

3. Add your secrets

Go to the repo’s Settings → Secrets and variables → Actions.
On the Secrets tab, click New repository secret and add three, one at a time:
GMAIL_ADDRESS: your Gmail address
GMAIL_APP_PASSWORD: the 16-character App Password from Google
TO_EMAIL: where you want to receive the lessons
On the Variables tab, click New repository variable. Add START_DATE with the value 2026-10-26, or whichever day you want Day 7 to arrive.
4. Test it now

Open the Actions tab. If GitHub asks, click “I understand my workflows, enable them”.
Click Daily bootcamp email in the left list, then Run workflow → Run workflow.
Wait about 30 seconds. A green tick means it worked and you should have an email.
If you test before START_DATE, it will say “nothing to send”. That’s expected, so set START_DATE to today to test.
5. The daily trigger

You don’t do anything here. The line cron: "30 1 * * *" in the file makes GitHub run it every day at 01:30 UTC, which is 7:00 AM India time. GitHub’s scheduler can be late by 5 to 30 minutes, which is normal.

Three things to know:

If a repo has no activity for 60 days, GitHub may pause scheduled workflows. You’d get a notice, and you can re-enable it with one click in the Actions tab.
Scheduled runs only work from the default branch (main).
If a run fails, check the red cross in Actions and click into it. The most common cause is a wrong App Password or a typo in a secret name.
If anything fails, paste the error text from the Actions log and I’ll help you fix it.


Claude works directly with your codebase




Claude is AI and can make mistakes. Please double-check responses.
Daily bootcamp · ZIP
Daily bootcamp
ZIP
No preview available

Claude finished the response
