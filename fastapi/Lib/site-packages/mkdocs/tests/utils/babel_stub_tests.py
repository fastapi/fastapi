import unittest

from mkdocs.utils.babel_stub import Locale, UnknownLocaleError


class BabelStubTests(unittest.TestCase):
    def test_locale_language_only(self):
        locale = Locale("es")
        self.assertEqual(locale.language, "es")
        self.assertEqual(locale.territory, "")
        self.assertEqual(str(locale), "es")

    def test_locale_language_territory(self):
        locale = Locale("es", "ES")
        self.assertEqual(locale.language, "es")
        self.assertEqual(locale.territory, "ES")
        self.assertEqual(str(locale), "es_ES")

    def test_parse_locale_language_only(self):
        locale = Locale.parse("fr", "_")
        self.assertEqual(locale.language, "fr")
        self.assertEqual(locale.territory, "")
        self.assertEqual(str(locale), "fr")

    def test_parse_locale_language_territory(self):
        locale = Locale.parse("fr_FR", "_")
        self.assertEqual(locale.language, "fr")
        self.assertEqual(locale.territory, "FR")
        self.assertEqual(str(locale), "fr_FR")

    def test_parse_locale_language_territory_sep(self):
        locale = Locale.parse("fr-FR", "-")
        self.assertEqual(locale.language, "fr")
        self.assertEqual(locale.territory, "FR")
        self.assertEqual(str(locale), "fr_FR")

    def test_parse_locale_bad_type(self):
        with self.assertRaises(TypeError):
            Locale.parse(["list"], "_")

    def test_parse_locale_invalid_characters(self):
        with self.assertRaises(ValueError):
            Locale.parse("42", "_")

    def test_parse_locale_bad_format(self):
        with self.assertRaises(ValueError):
            Locale.parse("en-GB", "_")

    def test_parse_locale_bad_format_sep(self):
        with self.assertRaises(ValueError):
            Locale.parse("en_GB", "-")

    def test_parse_locale_unknown_locale(self):
        with self.assertRaises(UnknownLocaleError):
            Locale.parse("foo", "_")
