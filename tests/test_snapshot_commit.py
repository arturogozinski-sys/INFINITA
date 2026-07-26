import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from narzedzia.zbuduj_snapshot_claude import build_snapshot  # noqa: E402


class TestSnapshotZCommita(unittest.TestCase):
    def test_brudny_working_tree_nie_zmienia_zawartosci_snapshotu(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "config", "core.autocrlf", "false"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.email", "test@example.invalid"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.name", "Test"],
                check=True,
            )
            tracked = repo / "dane.txt"
            tracked.write_text("stan commita\n", encoding="utf-8", newline="\n")
            subprocess.run(["git", "-C", str(repo), "add", "dane.txt"], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "commit", "-q", "-m", "stan bazowy"],
                check=True,
            )
            sha = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "HEAD"],
                check=True,
                text=True,
                encoding="utf-8",
                capture_output=True,
            ).stdout.strip()

            tracked.write_text("niezapisana zmiana\n", encoding="utf-8", newline="\n")
            (repo / "niesledzony.txt").write_text("nie pakuj\n", encoding="utf-8")
            output = build_snapshot(repo, Path(tmp) / "dist")

            with zipfile.ZipFile(output) as archive:
                self.assertEqual(archive.read("dane.txt"), b"stan commita\n")
                self.assertNotIn("niesledzony.txt", archive.namelist())
                manifest = archive.read("CLAUDE_SNAPSHOT.yaml").decode("utf-8")
                self.assertIn(f'commit_bazowy: "{sha}"', manifest)
                self.assertIn("zawartosc_working_tree: false", manifest)


if __name__ == "__main__":
    unittest.main(verbosity=2)
