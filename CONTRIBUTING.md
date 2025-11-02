# Contributing to StyleSense.AI

Thank you for your interest in contributing to StyleSense.AI! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other contributors

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB
- Git

### Setting Up Development Environment

1. **Fork the repository**
   ```bash
   # Click "Fork" button on GitHub
   git clone https://github.com/YOUR_USERNAME/final-stylesense.git
   cd final-stylesense
   ```

2. **Set up backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Set up frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Run tests**
   ```bash
   # Backend tests
   cd backend
   pytest tests/

   # Frontend tests
   cd frontend
   npm test
   ```

## Development Process

### Branching Strategy

- `main`: Production-ready code
- `develop`: Development branch
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Critical production fixes

### Working on a Feature

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes**
   - Write code
   - Add tests
   - Update documentation

3. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Describe your changes
   - Link related issues

## Pull Request Process

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow conventions
- [ ] No merge conflicts

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No linting errors
```

### Review Process

1. Maintainer reviews code
2. Automated tests run
3. Feedback provided
4. Changes requested if needed
5. Approved and merged

## Coding Standards

### Python (Backend)

#### Style Guide
- Follow PEP 8
- Use type hints where appropriate
- Maximum line length: 100 characters

#### Example
```python
from typing import Dict, List, Optional

def get_recommendations(
    user_id: str,
    occasion: str = "casual",
    weather: str = "moderate"
) -> List[Dict]:
    """
    Generate outfit recommendations.
    
    Args:
        user_id: User identifier
        occasion: Event type (casual, formal, etc.)
        weather: Weather condition
        
    Returns:
        List of recommendation dictionaries
    """
    # Implementation
    pass
```

#### Docstrings
Use Google-style docstrings:
```python
def function_name(param1: str, param2: int) -> bool:
    """Short description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is invalid
    """
```

### JavaScript/React (Frontend)

#### Style Guide
- Use functional components with hooks
- Use destructuring for props
- Keep components focused and small

#### Example
```javascript
import React, { useState, useEffect } from 'react';

/**
 * Component description
 */
function MyComponent({ prop1, prop2 }) {
  const [state, setState] = useState(null);
  
  useEffect(() => {
    // Effect logic
  }, []);
  
  return (
    <div className="container">
      {/* JSX */}
    </div>
  );
}

export default MyComponent;
```

### Commit Messages

Follow Conventional Commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

#### Examples
```
feat(backend): add weather-based recommendations

Implement weather API integration for outfit suggestions
based on current conditions.

Closes #123
```

```
fix(frontend): resolve camera capture on Safari

Update MediaDevices API usage to support Safari browser.
Added polyfill for older browsers.

Fixes #456
```

## Testing Guidelines

### Backend Tests

#### Unit Tests
```python
def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
```

#### Integration Tests
```python
def test_upload_and_retrieve(client):
    """Test upload and retrieval workflow"""
    # Upload item
    response = client.post('/api/wardrobe/upload', data={
        'file': test_file,
        'user_id': 'test_user'
    })
    assert response.status_code == 201
    
    # Retrieve items
    response = client.get('/api/wardrobe/test_user')
    assert len(response.json['items']) > 0
```

### Frontend Tests

#### Component Tests
```javascript
import { render, screen } from '@testing-library/react';
import Dashboard from './Dashboard';

test('renders dashboard title', () => {
  render(<Dashboard />);
  const title = screen.getByText(/StyleSense.AI Dashboard/i);
  expect(title).toBeInTheDocument();
});
```

#### API Tests
```javascript
test('fetches health status', async () => {
  const data = await getHealthStatus();
  expect(data.status).toBe('healthy');
});
```

### Test Coverage

Aim for:
- Backend: 80%+ coverage
- Frontend: 70%+ coverage
- Critical paths: 100% coverage

## Documentation

### What to Document

- API endpoints (in docs/api_specification.md)
- Component props and usage
- Complex algorithms
- Configuration options
- Deployment procedures

### Documentation Format

Use Markdown with clear examples:

```markdown
## Component Name

### Description
What the component does

### Props
| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| name | string | Yes | - | User name |

### Example
\`\`\`javascript
<Component name="John" />
\`\`\`
```

## Issue Reporting

### Bug Reports

Include:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details

### Feature Requests

Include:
- Feature description
- Use case/motivation
- Proposed implementation
- Alternative solutions considered

## Questions?

- Check existing issues
- Review documentation
- Ask in discussions
- Contact maintainers

---

Thank you for contributing to StyleSense.AI! 🎨✨
