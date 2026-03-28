-- Push to existing GitHub repo: kingdavid200/Yananai_Intranet
-- Just paste your Personal Access Token below

set instructions to "Enter your GitHub Personal Access Token:" & return & return & "Create one at: github.com/settings/tokens/new" & return & "(needs 'repo' scope)"

set ghToken to text returned of (display dialog instructions default answer "" buttons {"Cancel", "Push to GitHub"} default button "Push to GitHub")

try
	set pushCmd to "cd ~/Desktop/yananai_intranet && git init && git branch -M main && git add -A && git commit -m 'Initial commit - Project Yananai Intranet' 2>/dev/null; git remote remove origin 2>/dev/null; git remote add origin 'https://kingdavid200:" & ghToken & "@github.com/kingdavid200/Yananai_Intranet.git' && git push -u origin main --force 2>&1"
	
	set pushResult to do shell script pushCmd
	
	display dialog "Code pushed to GitHub!" & return & return & "Repo: github.com/kingdavid200/Yananai_Intranet" & return & return & "Next step: deploy on Railway." buttons {"Done"} default button "Done"
	
on error errMsg number errNum
	if errNum is -128 then return
	display dialog "Error: " & errMsg buttons {"OK"} default button "OK" with icon stop
end try
