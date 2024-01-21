import subprocess
from tempfile import TemporaryDirectory

from wabbit.main import compile_to_llvm


def compile_and_exec(source: str) -> list[str]:
    with TemporaryDirectory() as tmpdir:
        with open(f"{tmpdir}/source.wb", "w") as f:
            f.write(source)

        llvm = compile_to_llvm(f"{tmpdir}/source.wb")
        with open(f"{tmpdir}/compiled.ll", "w") as f:
            f.write(llvm)

        subprocess.call(
            [
                "clang",
                f"{tmpdir}/compiled.ll",
                "wabbit/misc/runtime.c",
                "-o",
                f"{tmpdir}/compiled.exe",
            ]
        )
        res = subprocess.run(f"{tmpdir}/compiled.exe", capture_output=True)
    return res.stdout.decode().splitlines()
