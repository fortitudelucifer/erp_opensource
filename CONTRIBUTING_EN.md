# Contributing Guide

Thank you for your interest in contributing to the **Industrial Flow ERP System (Open Source Edition)**!

This project aims to provide a modern, zero-cost, secure, and reliable ERP solution for small and medium-sized manufacturing enterprises. We warmly welcome any contribution from the community, including but not limited to:

- 🐛 Reporting Bugs
- ✨ Submitting Feature Requests
- 📝 Improving Documentation
- 🎨 Optimizing UI/UX
- 🛠️ Submitting Code Fixes or New Features (Pull Requests)

Before you start contributing, please take a moment to read the following guide.

---

## 🤝 Code of Conduct

We hope to establish an open, friendly, and inclusive community environment. Please remain respectful and professional during communication.

- Use inclusive language.
- Respect different viewpoints and experiences.
- Accept constructive criticism.
- Focus on what is best for the community.
- Show empathy towards other community members.

## 🐛 How to Report Bugs

If you find a Bug, please submit a report via [GitHub Issues](https://github.com/fortitudelucifer/erp_opensource/issues). To help us locate the problem quickly, please include the following information in your report:

1.  **Title**: Describe the issue clearly and concisely.
2.  **Environment Information**:
    - Operating System (Windows/Linux/macOS)
    - Python Version
    - Browser Version
    - Database Type (SQL Server/PostgreSQL/MySQL)
3.  **Steps to Reproduce**: Describe in detail how to reproduce the bug.
4.  **Expected Behavior**: What you expected to happen.
5.  **Actual Behavior**: What actually happened.
6.  **Screenshots/Logs**: If there are error screenshots or backend logs (logs in `logs/` directory or console output), please provide them as well.

## ✨ How to Submit Feature Requests

If you have good ideas, welcome to submit a Feature Request Issue. Please describe:

1.  What pain point are you facing?
2.  What is your suggested solution?
3.  How does this feature help other users?

## 🛠️ How to Submit Code (Pull Request)

1.  **Fork this Repository**: Click the "Fork" button in the upper right corner to copy the project to your GitHub account.
2.  **Clone Code**: Clone your Fork to local.
    ```bash
    git clone https://github.com/YourUsername/erp_opensource.git
    cd erp_opensource
    ```
3.  **Create Branch**: Create a new branch for your changes.
    ```bash
    git checkout -b fix/issue-number-description
    # Or
    git checkout -b feat/feature-name
    ```
4.  **Environment Setup**: Please refer to the installation steps in `README_EN.md` or `README.md` to set up the local development environment. Ensure all dependencies are installed and database configuration is correct.
5.  **Make Changes**:
    - Follow existing code style (PEP 8).
    - Keep code concise and clear.
    - If adding new features, please try to add corresponding comments.
6.  **Commit Changes**:
    ```bash
    git add .
    git commit -m "feat: Added XXX feature"
    ```
    _Recommended to use [Conventional Commits](https://www.conventionalcommits.org/) specification for Commit messages._
7.  **Push to Remote**:
    ```bash
    git push origin your-branch-name
    ```
8.  **Submit PR**: Initiate a Pull Request on GitHub. Please associate relevant Issues in the PR description (e.g., `Closes #123`) and briefly describe your modifications.

## 🎨 Code Style Guide

- **Python**: Follow PEP 8 specification.
- **HTML/CSS/JS**: Keep indentation consistent (recommended 4 spaces), follow existing naming conventions.
- **Comments**: Since this project is mainly for Chinese users, Chinese comments are recommended for better understanding, but English is also welcome.

## ❓ Get Help

If you encounter any problems during the contribution process, welcome to ask in Issues, or contact the author directly.

Thank you again for your contribution! Let's make this project better together!
