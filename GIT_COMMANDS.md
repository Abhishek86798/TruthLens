# Git Commands for TruthLens Project

## Initial Setup

```bash
# Initialize repository
git init

# Configure user
git config --local user.name "Your Name"
git config --local user.email "your.email@example.com"
```

## Daily Development

```bash
# Check status
git status

# Add files
git add src/preprocessing.py
git add src/data_collection.py
git add -A  # Add all changes

# Commit
git commit -m "feat: add preprocessing module"
git commit -m "fix: handle empty text input"

# View history
git log --oneline
```

## Branching

```bash
# Create feature branch
git checkout -b feature/concurrent-scraping

# Switch branches
git checkout main
git checkout feature/concurrent-scraping

# Merge feature
git checkout main
git merge feature/concurrent-scraping
```

## Remote Operations

```bash
# Add remote
git remote add origin https://github.com/username/TruthLens.git

# Push changes
git push origin main
git push -u origin feature/concurrent-scraping

# Pull updates
git pull origin main
```

## Best Practices

### Commit Message Format

- feat: new feature
- fix: bug fix
- docs: documentation changes
- test: adding tests
- refactor: code restructuring

### Branch Naming

- feature/feature-name
- bugfix/issue-description
- docs/documentation-update

### Development Workflow

1. Create feature branch
2. Make changes
3. Run tests
4. Commit with clear message
5. Push to remote
6. Create pull request

## Common Issues

```bash
# Discard local changes
git checkout -- src/preprocessing.py

# Undo last commit
git reset --soft HEAD~1

# View file history
git log -p src/preprocessing.py
```

## CI/CD Integration

- Push triggers GitHub Actions
- Tests run automatically
- Check status in GitHub interface
