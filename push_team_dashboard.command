#!/bin/bash
cd "$(dirname "$0")"
echo "=== Pushing team dashboard update to GitHub ==="
echo ""
git add accounts/migrations/0002_add_team_field.py accounts/models.py accounts/views.py templates/dashboard.html templates/base.html create_superuser.py push_team_dashboard.command
git commit -m "Role-based dashboard: team field migration, views, and templates"
echo ""
echo "Pushing to GitHub..."
git push
echo ""
echo "Done! Railway will auto-redeploy."
echo ""
read -p "Press Enter to close..."
