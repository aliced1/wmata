import unittest
import driver

class Testing(unittest.TestCase):
    driver = driver.Driver()
    driver.draw_screen()
    pass

if __name__ == '__main__':
    unittest.main()