import unittest
import typewise_alert


class TypewiseTest(unittest.TestCase):

    def test_infers_breach_as_per_limits(self):
        self.assertTrue(typewise_alert.infer_breach(20, 50, 100) == 'TOO_LOW')
        self.assertTrue(typewise_alert.infer_breach(100, 0, 45) == 'TOO_HIGH')
        self.assertTrue(typewise_alert.infer_breach(25, 0, 40) == 'NORMAL')

    def test_checks_input_data_valid(self):
        self.assertTrue(typewise_alert.check_if_input_is_valid('PASSIVE_COOLING', 80))
        self.assertFalse(typewise_alert.check_if_input_is_valid(None, 40))
        self.assertFalse(typewise_alert.check_if_input_is_valid('PASSIVE_COOLING', None))
        self.assertFalse(typewise_alert.check_if_input_is_valid('EXTRA_COOLING', 80))

    def test_yields_alert_for_breaches(self):
        self.assertEqual(typewise_alert.check_and_alert('email', {'coolingType': 'PASSIVE_COOLING'}, 120), 'EMAIL_SENT')
        self.assertEqual(typewise_alert.check_and_alert('controller', {'coolingType': 'HI_ACTIVE_COOLING'}, -20), 'CONTROLLER_ACTIVATED')
        self.assertEqual(typewise_alert.check_and_alert('email', {'coolingType': 'MED_ACTIVE_COOLING'}, 90), 'EMAIL_SENT')


if __name__ == '__main__':
    unittest.main()
