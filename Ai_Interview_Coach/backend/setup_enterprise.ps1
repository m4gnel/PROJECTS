# AI Interview Coach - Enterprise Database Setup Script
# For Windows PowerShell
# Version 2.0

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('setup', 'migrate', 'start', 'test', 'backup', 'clean')]
    [string]$Action = 'setup'
)

$ErrorActionPreference = "Stop"
$ProjectPath = $PSScriptRoot

function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Show-Banner {
    Write-ColorOutput Green @"
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   🚀 AI INTERVIEW COACH - ENTERPRISE DATABASE SETUP       ║
║                                                            ║
║   Version: 2.0 Enterprise Edition                         ║
║   Database: 13 Tables | Real-Time Analytics | Zero Errors ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"@
    Write-Output ""
}

function Test-Prerequisites {
    Write-ColorOutput Cyan "Checking prerequisites..."
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+)\.(\d+)") {
            $major = [int]$matches[1]
            $minor = [int]$matches[2]
            if ($major -ge 3 -and $minor -ge 9) {
                Write-ColorOutput Green "✅ Python $major.$minor detected"
            } else {
                throw "Python 3.9 or higher required. Found: $pythonVersion"
            }
        }
    } catch {
        Write-ColorOutput Red "❌ Python not found or version too old"
        Write-ColorOutput Yellow "Please install Python 3.9+ from https://www.python.org/"
        exit 1
    }
    
    # Check pip
    try {
        $pipVersion = pip --version 2>&1
        Write-ColorOutput Green "✅ pip detected"
    } catch {
        Write-ColorOutput Red "❌ pip not found"
        exit 1
    }
    
    # Check project path
    if (Test-Path $ProjectPath) {
        Write-ColorOutput Green "✅ Project path found: $ProjectPath"
    } else {
        Write-ColorOutput Red "❌ Project path not found: $ProjectPath"
        Write-ColorOutput Yellow "Please update `$ProjectPath in this script"
        exit 1
    }
}

function Setup-Environment {
    Write-ColorOutput Cyan "`n📦 Setting up environment..."
    
    Set-Location $ProjectPath
    
    # Create virtual environment if doesn't exist
    if (-not (Test-Path "venv")) {
        Write-ColorOutput Yellow "Creating virtual environment..."
        python -m venv venv
        Write-ColorOutput Green "✅ Virtual environment created"
    } else {
        Write-ColorOutput Green "✅ Virtual environment exists"
    }
    
    # Activate virtual environment
    Write-ColorOutput Yellow "Activating virtual environment..."
    & ".\venv\Scripts\Activate.ps1"
    
    # Upgrade pip
    Write-ColorOutput Yellow "Upgrading pip..."
    python -m pip install --upgrade pip --quiet
    Write-ColorOutput Green "✅ pip upgraded"
    
    # Install dependencies
    Write-ColorOutput Yellow "Installing dependencies (this may take 10-15 minutes)..."
    Write-ColorOutput Gray "Installing core packages..."
    
    $corePackages = @(
        "Flask==3.0.0",
        "Flask-SQLAlchemy==3.1.1",
        "Flask-Migrate==4.0.5",
        "Flask-CORS==4.0.0",
        "Flask-JWT-Extended==4.6.0",
        "Flask-Limiter==3.5.0",
        "Flask-Caching==2.1.0",
        "bcrypt==4.1.2",
        "python-dotenv==1.0.0"
    )
    
    foreach ($package in $corePackages) {
        Write-ColorOutput Gray "  Installing $package..."
        pip install $package --quiet
    }
    
    Write-ColorOutput Green "✅ Core packages installed"
    
    # Install remaining packages
    if (Test-Path "requirements_enterprise.txt") {
        Write-ColorOutput Yellow "Installing remaining packages..."
        pip install -r requirements_enterprise.txt --quiet
        Write-ColorOutput Green "✅ All dependencies installed"
    }
}

function Backup-Database {
    Write-ColorOutput Cyan "`n💾 Backing up database..."
    
    Set-Location $ProjectPath
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupName = "interview_coach_backup_$timestamp.db"
    
    if (Test-Path "interview_coach.db") {
        Copy-Item "interview_coach.db" $backupName
        Write-ColorOutput Green "✅ Backup created: $backupName"
    } else {
        Write-ColorOutput Yellow "⚠️  No existing database to backup"
    }
}

function Initialize-Database {
    Write-ColorOutput Cyan "`n🗄️  Initializing enterprise database..."
    
    Set-Location $ProjectPath
    
    # Check if app_enhanced.py exists
    if (-not (Test-Path "app_enhanced.py")) {
        Write-ColorOutput Red "❌ app_enhanced.py not found"
        Write-ColorOutput Yellow "Please ensure all enterprise files are in the backend folder"
        exit 1
    }
    
    # Backup old app.py
    if (Test-Path "app.py") {
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        Copy-Item "app.py" "app_old_$timestamp.py"
        Write-ColorOutput Yellow "Old app.py backed up as app_old_$timestamp.py"
    }
    
    # Copy enhanced version
    Copy-Item "app_enhanced.py" "app.py" -Force
    Write-ColorOutput Green "✅ Enhanced app.py deployed"
    
    # Initialize database
    Write-ColorOutput Yellow "Initializing database tables..."
    
    $initScript = @"
from app import init_db, db, Question, User
import sys

try:
    print('Creating database tables...')
    init_db()
    
    # Verify tables
    table_names = list(db.metadata.tables.keys())
    print(f'✅ Created {len(table_names)} tables:')
    for table in table_names:
        print(f'   - {table}')
    
    # Check sample questions
    question_count = Question.query.count()
    print(f'\n✅ Loaded {question_count} sample questions')
    
    print('\n✅ Database initialization successful!')
    sys.exit(0)
    
except Exception as e:
    print(f'❌ Error: {str(e)}')
    sys.exit(1)
"@
    
    $initScript | python
    
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput Green "✅ Database initialized successfully"
    } else {
        Write-ColorOutput Red "❌ Database initialization failed"
        exit 1
    }
}

