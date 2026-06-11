#!/usr/bin/env python3
"""
Auto-refresh data and commit to GitHub
This script can be run manually to fetch latest data for today
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_command(cmd, description):
    """Run shell command and report status"""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    if result.returncode != 0:
        print(f"❌ Failed with return code {result.returncode}")
        return False
    
    print(f"✅ {description} - Complete")
    return True

def main():
    print("\n" + "="*60)
    print("🇮🇳 NSE Stock Market Analysis - Data Refresh")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
    
    # Step 1: Update top 250 stocks (optional - run weekly)
    if '--update-stocks' in sys.argv:
        if not run_command('python fetch_top_stocks.py', 'Updating Top 250 Stocks by Volume'):
            sys.exit(1)
    
    # Step 2: Run daily analysis
    if not run_command('python indian_stock_analyzer_250.py', 'Running Daily Analysis for 250 Stocks'):
        sys.exit(1)
    
    # Step 3: Commit results to GitHub
    print(f"\n{'='*60}")
    print("▶ Committing results to GitHub")
    print(f"{'='*60}")
    
    run_command('git config --local user.email "stock-bot@github.com"', 'Configure git email')
    run_command('git config --local user.name "Stock Bot"', 'Configure git name')
    run_command('git add data/daily_analysis/', 'Stage daily analysis files')
    
    today = datetime.now().strftime('%Y-%m-%d')
    commit_msg = f"🔍 Daily analysis - {today} {datetime.now().strftime('%H:%M:%S')}"
    
    result = subprocess.run(
        f'git commit -m "{commit_msg}"',
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"✅ Committed: {commit_msg}")
        
        # Push to GitHub
        if run_command('git push', 'Pushing to GitHub'):
            print("\n" + "="*60)
            print("✅ ALL COMPLETE!")
            print("="*60)
            print(f"📊 View dashboard: dashboard.html")
            print(f"📁 Data saved to: data/daily_analysis/")
            print(f"✓ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
            print("="*60)
        else:
            print("⚠️ Commit created but push failed")
    else:
        if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
            print("ℹ️  No changes to commit (data may be the same as last run)")
        else:
            print(f"❌ Commit failed: {result.stderr}")

if __name__ == "__main__":
    main()
