import subprocess
import sys
import os
from pathlib import Path

def make_docs():
    """Generate documentation using Sphinx."""
    # 현재 작업 디렉토리를 기준으로 경로 설정
    current_dir = Path(os.getcwd())
    
    # Sphinx 소스 및 빌드 디렉토리 경로
    source_dir = current_dir / "docs" / "sphinx" / "source"
    build_dir = current_dir / "docs" / "sphinx" / "build"
    
    cmd = ["sphinx-build", "-b", "html", str(source_dir), str(build_dir)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # stdout 출력
    if result.stdout:
        print(result.stdout)
    
    # stderr(경고) 출력
    if result.stderr:
        print("\nWarnings:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
    
    if result.returncode != 0:
        sys.exit(result.returncode)

if __name__ == "__main__":
    make_docs() 