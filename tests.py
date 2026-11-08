"""
Юнит-тесты для validation.py и operations.py
Запуск:
    python -m unittest tests -v
"""
import unittest
from unittest.mock import patch
import logger
import validation
import operations

class TestValidateRange(unittest.TestCase):
    """Проверка границ validate_range(5 тестов)"""
    def test_inside(self):
        ok,msg=validation.validate_range(50.0,5.0,500.0)
        self.assertTrue(ok)
        self.assertEqual(msg,"")
    def test_on_lower(self):
        ok,_=validation.validate_range(5.0,5.0,500.0)
        self.assertTrue(ok)
    def test_on_upper(self):
        ok,_=validation.validate_range(500.0,5.0,500.0)
        self.assertTrue(ok)
    def test_below(self):
        ok,msg=validation.validate_range(4.9,5.0,500.0)
        self.assertFalse(ok)
        self.assertIn("нижней",msg)

    def test_above(self):
        ok,msg=validation.validate_range(500.1,5.0,500.0)
        self.assertFalse(ok)
        self.assertIn("верхней",msg)

class TestInputSize(unittest.TestCase):
    """Циклический ввод размера сечения(3 теста)"""
    def setUp(self):
        logger.clear()
    @patch("validation.input",side_effect=["abc","600","50"])
    def test_cycle_then_valid(self,_mock):
        self.assertEqual(validation.input_size("d:"),50.0)
    @patch("validation.input",side_effect=["5"])
    def test_lower_boundary(self,_mock):
        self.assertEqual(validation.input_size("d:"),5.0)
    @patch("validation.input",side_effect=["500"])
    def test_upper_boundary(self,_mock):
        self.assertEqual(validation.input_size("d:"),500.0)

class TestInputSpeed(unittest.TestCase):
    """Циклический ввод скорости потока(3 теста)"""
    def setUp(self):
        logger.clear()
    @patch("validation.input", side_effect=["0.05","20","2.5"])
    def test_cycle_then_valid(self, _mock):
        self.assertEqual(validation.input_speed(),2.5)
    @patch("validation.input", side_effect=["0.1"])
    def test_lower_boundary(self,_mock):
        self.assertEqual(validation.input_speed(),0.1)
    @patch("validation.input",side_effect=["10"])
    def test_upper_boundary(self,_mock):
        self.assertEqual(validation.input_speed(),10.0)

class TestOperations(unittest.TestCase):
    """Проверка расчётов и классификации(9 тестов)"""
    def test_area_circle(self):
        self.assertAlmostEqual(operations.area_circle(100),0.0078539816,places=7)
    def test_area_rectangle(self):
        self.assertAlmostEqual(operations.area_rectangle(100,200),0.02,places=7)
    def test_area_ring(self):
        self.assertAlmostEqual(operations.area_ring(200,100),0.0235619449,places=7)
    def test_flow_rate(self):
        self.assertAlmostEqual(operations.flow_rate(0.01,2),72.0,places=7)
    def test_class_small(self):
        self.assertEqual(operations.diameter_class(10),"малое сечение")
    def test_class_boundary_25(self):
        self.assertEqual(operations.diameter_class(25),"нормальное сечение")
    def test_class_normal(self):
        self.assertEqual(operations.diameter_class(50),"нормальное сечение")
    def test_class_boundary_200(self):
        self.assertEqual(operations.diameter_class(200),"нормальное сечение")
    def test_class_large(self):
        self.assertEqual(operations.diameter_class(201),"крупное сечение")

if __name__ == "__main__":
    unittest.main()