# Contributing to 3D Decimator

Thank you for your interest in contributing to 3D Decimator! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Docker version, browser)
- Sample files if applicable (keep them small)

### Suggesting Features

Feature requests are welcome! Please:
- Check existing issues first
- Clearly describe the feature and use case
- Explain why it would be valuable to users

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   # Run the application locally
   python app.py
   
   # Test with Docker
   docker build -t 3d-decimator-test .
   docker run -p 8000:8000 3d-decimator-test
   ```

5. **Commit your changes**
   ```bash
   git commit -m "feat: add feature description"
   ```
   
   Use conventional commits:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Code style changes
   - `refactor:` - Code refactoring
   - `test:` - Adding tests
   - `chore:` - Maintenance tasks

6. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Setup

### Local Development

```bash
# Clone your fork
git clone https://github.com/yourusername/3d-decimator.git
cd 3d-decimator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Docker Development

```bash
# Build development image
docker build -t 3d-decimator-dev .

# Run with volume mounting for live reload
docker run -p 8000:8000 \
  -v $(pwd)/app.py:/app/app.py \
  -v $(pwd)/templates:/app/templates \
  3d-decimator-dev
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Keep functions focused and small
- Add docstrings to functions
- Comment complex algorithms

## Testing

Before submitting:
- Test with multiple file formats (STL, OBJ, 3MF)
- Test batch processing with various file counts
- Test different reduction levels
- Check file browser functionality
- Verify history tracking
- Test in different browsers

## Documentation

When adding features:
- Update README.md if user-facing
- Update code comments
- Add examples if applicable
- Update deployment guide if affecting deployment

## Questions?

Open an issue for discussion or contact the maintainers.

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on the issue, not the person
- Assume good intentions

Thank you for contributing! 🙏
