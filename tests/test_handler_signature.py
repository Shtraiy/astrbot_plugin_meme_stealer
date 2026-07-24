import ast
import unittest
from pathlib import Path


class HandlerSignatureTests(unittest.TestCase):
    def test_on_message_accepts_pipeline_extra_arguments(self):
        source = Path(__file__).resolve().parents[1] / "main.py"
        module = ast.parse(source.read_text(encoding="utf-8"))
        handler = next(
            node
            for node in ast.walk(module)
            if isinstance(node, ast.AsyncFunctionDef) and node.name == "on_message"
        )

        self.assertIsNotNone(handler.args.vararg)
        self.assertIsNotNone(handler.args.kwarg)


if __name__ == "__main__":
    unittest.main()
