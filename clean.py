from pathlib import Path
import shutil

ROOT = Path(__file__).parent

removed_dirs = 0
removed_files = 0

print(f"Очистка проекта: {ROOT}\n")

# Удаляем папки __pycache__
for folder in ROOT.rglob("__pycache__"):
    try:
        shutil.rmtree(folder)
        removed_dirs += 1
        print(f"Удалена папка: {folder.relative_to(ROOT)}")
    except Exception as e:
        print(f"Ошибка: {folder} -> {e}")

# Удаляем .pyc и .pyo
for ext in ("*.pyc", "*.pyo"):
    for file in ROOT.rglob(ext):
        try:
            file.unlink()
            removed_files += 1
            print(f"Удалён файл: {file.relative_to(ROOT)}")
        except Exception as e:
            print(f"Ошибка: {file} -> {e}")

print("\n===================================")
print(f"Удалено папок : {removed_dirs}")
print(f"Удалено файлов: {removed_files}")
print("Очистка завершена.")