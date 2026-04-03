# LaTeX 格式规范总结

## 快速索引
- **无标号数字**：所有章节标题都不写"1.2"这样的数字，由 LaTeX 自动编号
- **段尾双反斜杠**：每个自然段后追加 `\\` 强制换行
- **双列图片**：宽图用 `figure*[t]` 并 `\textwidth{0.8}` 宽度，每页最多 1 张
- **单列图片**：窄图用 `figure[H]` 并 `\columnwidth` 宽度，可多张同页
- **溢出防护**：用 `\resizebox{\columnwidth}{!}{...}` 让表格自适应列宽

---

## 详细规范

### 1. 章节编号
```latex
\section{Game Definition and Urban Commuting Framing}
\subsection{Motivating Context}
```
✅ **正确**：不写数字，LaTeX 自动生成 "1. Game Definition..." 和 "1.1 Motivating Context"

❌ **错误**：`\section{1. Game Definition...}` 会变成 "1. 1. Game Definition..."

**配置**：文件开头已设置 `\setcounter{secnumdepth}{2}` 启用自动编号到 subsection 级别

---

### 2. 段落结尾强制换行
```latex
Every weekday morning, $N=101$ workers decide independently...
This is a minority game (Challet & Zhang, 1997)... \\
```
✅ **规则**：每个逻辑段落后追加 `\\` 两个反斜杠
- 自然段：需要 `\\`
- `\item` 列表项：不需要 `\\`（LaTeX 自动处理）
- 表格/方程后段落：需要 `\\`

---

### 3. 图片分类和布局

#### 3.1 单列图片（宽度 ≤ 5 英寸）
```latex
\begin{figure}[H]
\centering
\includegraphics[width=\columnwidth]{figure1_static_sweep.png}
\caption{(a) Mean attendance vs $p$. (b) Indifference condition.}
\label{fig:fig1}
\end{figure}
```
- 使用 `[H]` specifier（严格位置）
- 宽度用 `\columnwidth`（单列宽度）
- 可在同一页放多张窄图
- 例子：Figures 1, 2, 4, 5, 6

#### 3.2 双列图片（宽度 > 5 英寸）
```latex
\begin{figure*}[t]
\centering
\includegraphics[width=0.8\textwidth]{figure3_best_response.png}
\caption{Stage-game best-reply: permanent oscillation.}
\label{fig:fig3}
\end{figure*}
```
- 使用 `figure*` 环境（双列）
- 使用 `[t]` specifier（页顶位置，防止浮动干扰）
- 宽度用 `0.8\textwidth` 或 `0.75\textwidth`（保留边距）
- **关键**：每页最多 1 张双列图（避免布局混乱）
- 例子：Figures 3, 7（都是宽图）

#### 3.3 表格尺寸控制
```latex
\begin{table}[H]
\centering
\small
\resizebox{\columnwidth}{!}{%
\begin{tabular}{lccc}
...
\end{tabular}%
}
\caption{Welfare comparison across strategy profiles}
\label{tab:welfare}
\end{table}
```
- 单列表：`\resizebox{\columnwidth}{!}{...}`（自动缩放到单列宽）
- 双列表：`\resizebox{0.8\textwidth}{!}{...}` 或直接不限制（`\begin{table*}[t]...`）
- `!` 参数：保持宽高比，只改变宽度

---

### 4. 图片标题规范
```latex
❌ \caption{Figure 1: Mean attendance vs p}
✅ \caption{Mean attendance $\mathbb{E}[A]$ vs $p$ across the full sweep.}
```
- **不写** "Figure X:" 或 "Table Y:"（LaTeX 自动生成）
- 直接写描述内容
- 使用数学模式表达公式（`$...$`）

---

### 5. 特殊环境规范

#### 浮动图片防止溢出
文件已导入 `\usepackage{stfloats}` 处理双列图片底部对齐。用法：
- 单列 `[H]`：不浮动，严格位置
- 双列 `[t]`：浮动到页顶，stfloats 自动排版底部对齐

#### 数学和列表
```latex
\begin{itemize}
    \item \textbf{Players:} $\mathcal{N} = \{1,\ldots, 101\}$
    \item \textbf{Strategy space:} ...
\end{itemize}
```
- 列表后**不需要** `\\`（LaTeX 自动处理垂直间距）
- 列表前的段落需要 `\\`

---

## 双列文档中的页面布局最佳实践

| 页面位置 | 推荐内容 | 备注 |
|---------|--------|------|
| 上半部分 | 双列图 (1张) + 文字 | `\figure*[t]`，高 ~4 英寸 |
| 中间部分 | 单列图 (1-2张) + 表格 | `\figure[H]`，可堆叠 |
| 下半部分 | 文字继续 + 单列表 | 避免双列图底部堆积 |

---

## 本文档应用示例

### Section 2.3 Welfare Analysis 页面布局
```
[文字开始]
The mixed NE is Pareto-inefficient... \\

[单列表：Welfare comparison - \columnwidth]
\begin{table}[H] ... \end{table}

[文字继续]
The social optimum coincides with... \\
```
✅ 表格自动缩放到单列宽，不造成溢出

### Section 3: Static Game 双列页面
```
[文字开始 ~ 1/3 页]
Running 1,000 independent... \\

[双列图 Figure 3]
\begin{figure*}[t] ... \end{figure*}

[下一节开始]
\subsection{Attendance Distribution...}
```
✅ 双列图占 1/3 页高度，后续内容自动换页

---

## 常见错误与修复

| 错误 | 原因 | 修复 |
|-----|------|-----|
| "1. 1. Game Definition" | 标题中有数字 + LaTeX 自动编号 | 删除标题中的数字 |
| 图片跑到下一页 | 没用 `\\` 强制换行 | 在段落末尾加 `\\` |
| 表格超出列宽 | 直接 `\tabular` 没缩放 | 用 `\resizebox{\columnwidth}{!}{...}` 包裹 |
| 双列图乱七八糟 | 多张 `figure*[t]` 同页 | 限制每页 1 张双列图 |
| 文字贴在图题下 | 没用 `\\` 分隔 | 图片后追加 `\\` |

---

## 配置文件检查清单

文件头部已包含：
- ✅ `\usepackage{stfloats}` — 双列浮动管理
- ✅ `\setcounter{secnumdepth}{2}` — 自动编号到 subsection
- ✅ `\usepackage{booktabs}` — 专业表格线条
- ✅ `\documentclass[letterpaper]{article}` — Letter 纸张（8.5×11 英寸）

---

## 转换检查表

当从 Markdown 转换为 LaTeX 时，依次检查：

- [ ] 所有 `#` 或 `##` 标题改为 `\section` 和 `\subsection`（去掉数字）
- [ ] 每个自然段末尾加 `\\`
- [ ] 图片用 `includegraphics` + 合适的宽度（`\columnwidth` 或 `0.8\textwidth`）
- [ ] 图题去掉 "Figure X:" 前缀
- [ ] 表格用 `\resizebox{...}{!}{...}` 保证不溢出
- [ ] 列表（`\itemize`）项目不加 `\\`
- [ ] 双列图限制每页 1 张
- [ ] 公式用 `$...$`（内联）或 `\begin{equation}...\end{equation}`（展示）

