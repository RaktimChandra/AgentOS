# Contributing to AgentOS

Thank you for your interest in contributing to AgentOS!

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker Desktop
- Git

### Setup Development Environment

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/AgentOS.git
cd AgentOS
```

3. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. Install frontend dependencies:
```bash
cd frontend
npm install
```

5. Start development services:
```bash
cd docker
docker-compose up -d
```

## Development Workflow

### Branching Strategy

- `main` - Production branch
- `develop` - Development branch
- `feature/*` - Feature branches
- `bugfix/*` - Bug fix branches
- `hotfix/*` - Hotfix branches for production

### Creating a Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### Making Changes

1. Make your changes
2. Write tests for new functionality
3. Update documentation
4. Run tests:
```bash
cd backend
pytest tests/ -v
```

5. Run linting:
```bash
cd backend
ruff check .
black --check .
mypy app/
```

### Committing Changes

Follow conventional commits format:
```
feat: add new feature
fix: fix bug
docs: update documentation
test: add tests
refactor: refactor code
chore: maintenance tasks
```

Example:
```bash
git add .
git commit -m "feat: add webhook system for event notifications"
```

### Pushing and Creating Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Code Style

### Python

- Follow PEP 8
- Use type hints
- Write docstrings for all public functions
- Maximum line length: 100 characters

### TypeScript/React

- Follow ESLint rules
- Use functional components
- Use hooks
- Write PropTypes or TypeScript types

### Documentation

- Use clear, concise language
- Include examples
- Update API reference for API changes
- Update README for user-facing changes

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Integration Tests

```bash
cd docker
docker-compose up -d
cd backend
pytest tests/integration/
```

## Pull Request Guidelines

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests passing
- [ ] No linting errors
- [ ] Commit messages follow conventional commits
- [ ] PR description clearly describes changes

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Fixes #123

## Testing
Describe testing performed

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## Reporting Bugs

1. Check existing issues
2. Create new issue with:
   - Clear title
   - Description of bug
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details
   - Screenshots/logs if applicable

## Feature Requests

1. Check existing issues
2. Create new issue with:
   - Clear title
   - Description of feature
   - Use case
   - Proposed implementation (if known)

## Questions

Use GitHub Discussions for questions.

## Code of Conduct

- Be respectful
- Be inclusive
- Be constructive
- Focus on what is best for the community

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
