# 贡献指南 (Contributing Guide)

感谢您有兴趣为 **工业流程 ERP 系统 (开源版)** 做出贡献！

本项目致力于为中小型制造企业提供一个现代化、零成本、安全可靠的 ERP 解决方案。我们非常欢迎来自社区的任何贡献，包括但不限于：

- 🐛 提交 Bug 报告
- ✨ 提交新功能建议 (Feature Requests)
- 📝 改进文档
- 🎨 优化 UI/UX
- 🛠️ 提交代码修复或新功能实现 (Pull Requests)

在您参与贡献之前，请花一点时间阅读以下指南。

---

## 🤝 行为准则 (Code of Conduct)

我们希望建立一个开放、友善、包容的社区环境。请在交流过程中保持尊重和专业。

- 使用包容性的语言。
- 尊重不同的观点和经验。
- 接受建设性的批评。
- 关注对社区最有利的事情。
- 对社区其他成员表现出同理心。

## 🐛 如何报告 Bug

如果您发现了 Bug，请通过 [GitHub Issues](https://github.com/fortitudelucifer/erp_opensource/issues) 提交报告。为了帮助我们快速定位问题，请在报告中包含以下信息：

1.  **标题**: 清晰简明地描述问题。
2.  **环境信息**:
    - 操作系统 (Windows/Linux/macOS)
    - Python 版本
    - 浏览器版本
    - 数据库类型 (SQL Server/PostgreSQL/MySQL)
3.  **复现步骤**: 详细描述如何重现该 Bug。
4.  **预期行为**: 您期望发生什么。
5.  **实际行为**: 实际发生了什么。
6.  **截图/日志**: 如果有报错截图或后台日志 (`logs/` 目录下的日志或控制台输出)，请一并提供。

## ✨ 如何提交功能建议

如果您有好的想法，欢迎提交 Feature Request Issue。请描述：

1.  您遇到的痛点是什么？
2.  您建议的解决方案是什么？
3.  这个功能对其他用户有什么帮助？

## 🛠️ 如何提交代码 (Pull Request)

1.  **Fork 本仓库**: 点击右上角的 "Fork" 按钮，将项目复制到您的 GitHub 账户。
2.  **克隆代码**: 将您的 Fork 克隆到本地。
    ```bash
    git clone https://github.com/您的用户名/erp_opensource.git
    cd erp_opensource
    ```
3.  **创建分支**: 为您的修改创建一个新的分支。
    ```bash
    git checkout -b fix/issue-number-description
    # 或者
    git checkout -b feat/feature-name
    ```
4.  **环境搭建**: 请参考 `README.md` 中的安装步骤搭建本地开发环境。确保所有依赖已安装，且数据库配置正确。
5.  **进行修改**:
    - 遵循现有的代码风格（PEP 8）。
    - 保持代码简洁清晰。
    - 如果添加了新功能，请尽量补充相应的注释。
6.  **提交更改**:
    ```bash
    git add .
    git commit -m "feat: 添加了XXX功能"
    ```
    *建议使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范编写 Commit 信息。*
7.  **推送到远程**:
    ```bash
    git push origin your-branch-name
    ```
8.  **提交 PR**: 在 GitHub 上发起 Pull Request。请在 PR 描述中关联相关的 Issue (例如 `Closes #123`)，并简要说明您的修改内容。

## 🎨 代码风格指南

- **Python**: 遵循 PEP 8 规范。
- **HTML/CSS/JS**: 保持缩进一致（建议 4 空格），遵循现有的命名约定。
- **中文注释**: 由于本项目主要面向中文用户，建议代码注释使用中文，以便于理解。

## ❓ 获取帮助

如果您在贡献过程中遇到任何问题，欢迎在 Issue 中提问，或者直接联系作者。

再次感谢您的贡献！让我们一起把这个项目变得更好！
