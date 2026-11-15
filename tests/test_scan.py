import glob
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "skills", "unbot-voice", "scripts"))
import scan  # noqa: E402

SCAN = os.path.join(ROOT, "skills", "unbot-voice", "scripts", "scan.py")
WALDEN = (
    "When I wrote the following pages, or rather the bulk of them, I lived alone, in the woods, a mile from "
    "any neighbor, in a house which I had built myself, on the shore of Walden Pond, in Concord, Massachusetts, "
    "and earned my living by the labor of my hands only. I lived there two years and two months. At present I am "
    "a sojourner in civilized life again. I should not obtrude my affairs so much on the notice of my readers if "
    "very particular inquiries had not been made by my townsmen concerning my mode of life. Some have asked what "
    "I got to eat; if I did not feel lonesome; if I was not afraid; and the like. In most books, the I, or first "
    "person, is omitted; in this it will be retained; that, in respect to egotism, is the main difference."
)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


class EvalCorpus(unittest.TestCase):
    def test_ai_drafts_score_high(self):
        for f in glob.glob(os.path.join(ROOT, "evals", "before", "*.txt")):
            self.assertGreater(scan.scan(read(f))["score"], 50, f)

    def test_rewrites_score_low(self):
        for f in glob.glob(os.path.join(ROOT, "evals", "after", "*.txt")):
            self.assertLess(scan.scan(read(f))["score"], 10, f)

    def test_human_prose_scores_low(self):
        self.assertLess(scan.scan(WALDEN)["score"], 10)


class Behaviour(unittest.TestCase):
    def test_quoted_mentions_ignored(self):
        text = 'Words like "delve" and "tapestry" were common tells in 2023.'
        self.assertEqual(scan.scan(text)["hits"], [])
        self.assertTrue(scan.scan(text, include_quotes=True)["hits"])

    def test_code_blocks_ignored(self):
        text = "Example:\n\n```\nI hope this helps! Let me delve into it.\n```\n"
        self.assertEqual(scan.scan(text)["hits"], [])

    def test_line_numbers(self):
        hit = scan.scan("Fine line.\nSecond line.\nI hope this helps.")["hits"][0]
        self.assertEqual(hit["line"], 3)

    def test_threshold_exit_codes(self):
        bad = os.path.join(ROOT, "evals", "before", "03-cold-email.txt")
        good = os.path.join(ROOT, "evals", "after", "03-cold-email.txt")
        run = lambda f: subprocess.run([sys.executable, SCAN, f, "--threshold", "25"], capture_output=True).returncode
        self.assertEqual(run(bad), 1)
        self.assertEqual(run(good), 0)

    def test_short_files_never_fail(self):
        short = subprocess.run([sys.executable, SCAN, "--threshold", "1"], input=b"I hope this helps!",
                               capture_output=True)
        self.assertEqual(short.returncode, 0)


if __name__ == "__main__":
    unittest.main()
