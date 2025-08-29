import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_command(command, cwd=None):
    """Run a system command and log it."""
    logger.info(f"Running: {' '.join(command)}")
    try:
        result = subprocess.run(command, cwd=cwd, check=True,
                                capture_output=True, text=True)
        logger.info(result.stdout.strip())
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(e.stderr.strip())
        raise


def init_git_repo(project_path):
    """Initialize Git repository if not already initialized."""
    if not os.path.exists(os.path.join(project_path, ".git")):
        run_command(["git", "init"], cwd=project_path)
    else:
        logger.info("Git already initialized.")


def parse_gitignore(content: str) -> set:
    """Parse gitignore content into a set of rules."""
    return {line.strip() for line in content.splitlines() if line.strip() and not line.startswith('#')}


def setup_gitignore(project_path):
    """Write .gitignore with correct rules for dataset and DVC."""
    required_rules = {
        # Ignore data but allow DVC files
        "/data/*",
        "!/data/*.dvc",
        # Track DVC files
        "!.dvc/",
        "!*.dvc",
        # Ignore DVC cache
        ".dvc/cache",
        ".dvc/tmp",
        ".dvc/plots",
        # Python
        "*.pyc",
        "__pycache__/",

        ".pytest_cache/"
    }

    gitignore_path = os.path.join(project_path, ".gitignore")

    # Read existing rules if file exists
    existing_rules = set()
    if os.path.exists(gitignore_path):
        with open(gitignore_path) as f:
            existing_rules = parse_gitignore(f.read())

    # Combine rules, maintaining order
    final_rules = sorted(required_rules.union(existing_rules))

    # Write updated .gitignore
    with open(gitignore_path, "w") as f:
        f.write("\n".join(final_rules) + "\n")

    logger.info("✅ .gitignore updated with correct DVC rules")


def init_dvc(project_path):
    """Initialize DVC repository cleanly."""
    try:
        # Force reinit DVC
        run_command(["dvc", "init", "--force"], cwd=project_path)
        # Configure DVC
        run_command(["dvc", "config", "core.analytics", "false"], cwd=project_path)
        logger.info("✅ DVC initialized")
    except Exception as e:
        logger.error(f"DVC init failed: {e}")
        raise


def track_dataset(project_path):
    """Track dataset with DVC."""
    dataset_path = os.path.join(project_path, "data", "dataset")
    try:
        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path, exist_ok=True)
            # Create sample file
            with open(os.path.join(dataset_path, "sample.txt"), "w") as f:
                f.write("Sample content\n")

        run_command(["dvc", "add", "data/dataset"], cwd=project_path)
        logger.info("✅ Dataset tracked with DVC")
    except Exception as e:
        logger.error(f"Failed to track dataset: {e}")
        raise


def commit_changes(project_path):
    """Commit DVC configuration."""
    try:
        # First, update .gitignore
        setup_gitignore(project_path)

        # Force add DVC files
        dvc_files = [
            ".dvc",
            ".dvc/config",
            ".gitignore",
            "data/dataset.dvc"
        ]

        for file in dvc_files:
            file_path = os.path.join(project_path, file)
            if os.path.exists(file_path):
                # Use -f to override any ignore rules
                run_command(["git", "add", "-f", file], cwd=project_path)

        try:
            run_command(["git", "commit", "-m", "Setup DVC and track dataset"], cwd=project_path)
            logger.info("✅ Changes committed")
        except subprocess.CalledProcessError as e:
            if "nothing to commit" in str(e.stderr):
                logger.info("No changes to commit")
            else:
                raise
    except Exception as e:
        logger.error(f"Commit failed: {e}")
        raise


def main():
    project_path = os.getcwd()
    logger.info("=== Setting up Git and DVC ===")

    init_git_repo(project_path)
    setup_gitignore(project_path)
    init_dvc(project_path)
    track_dataset(project_path)
    commit_changes(project_path)

    logger.info("✅ Git + DVC setup complete.")


if __name__ == "__main__":
    main()
    logger.info("✅ Git + DVC setup complete.")


if __name__ == "__main__":
    main()
