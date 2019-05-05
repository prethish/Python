import test_base

from core import config
from core import ProgressPrint
from core import logger


class TestSubClass(config.Borg):
    def __init__(self, var):
        config.Borg.__init__(self)
        self.var = var or "default"


class TestBorg(test_base.TestBase):

    def test_multiple_instances(self):
        instance_a = TestSubClass("")
        self.assertEqual(
            instance_a.var,
            "default"
        )

        instance_b = TestSubClass("new")
        self.assertEqual(
            instance_a.var,
            "new"
        )


class TestEnvVariableExpander(test_base.TestBase):
    def setUp(self):
        self.expander = config.EnvVariableExpander()

    def test_populate_default_values_keys(self):

        self.assertTrue(
            all(
                (
                    hasattr(self.expander, var)
                    for var in ("_home", "_user", "_temp", "_host")
                )
            )
        )

    def test_populate_default_values(self):
        self.assertEqual(
            self.expander._home,
            test_base.os.path.expanduser('~')
        )

    def test_get_item(self):
        self.assertEqual(
            self.expander["home"],
            test_base.os.path.expanduser('~')
        )

    def test_get_item_not_present(self):
        self.assertRaises(
            KeyError,
            self.expander.__getitem__,
            "random"
        )

    def test_convert_str(self):
        self.assertEqual(
            self.expander.convert_str("$HOME/$USER/$HOST/test"),
            (
                True,
                "%s/%s/%s/test" % (
                    test_base.os.path.expanduser("~"),
                    config.getpass.getuser(),
                    config.socket.gethostname()
                )
            )
        )

    def test_convert_str_invalid(self):
        self.assertEqual(
            self.expander.convert_str("$HOME1/$USER/$HOST/test"),
            (
                False,
                "$HOME1/%s/%s/test" % (
                    config.getpass.getuser(),
                    config.socket.gethostname()
                )
            )
        )
