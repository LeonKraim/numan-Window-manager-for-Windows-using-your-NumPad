# Contributing to NumaN

Thanks for considering contributing. Here's how to get started.

## Reporting bugs

Open an issue with:
- What you expected to happen
- What actually happened
- Your Windows version
- Steps to reproduce

## Submitting changes

1. Fork the repo
2. Create a branch (`git checkout -b fix/your-fix-name`)
3. Make your changes
4. Test them — run the app, try assigning and switching windows
5. Submit a pull request

Keep PRs focused. One fix or feature per PR is easier to review.

## Development setup

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/numan/main.py
```

## Code style

Nothing fancy. Keep it readable. Follow the existing patterns in the codebase.
