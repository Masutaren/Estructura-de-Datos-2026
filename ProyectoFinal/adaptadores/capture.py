import sys
import io
import importlib.util
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def path_for(*parts):
    """Build absolute path from project root."""
    return os.path.join(BASE_DIR, *parts)


def import_module_captured(filepath, module_name, extra_paths=None):
    """Import a Python file capturing all stdout during execution.
    Returns (module, output_str). On error returns (None, error_message)."""
    if extra_paths:
        for p in reversed(extra_paths):
            if p not in sys.path:
                sys.path.insert(0, p)

    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    mod = None
    try:
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = mod
        spec.loader.exec_module(mod)
        output = buf.getvalue()
    except Exception as e:
        output = f"[Error al cargar módulo '{module_name}': {e}]"
        mod = None
    finally:
        sys.stdout = old_stdout
    return mod, output


def read_source(filepath):
    """Return source code of a file as a string."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"# No se pudo leer el archivo:\n# {e}"
