"""Simple Build Script to create a python package wheel."""

# Python Dependencies
import os
import shutil
import subprocess
import argparse

from pathlib import Path


project_dir = os.path.split(os.path.abspath(__file__))[0]
package_name = "CurveFitting"

_ansi = [f"\033[{i}m" for i in range(30, 38)]
_colors = [
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "purple",
    "cyan",
    "white"
]
_ansi_colors = dict(zip(_colors, _ansi))


def print_color(color, *msg):
    reset = u"\u001b[0m"
    print(_ansi_colors[color], sep="", end="")
    print(*msg, reset)


def cleanup(source: str):
    try:
        shutil.rmtree(source)
    except FileNotFoundError:
        pass


def build_docs():
    print_color(
        "cyan",
        f"\n\nBuilding Documentation for `{package_name}`",
        "... Please be Patient."
    )
    doc_dir = os.path.join(project_dir, "docs")
    src_dir = os.path.join(project_dir, package_name)

    # Cleanup Before Build
    cleanup(doc_dir)

    template_dir = os.path.join(project_dir, "templates")
    # logo_path = os.path.join(template_dir, "logo.svg")

    subprocess.run([
        "pdoc",
        # "--no-show-source",
        "--no-browser",
        "-d",
        "google",
        # "--logo",
        # logo_path,
        "-t",
        template_dir,
        "-o",
        doc_dir,
        src_dir
    ])

    print_color("green", "\n\nFinished Building Documentation.")


def install_wheel():
    print_color("cyan", f"\n\nInstalling Latest Build of {package_name}")

    # Uninstall Previous Version (important when version is not updated from current)
    subprocess.run(["pip", "uninstall", package_name], input="y", text=True)

    # Install Most Recently Built Wheel
    dist = os.path.join(project_dir, "dist")
    wheel_path = [str(i) for i in Path(dist).glob("*.whl")][0]
    subprocess.run(["pip", "install", wheel_path])

    print_color("green", "\nInstallation Completed Successfully!")


def main():
    # Cleanup Before Build
    remnants = ["dist", "build", f"{package_name}/{package_name}.egg-info"]
    for r in remnants:
        cleanup(r)

    # Build the Wheel
    subprocess.run(["python", "setup.py", "bdist_wheel"])

    # Cleanup after build
    for r in ["build", f"{package_name}.egg-info"]:
        cleanup(r)

    dist = os.path.join(project_dir, "dist")
    non_wheels = [os.path.join(dist, f) for f in os.listdir(dist) if os.path.splitext(f)[-1] != ".whl"]

    for fp in non_wheels:
        os.remove(fp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"{package_name} Build")
    parser.add_argument("--docs", action="store_true", help="Build Package Documentation")
    parser.add_argument("--install", action="store_true", help="Install Freshly Built Wheel.")
    args = parser.parse_args()

    main()

    if args.docs:
        build_docs()

    if args.install:
        install_wheel()
