from Reporter import Reporter

from unittest import TestCase, main


result_dict1 = {"timestamp": "2014_04_11_05_32_19", "name": "TestProjectCreate", "results": {"navigateToObjectAndOpenObjectEditWindow": [8.070629], "verifyObjectIsCreatedinLHN": [6.616874], "saveObjectData": [8.578599], "authorizeGAPI": [5.183145], "submitGoogleCredentials": [1.380699], "populateNewObjectData": [1.620795], "createObject": [17.659138], "showObjectLinkWithSearch": [3.508342], "searchFor": [0.635745], "uncheckMyWorkBox": [0.220125], "closeOtherWindows": [0.012524, 0.013109, 0.01158], "login": [11.447577], "openCreateNewObjectWindowFromLhn": [0.609956], "deleteObject": [37.263289], "overall_time": 79.896487}}

result_dict2 = {"timestamp": "2014_04_11_19_42_03", "name": "TestProjectCreate", "results": {"navigateToObjectAndOpenObjectEditWindow": [10.498568], "verifyObjectIsCreatedinLHN": [6.25393], "saveObjectData": [43.652339], "authorizeGAPI": [5.201087], "submitGoogleCredentials": [1.465374], "populateNewObjectData": [1.364613], "createObject": [52.076119], "showObjectLinkWithSearch": [1.93819], "searchFor": [0.616981], "uncheckMyWorkBox": [0.231483], "closeOtherWindows": [0.010294, 0.011969, 0.012411], "login": [11.684699], "openCreateNewObjectWindowFromLhn": [0.563221], "deleteObject": [7.443858], "overall_time": 87.737129}}

class TestResultDictProcess(TestCase):

    def setUp(self):
        self.r1 = Reporter()

    def tearDown(self):
        pass

    def test_single_result(self):
        actual = self.r1.single_function_recent_history([result_dict1])
        actual_gcred = actual["submitGoogleCredentials"][0]
        actual_login = actual["login"][0]
        self.assertAlmostEqual(1.3807, actual_gcred, 4)
        self.assertAlmostEqual(11.4476, actual_login, 4)

    def test_several_results(self):
        actual = self.r1.single_function_recent_history([result_dict2, result_dict1])
        actual_close = actual["closeOtherWindows"]
        self.assertAlmostEqual(0.0131, actual_close[0], 4)

if __name__ == "__main__":
    main()
