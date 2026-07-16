# 用途：自动发现并加载分类目录中的全部参考指标算子。
from __future__ import annotations

import importlib.util
from pathlib import Path


class OperatorError(RuntimeError):
    pass


def load_operators(root: Path) -> list[object]:
    modules: list[object] = []
    for path in sorted(root.glob("*/*.py")):
        if path.name == "__init__.py":
            continue
        module_name = f"evidence_operator_{path.parent.name}_{path.stem}"
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise OperatorError(f"无法加载指标算子：{path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, "SPEC") or not callable(getattr(module, "evaluate", None)):
            raise OperatorError(f"指标算子缺少 SPEC/evaluate：{path}")
        modules.append(module)
    ids = [module.SPEC["id"] for module in modules]
    if len(ids) != len(set(ids)):
        raise OperatorError("指标算子 ID 存在重复")
    if len(ids) < 200:
        raise OperatorError(f"指标算子仅 {len(ids)} 个，少于 200 个")
    return modules
