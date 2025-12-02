# 🆕 v3.1.1 更新说明

## 关键修复和新功能

### 🔧 P0级别修复 (2025-12-01)

#### 1. 安全导入系统
- **新增**: `safe_import.py` 模块
- **功能**: 可选依赖安全导入，未安装不影响核心功能
- **影响**: allure/websocket等可选模块未安装时，框架仍可正常使用

#### 2. YAML配置验证
- **新增**: `yaml_validator.py` 模块
- **功能**: 配置文件加载时自动验证
- **优势**: 早期发现配置错误，提供详细错误提示

#### 3. 增强的Hook系统
- **新增**: `hook_manager.py` 模块
- **功能**: 13种测试生命周期Hook
- **支持**: before_suite, after_suite, before_test, after_test, on_failure等

#### 4. 依赖管理优化
- **优化**: 重新整理requirements文件
- **结构**:
  - `requirements.txt` - 核心依赖（6个）
  - `requirements-optional.txt` - 可选依赖分组
  - `requirements-full.txt` - 完整安装

---

## 快速使用

### 安装

```bash
# 最小安装（推荐）
pip install -r requirements.txt

# 完整安装（所有功能）
pip install -r requirements-full.txt

# 按需安装
pip install -r requirements.txt
pip install allure-pytest jinja2  # 添加报告功能
```

### 验证配置

```python
from yaml_validator import validate_yaml_file

# 自动验证YAML配置
validate_yaml_file('test.yaml')
```

### 使用Hook

```python
from hook_manager import before_test, after_test

@before_test
def setup():
    print("测试前准备")

@after_test
def cleanup():
    print("测试后清理")
```

### 安全导入

```python
from safe_import import safe_import

# 可选模块安全导入
allure = safe_import('allure')
websocket = safe_import('websocket')
```

---

## 测试验证

运行验证测试：
```bash
python test_fixes.py
```

预期输出：
```
[PASS] - 安全导入模块
[PASS] - YAML配置验证器
[PASS] - Hook管理器
[PASS] - Runner导入修复
[PASS] - 依赖文件整理
[PASS] - YAML文件验证

总计: 6/6 测试通过
```

---

## 向后兼容性

✅ 完全向后兼容
- 现有测试用例无需修改
- RunYaml类接口保持不变
- 默认启用配置验证（可选关闭）

---

## 详细文档

查看完整修复说明: [FIX_SUMMARY.md](FIX_SUMMARY.md)

---

## 下一步计划

- [ ] 拆分runner.py（1287行 -> 多个模块）
- [ ] 配置文件热重载
- [ ] YAML配置IDE支持（JSON Schema）
- [ ] 可视化测试编排器

---

**更新日期**: 2025-12-01
**版本**: v3.1.1
**状态**: ✅ 已发布
