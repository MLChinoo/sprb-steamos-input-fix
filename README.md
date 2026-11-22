# Summer Pockets REFLECTION BLUE — SteamOS Input Fix

《Summer Pockets REFLECTION BLUE》Steam 版在 SteamOS / Proton 环境下的非官方 Steam Input 兼容性修复补丁。

本项目旨在解决部分 Linux 掌机使用原生手柄时，打开游戏的 **Settings（设置）** 或 **Load（读取存档）** 界面导致游戏崩溃的问题。

修复后无需切换到键盘鼠标布局，也不需要更换操作系统或修改系统级手柄配置。

### **注意：请先打上官方的[CG・文本还原版补丁](https://va-trialdist.azureedge.net/key/summer_rb/index.html)(发布日：2026年3月3日 Ver.2.4.2.3)，再使用本项目修补。**

## 问题描述

在部分 SteamOS / Proton 环境下，游戏存在以下问题：

- 游戏能够正常启动并进入主菜单。
- 使用原生手柄时，打开 Settings 或 Load 会导致崩溃。
- 将 Steam Input 切换为键盘鼠标布局可以规避问题，但会失去正常的原生手柄体验。
- 更换 Proton 版本或调整 Steam Input 设置不一定能够解决问题。

相关问题：

- [ValveSoftware/Proton #9948](https://github.com/ValveSoftware/Proton/issues/9948)
- [ublue-os/bazzite #5745](https://github.com/ublue-os/bazzite/issues/5745)

## 兼容性

本项目主要针对以下环境开发和测试：

| 项目        | 环境                               |
| ----------- | ---------------------------------- |
| 游戏        | Summer Pockets REFLECTION BLUE     |
| Steam AppID | 3418570                            |
| 设备        | ASUS ROG Ally Z1 Extreme           |
| 操作系统    | 官方 SteamOS                       |
| 兼容层      | Proton 11.0-2e                     |
| 控制器      | Steam Deck Controller（deck-uhid） |

其他设备、Linux 发行版和 Proton 版本可能同样受益，但尚未经过全面测试。

## 安装方法

### 1. 下载项目

下载仓库中的 `patch_glyph_bounds.py`，并准备 Python 3。

### 2. 备份游戏文件

在 Steam 中打开游戏属性，选择：

**已安装文件 → 浏览**

找到：

```
SummerPocketsRB.exe
```

先备份该文件，以便随时恢复。

### 3. 准备可修补的 EXE

由于游戏原始 EXE 带有 SteamStub 保护，需要先获得解包后的程序。

可以使用 [Steamless](https://github.com/atom0s/Steamless) 处理自己合法安装的游戏文件。

补丁要求解包后的 EXE 具有以下 SHA-256：

```
4cac5967d6619f92190be84f3a25a255613c90ff95122296373cc9bf0ace8e64
```

不符合该版本的文件将被补丁脚本拒绝。

### 4. 生成修复后的 EXE

在包含补丁脚本和解包后 EXE 的目录中执行：

```
python patch_glyph_bounds.py SummerPocketsRB.exe.unpacked.exe SummerPocketsRB.patched.exe
```

成功后会生成：

```
SummerPocketsRB.patched.exe
```

预期 SHA-256：

```
0d3190237535a6c4c4be8b8f30a17ecd2e365884f65da07f26d42ca807879e13
```

### 5. 安装补丁

完全退出游戏，将生成的 `SummerPocketsRB.patched.exe` 复制到游戏安装目录，并重命名为：

```
SummerPocketsRB.exe
```

替换前请确认原文件已经备份。

在 SteamOS 上操作时，请保留文件原有的执行权限。

### 6. 启动与验证

通过 Steam 正常启动游戏，使用原生 Gamepad 布局测试：

- Settings 是否可以正常打开。
- Load 是否可以正常打开。
- 游戏内手柄按键是否正常工作。
- SteamOS 的系统按键是否保持正常。

无需切换 InputPlumber 的虚拟手柄类型。

## 恢复原版

如果出现异常，可以选择以下任一方式：

1. 退出游戏，将备份的原始 `SummerPocketsRB.exe` 放回游戏目录。
2. 在 Steam 中打开 **属性 → 已安装文件 → 验证游戏文件的完整性**，让 Steam 恢复官方文件。

恢复后，原有崩溃问题可能再次出现。

## 技术分析

该问题与游戏处理 Steam Input 控制器按钮图标时的兼容性缺陷有关。

本项目通过对游戏程序进行局部修补，避免相关异常导致游戏崩溃，同时尽量保留正常的原生手柄功能。

关于问题定位、IDA Pro 逆向分析、补丁实现及验证过程，请参阅：

[技术复盘报告（简体中文）](docs/technical-analysis.zh-CN.md)

README 仅介绍补丁的用途和使用方法，完整技术细节统一放在复盘报告中。

## 已知限制

- 仅支持指定 SHA-256 的解包后 EXE。
- Steam 更新游戏后可能覆盖补丁。
- 某些未受游戏支持的手柄按钮图标可能无法显示。
- 其他设备和系统组合尚未完全验证。
- 此补丁并不保证解决所有类型的游戏崩溃。

## 免责声明

本项目是由社区独立制作的非官方兼容性修复，不隶属于 Visual Arts、Key、Valve 或 Steam。

游戏本身及相关商标、素材的权利归其各自所有者所有。

本仓库不提供游戏本体、原始可执行文件、解包后的完整可执行文件或修改后的完整游戏程序。用户需要自行持有合法获取的游戏副本。

使用补丁前请备份原始文件。使用者应自行承担修改游戏文件可能产生的兼容性问题及其他风险。

**希望这个项目能够帮助更多 SteamOS / Linux 掌机玩家正常体验《Summer Pockets REFLECTION BLUE》。**