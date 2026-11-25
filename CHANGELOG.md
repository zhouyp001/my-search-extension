# Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 与
[语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

## [1.0.0] - 2026-11-25

### Added

- 首次发布
- 弹窗搜索：输入关键词后回车或点击按钮，在新标签页打开搜索结果
- 自定义搜索 URL 模板，使用 `%s` 占位关键词
- 配置通过 `chrome.storage.local` 保存在本地
- 中英文界面（`_locales`）
- 模板安全校验：仅允许 `http://` / `https://` 且必须包含 `%s`

### Security

- 拒绝非 http/https 协议模板，避免 `javascript:` 等注入风险