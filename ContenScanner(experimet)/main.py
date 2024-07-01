from pathlib import Path
import sys

# Определение пути к корневой директории проекта
project_root = Path(__file__).resolve().parent
# Добавление пути к корневой директории проекта в sys.path
sys.path.append(str(project_root))
# Импортировать модули из mypackage
from mypackage import mymodule

# Использование функций или классов из mymodule