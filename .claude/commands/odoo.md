你是 Odoo 开发助手。根据用户的请求，自动判断并执行对应的操作。

用户请求：$ARGUMENTS

---

## 操作判断

根据用户输入自动匹配以下场景。如果用户没有输入任何内容，检测当前项目状态并建议下一步。

### 场景 A：项目初始化（关键词：setup / 初始化 / 配置 / 设置 / init）

或者：当前目录没有 Agent.md 也没有 CLAUDE.md 时，自动建议初始化。

执行以下步骤：

1. **查找工具包仓库**（按顺序尝试）：
   - `$ODOO_DESIGN_PATTERN_HOME`
   - `~/odoo-design-pattern`
   - `~/working/odoo-design-pattern`
   - 找不到则提示用户指定路径

2. **从仓库复制以下文件到当前项目**：
   - `Agent.md` → 当前项目根目录（如已有 CLAUDE.md，追加到末尾）
   - `DEVELOPMENT_STANDARD.md` → 当前项目根目录
   - `COMMIT_CONVENTION.md` → 当前项目根目录
   - `.pre-commit-config.yaml` → 当前项目根目录
   - `.github/pull_request_template.md`
   - `.github/workflows/pr-review.yml`
   - `.github/scripts/review_pr.py`
   - `_templates/` → 当前项目根目录

3. **安装 pre-commit**（如可用）：
   - 检测 `pre-commit` 是否已安装
   - 如已安装，运行 `pre-commit install`
   - 如未安装，提示用户 `pip install pre-commit`

4. **输出清单**：列出所有创建的文件 + 需要手动做的事（如添加 GitHub Secret）

---

### 场景 B：创建新模块（关键词：new / 新建 / 创建 / create / module / 模块）

1. **解析模块名**：从用户输入中提取模块名。如未提供，询问。

2. **查找模板**（按顺序）：
   - 当前项目 `_templates/module_template/`
   - 工具包仓库 `_templates/module_template/`
   - 都找不到则用内置基础结构

3. **确定目标路径**：
   - `./addons/` 或 `./custom_addons/`（如存在）
   - 否则当前目录

4. **创建模块**：复制模板并替换所有占位符：
   - `module_template` → 实际模块名
   - `module.sample` → 实际模型 `_name`
   - `SampleModel` → 实际类名（PascalCase）
   - `sample_model` → 实际文件名
   - `module_sample` → XML ID 前缀
   - `TODO:` → 根据模块用途填入合理值

5. **输出**：列出创建的文件 + 后续需要调整的内容

---

### 场景 C：代码审查（关键词：review / 审查 / 检查 / check / lint）

1. **获取改动**：
   - 优先 `git diff --staged`（有暂存改动时）
   - 其次 `git diff HEAD~1`（已提交时）
   - 用户指定文件则只审查指定文件

2. **加载审查标准**：读取当前项目或工具包仓库的 `DEVELOPMENT_STANDARD.md`

3. **对照第 17 节的 15 项清单逐项检查**

4. **输出格式**：
   ```
   ## Blocker（必须修复）
   - [文件:行号] 问题描述

   ## Warning（建议修改）
   - [文件:行号] 问题描述

   ## Info（提示）
   - 建议

   ## 总结
   通过 / 需修改
   ```

---

### 场景 D：无法判断

如果无法判断用户意图，列出可用操作：

- **初始化项目**：`/odoo setup`
- **创建新模块**：`/odoo new myco_sale_approval`
- **审查代码**：`/odoo review`

并询问用户想做什么。
