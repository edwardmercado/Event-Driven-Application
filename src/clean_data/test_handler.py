import json, unittest, sys, os, requests

from app import usURL, hopkinsURL, dynamoDBTableName, snsTopicName

class TestLambda(unittest.TestCase):

    def test_resources(self):
        self.assertIsNotNone(usURL)
        self.assertIsNotNone(hopkinsURL)
        self.assertIsNotNone(dynamoDBTableName)
        self.assertIsNotNone(snsTopicName)

    def test_linksIfReachable(self):
        firstLink = requests.get(usURL)
        self.assertEqual(firstLink.status_code, 200)
        
        secondLink = requests.get(hopkinsURL)
        self.assertEqual(secondLink.status_code, 200)


if __name__ == '__main__':
    unittest.main()