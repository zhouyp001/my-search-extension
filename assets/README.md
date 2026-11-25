# assets

扩展图标目录。

## 文件说明

| 文件 | 用途 | 是否打进商店 zip |
| --- | --- | --- |
| `source.png` | 图标源图（建议 ≥ 512×512） | 否 |
| `icon16.png` / `icon32.png` / `icon48.png` / `icon128.png` | `manifest.json` 引用 | 是 |
| `icon300.png` | Edge 商店列表图标（后台上传） | 否 |

## 生成方式

1. 将源图保存为 `assets/source.png`
2. 运行：

   ```bash
   python scripts/generate_icons.py
   ```
3. 将生成的 icon16/32/48/128/300.png 一并提交到仓库（CI 打包依赖它们）