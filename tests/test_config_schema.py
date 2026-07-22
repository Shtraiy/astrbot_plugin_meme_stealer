import json
import unittest
from pathlib import Path


class ConfigSchemaTests(unittest.TestCase):
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
