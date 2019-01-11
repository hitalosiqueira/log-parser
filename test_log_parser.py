import unittest
import log_parser as lp


class TestParser(unittest.TestCase):
  def setUp(self):
    lp.parse()
  
  def tearDown(self):
    lp.data = []
    lp.results = []
    lp.drivers_best_laps = []
    lp.race_best_lap = {}
    lp.drivers_avg_speed = []
    lp.drivers_diff_to_first = []

  """ given a valid code it should return the corresponding driver's name """
  def test_extract_name(self):
    self.assertEqual(lp.extract_name('038'), 'F.MASSA')
    self.assertEqual(lp.extract_name('002'), 'K.RAIKKONEN')
    self.assertEqual(lp.extract_name('033'), 'R.BARRICHELLO')
    self.assertEqual(lp.extract_name('023'), 'M.WEBBER')
    self.assertEqual(lp.extract_name('015'), 'F.ALONSO')
    self.assertEqual(lp.extract_name('011'), 'S.VETTEL')

  """ given a valid code it should return the corresponding driver's lap number """
  def test_extract_laps(self):
    self.assertEqual(lp.extract_laps('038'), 4)
    self.assertEqual(lp.extract_laps('002'), 4)
    self.assertEqual(lp.extract_laps('033'), 4)
    self.assertEqual(lp.extract_laps('023'), 4)
    self.assertEqual(lp.extract_laps('015'), 4)
    self.assertEqual(lp.extract_laps('011'), 3)

  """ given a valid code it should return the corresponding driver's total race time in seconds """
  def test_extract_time(self):
    self.assertEqual(lp.extract_race_time('038'), 251.578)
    self.assertEqual(lp.extract_race_time('002'), 255.153)
    self.assertEqual(lp.extract_race_time('033'), 256.08)
    self.assertEqual(lp.extract_race_time('023'), 257.722)
    self.assertEqual(lp.extract_race_time('015'), 294.221)
    self.assertEqual(lp.extract_race_time('011'), 387.276)

  """ given a valid code it should return the corresponding driver's best lap """
  def test_extract_best_lap(self):
    self.assertEqual(lp.extract_best_lap('038'), 62.769)
    self.assertEqual(lp.extract_best_lap('002'), 63.076)
    self.assertEqual(lp.extract_best_lap('033'), 63.716)
    self.assertEqual(lp.extract_best_lap('023'), 64.216)
    self.assertEqual(lp.extract_best_lap('015'), 67.011)
    self.assertEqual(lp.extract_best_lap('011'), 78.097)

  """ given a valid code it should return the corresponding driver's avg speed """
  def test_extract_avg_speed(self):
    self.assertEqual(lp.extract_avg_speed('038'), 44.246)
    self.assertEqual(lp.extract_avg_speed('002'), 43.627)
    self.assertEqual(lp.extract_avg_speed('033'), 43.468)
    self.assertEqual(lp.extract_avg_speed('023'), 43.191)
    self.assertEqual(lp.extract_avg_speed('015'), 38.066)
    self.assertEqual(lp.extract_avg_speed('011'), 25.746)

  """ given a valid code it should return the corresponding driver's diff to first """
  def test_extract_diff_to_first(self):
    lp.build_result()
    self.assertEqual(lp.extract_diff_to_first('038'), 0.000)
    self.assertEqual(lp.extract_diff_to_first('002'), 3.575)
    self.assertEqual(lp.extract_diff_to_first('033'), 4.502)
    self.assertEqual(lp.extract_diff_to_first('023'), 6.144)
    self.assertEqual(lp.extract_diff_to_first('015'), 42.643)
    self.assertEqual(lp.extract_diff_to_first('011'), 135.698)

  """ given the log data it should return the race result as list of dictionaries """
  def test_build_result(self):
    lp.build_result()
    self.assertDictEqual(lp.results[0], {'code': '038', 'name': 'F.MASSA', 'laps': 4, 'time': 251.578, 'position': 1})
    self.assertDictEqual(lp.results[1], {'code': '002', 'name': 'K.RAIKKONEN', 'laps': 4, 'time': 255.153, 'position': 2})
    self.assertDictEqual(lp.results[2], {'code': '033', 'name': 'R.BARRICHELLO', 'laps': 4, 'time': 256.08, 'position': 3})
    self.assertDictEqual(lp.results[3], {'code': '023', 'name': 'M.WEBBER', 'laps': 4, 'time': 257.722, 'position': 4})
    self.assertDictEqual(lp.results[4], {'code': '015', 'name': 'F.ALONSO', 'laps': 4, 'time': 294.221, 'position': 5})
    self.assertDictEqual(lp.results[5], {'code': '011', 'name': 'S.VETTEL', 'laps': 3, 'time': 387.276, 'position': 6})

  """ given the log data it should return the all the drivers best lap as list of dictionaries """
  def test_build_drivers_best_lap(self):
    lp.build_result()
    lp.build_drivers_best_lap()
    self.assertDictEqual(lp.drivers_best_laps[0], {'name': 'F.MASSA', 'best_lap': 62.769})
    self.assertDictEqual(lp.drivers_best_laps[1], {'name': 'K.RAIKKONEN', 'best_lap': 63.076})
    self.assertDictEqual(lp.drivers_best_laps[2], {'name': 'R.BARRICHELLO','best_lap': 63.716})
    self.assertDictEqual(lp.drivers_best_laps[3], {'name': 'M.WEBBER', 'best_lap': 64.216})
    self.assertDictEqual(lp.drivers_best_laps[4], {'name': 'F.ALONSO', 'best_lap': 67.011})
    self.assertDictEqual(lp.drivers_best_laps[5], {'name': 'S.VETTEL', 'best_lap': 78.097})

  """ given the log data it should return the race best lap as list of dictionaries """
  def test_race_best_lap(self):
    lp.build_result()
    lp.build_drivers_best_lap()
    lp.build_race_best_lap()
    self.assertDictEqual(lp.race_best_lap, {'name': 'F.MASSA', 'best_lap': 62.769})
  
  """ given the log data it should return the the drivers avg speed as a list of dictionaries """
  def test_drivers_avg_speed(self):
    lp.build_result()
    lp.build_drivers_avg_speed()
    self.assertDictEqual(lp.drivers_avg_speed[0], {'name': 'F.MASSA', 'avg_speed': 44.246})
    self.assertDictEqual(lp.drivers_avg_speed[1], {'name': 'K.RAIKKONEN', 'avg_speed': 43.627})
    self.assertDictEqual(lp.drivers_avg_speed[2], {'name': 'R.BARRICHELLO','avg_speed': 43.468})
    self.assertDictEqual(lp.drivers_avg_speed[3], {'name': 'M.WEBBER', 'avg_speed': 43.191})
    self.assertDictEqual(lp.drivers_avg_speed[4], {'name': 'F.ALONSO', 'avg_speed': 38.066})
    self.assertDictEqual(lp.drivers_avg_speed[5], {'name': 'S.VETTEL', 'avg_speed': 25.746})
  
  """ given the log data it should return the the drivers diff to first as a list of dictionaries """
  def test_drivers_diff_to_first(self):
    lp.build_result()
    lp.build_drivers_diff_to_first()
    self.assertDictEqual(lp.drivers_diff_to_first[0], {'name': 'F.MASSA', 'to_first': 0.0})
    self.assertDictEqual(lp.drivers_diff_to_first[1], {'name': 'K.RAIKKONEN', 'to_first': 3.575})
    self.assertDictEqual(lp.drivers_diff_to_first[2], {'name': 'R.BARRICHELLO','to_first': 4.502})
    self.assertDictEqual(lp.drivers_diff_to_first[3], {'name': 'M.WEBBER', 'to_first': 6.144})
    self.assertDictEqual(lp.drivers_diff_to_first[4], {'name': 'F.ALONSO', 'to_first': 42.643})
    self.assertDictEqual(lp.drivers_diff_to_first[5], {'name': 'S.VETTEL', 'to_first': 135.698})

if __name__ == "__main__":
  unittest.main() 