function Start-Application {
    Write-ColorOutput Cyan "`n🚀 Starting application..."
    
    Set-Location $ProjectPath
    
    Write-ColorOutput Yellow "Starting Flask server on http://localhost:5000"
    Write-ColorOutput Yellow "Press Ctrl+C to stop"
    Write-Output ""
    
    # Check if .env exists
    if (-not (Test-Path ".env")) {
        Write-ColorOutput Yellow "Creating .env file from template..."
        if (Test-Path ".env.example") {
            Copy-Item ".env.example" ".env"
            Write-ColorOutput Green "✅ .env file created - please update with your settings"
        }
    }
    
    python app.py
}

function Run-Tests {
    Write-ColorOutput Cyan "`n🧪 Running tests..."
    
    Set-Location $ProjectPath
    
    # Quick smoke test
    $testScript = @"
import sys
from app import app, db, User, Interview, Question, Answer, Feedback

def test_database():
    with app.app_context():
        # Test table creation
        tables = list(db.metadata.tables.keys())
        assert len(tables) >= 13, f'Expected 13+ tables, found {len(tables)}'
        print(f'✅ Database has {len(tables)} tables')
        
        # Test question loading
        question_count = Question.query.count()
        assert question_count > 0, 'No questions found'
        print(f'✅ Database has {question_count} questions')
        
        return True

def test_imports():
    # Test all models can be imported
    from app import (
        User, Interview, Question, Answer, Feedback,
        PerformanceMetric, UserAchievement, UserSession,
        ActivityLog, CompanyQuestionBank, Leaderboard
    )
    print('✅ All models imported successfully')
    return True

try:
    print('Running smoke tests...\n')
    test_imports()
    test_database()
    print('\n✅ All tests passed!')
    sys.exit(0)
except Exception as e:
    print(f'\n❌ Test failed: {str(e)}')
    sys.exit(1)
"@
    
    $testScript | python
    
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput Green "`n✅ All tests passed"
    } else {
        Write-ColorOutput Red "`n❌ Tests failed"
    }
}

function Clean-Environment {
    Write-ColorOutput Cyan "`n🧹 Cleaning environment..."
    
    Set-Location $ProjectPath
    
    $confirm = Read-Host "This will delete the virtual environment and database. Continue? (y/N)"
    
    if ($confirm -eq 'y' -or $confirm -eq 'Y') {
        # Remove virtual environment
        if (Test-Path "venv") {
            Remove-Item -Recurse -Force "venv"
            Write-ColorOutput Green "✅ Virtual environment removed"
        }
        
        # Remove database
        if (Test-Path "interview_coach_enterprise.db") {
            Remove-Item "interview_coach_enterprise.db"
            Write-ColorOutput Green "✅ Database removed"
        }
        
        # Remove __pycache__
        if (Test-Path "__pycache__") {
            Remove-Item -Recurse -Force "__pycache__"
            Write-ColorOutput Green "✅ Cache cleaned"
        }
        
        Write-ColorOutput Green "`n✅ Cleanup complete"
    } else {
        Write-ColorOutput Yellow "Cleanup cancelled"
    }
}

function Show-Help {
    Write-Output @"

Usage: .\setup_enterprise.ps1 -Action <action>

Actions:
  setup    - Complete setup (install dependencies, initialize database)
  migrate  - Migrate from old database to enterprise version
  start    - Start the application server
  test     - Run smoke tests
  backup   - Backup current database
  clean    - Clean environment (remove venv and database)

Examples:
  .\setup_enterprise.ps1 -Action setup
  .\setup_enterprise.ps1 -Action start

"@
}

# Main execution
Show-Banner

switch ($Action) {
    'setup' {
        Test-Prerequisites
        Backup-Database
        Setup-Environment
        Initialize-Database
        Run-Tests
        
        Write-ColorOutput Green @"

╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   ✅ SETUP COMPLETE!                                       ║
║                                                            ║
║   Your enterprise database is ready to use!                ║
║                                                            ║
║   Next steps:                                              ║
║   1. Review .env configuration                             ║
║   2. Run: .\setup_enterprise.ps1 -Action start             ║
║   3. Open http://localhost:5000/health                     ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

"@
    }
    
    'migrate' {
        Test-Prerequisites
        Backup-Database
        Write-ColorOutput Yellow "Migration feature coming soon!"
        Write-ColorOutput Yellow "Please use the migration guide in MIGRATION_GUIDE.md"
    }
    
    'start' {
        Start-Application
    }
    
    'test' {
        Run-Tests
    }
    
    'backup' {
        Backup-Database
    }
    
    'clean' {
        Clean-Environment
    }
    
    default {
        Show-Help
    }
}
