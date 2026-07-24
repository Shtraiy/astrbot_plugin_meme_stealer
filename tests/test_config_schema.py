import json
import unittest
from pathlib import Path


class ConfigSchemaTests(unittest.TestCase):
    def test_metadata_points_to_the_plugin_repository(self):
        root = Path(__file__).resolve().parents[1]
        metadata = (root / "metadata.yaml").read_text(encoding="utf-8")

        repo_line = next(
            line for line in metadata.splitlines() if line.startswith("repo:")
        )
        self.assertEqual(
            repo_line,
            "repo: https://github.com/Shtraiy/astrbot_plugin_meme_stealer",
        )

    def test_plugin_display_name_is_meme_master(self):
        root = Path(__file__).resolve().parents[1]

        metadata = (root / "metadata.yaml").read_text(encoding="utf-8")
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("display_name: 表情包偷取大师", metadata)
        self.assertIn("# AstrBot 表情包偷取大师", readme)

    def test_schema_uses_astrbot_plugin_config_shape(self):
        schema = json.loads(
            (Path(__file__).resolve().parents[1] / "_conf_schema.json").read_text(
                encoding="utf-8"
            )
        )
        supported_types = {"string", "bool", "int", "float", "list", "object"}

        self.assertNotIn("properties", schema)
        self.assertNotIn("type", schema)
        for key, value in schema.items():
            self.assertIsInstance(value, dict, key)
            self.assertIn(value.get("type"), supported_types, key)

    def test_health_check_interval_defaults_to_five_minutes(self):
        schema = json.loads(
            (Path(__file__).resolve().parents[1] / "_conf_schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(schema["health_check_interval"]["default"], 300)

    def test_model_settings_use_astrbot_provider_selector(self):
        schema = json.loads(
            (Path(__file__).resolve().parents[1] / "_conf_schema.json").read_text(
                encoding="utf-8"
            )
        )
        provider_settings = (
            "vision_provider_id",
            "scene_provider_id",
            "reply_scene_provider_id",
            "library_index_provider_id",
        )

        for key in provider_settings:
            self.assertEqual(schema[key].get("_special"), "select_provider", key)

        self.assertEqual(
            schema["perceptual_dedupe_enabled"]["description"],
            "在模型请求前检查相似图片重复，Pillow 缺失时自动回退为精确去重",
        )
        self.assertEqual(
            schema["perceptual_duplicate_threshold"]["description"],
            "感知哈希的最大响应距离，值越小越严格",
        )


if __name__ == "__main__":
    unittest.main()
