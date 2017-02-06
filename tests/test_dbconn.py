import pyodbc
import unittest

class TestDBConnection(unittest.TestCase):

    def test_connection(self):
        """Returns connection to OTP database on OTP server"""
        with open(r'hdrpackage\\server_config.cfg', 'r') as f:
            conn_string = f.read()
        connection = pyodbc.connect(conn_string)
        self.assertTrue(connection)

if __name__ == '__main__':
    unittest.main()