'''
Created on Apr 09, 2014

@author: silas@reciprocitylabs.com

Interface for reporting results from the json
'''

import json
import os
from time import strftime

from testcase import base_metrics_dir

class Reporter(object):

    def single_function_recent_history(self, result_dicts, lastn=5):
        """Given list of benchmark dicts of the same test, return dict with lastn test results for it; leave blank if none, average it if there are multiple.
        """
        ordered_dicts = [x for x in result_dicts if 'timestamp' in x]
        ordered_dicts = sorted(ordered_dicts, key=lambda x: x['timestamp'])
        out_dict = {}
        for single_dict in ordered_dicts:
            for key in single_dict["results"]:
                vals = single_dict["results"][key]
                if not isinstance(vals, list):
                    continue
                if key in out_dict:
                    out_dict[key] += vals
                else:
                    out_dict[key] = vals
                # just save the lastn values
                out_dict[key] = out_dict[key][-lastn:]
        # add on the lastn time parameters as a key
        out_dict['overall_time'] = [x['results']['overall_time'] for x in ordered_dicts[-lastn:]]
        return out_dict


class Collector(object):
    """for getting and parsing the relevant subset of the result files"""

    def benchmarks_dir(self):
        THIS_ABS_PATH = os.path.abspath(os.path.dirname(__file__))
        ROOT_PATH = os.path.abspath(os.path.join(THIS_ABS_PATH, '../'))
        return os.path.join(ROOT_PATH, 'Benchmarks')

    def result_files(self):
        return [os.path.join(base_metrics_dir(), pth) for pth in os.listdir(base_metrics_dir()) if pth[-1] in "0123456789"]

    def single_test_history(self, testname, files):
        """Given test name and list of files, return corresponding list of dicts"""
        out_dicts = []
        match_files = [f for f in files if testname in f]
        for match_file in match_files:
            with open(match_file, "r") as g:
                out_dicts.append(json.loads(g.read()))
        return out_dicts

    def prettify(self, result_dict):
        outstring = ""
        outstring += "Latest total run times: {}\n".format(result_dict.get('overall_time'))
        for key, value in result_dict.iteritems():
            outstring += "{0}: {1}\n".format(key, value)
        return outstring

    def generate_report(self):
        """write to both a "latest" file an a timestamped one"""
        all_results = self.result_files()
        r = Reporter()
        out_root = self.benchmarks_dir()
        latest_file = os.path.join(self.benchmarks_dir(), "benchmark_report.txt")
        time_stamp = strftime("%Y_%m_%d_%H_%M_%S")
        historical_file = os.path.join(self.benchmarks_dir(), "benchmark_report_{}.txt".format(time_stamp))
        outfile1 = open(latest_file, "w")
        outfile2 = open(historical_file, "w")
        for test in TEST_LIST:
            outfile1.write("{}\n".format(test))
            outfile2.write("{}\n".format(test))
            results = r.single_function_recent_history(self.single_test_history(test, all_results))
            outfile1.write("{}\n".format(self.prettify(results)))
            outfile2.write("{}\n".format(self.prettify(results)))
        outfile1.close()
        outfile1.close()


TEST_LIST = [
"TestContractCreate",
"TestDataAssetCreate",
"TestFacilityCreate",
"TestMarketCreate",
"TestOrgGroupCreate",
"TestPolicyCreate",
"TestProcessCreate",
"TestProductCreate",
"TestProjectCreate",
"TestProgramCreate",
"TestRegulationCreate",
"TestSystemCreate",
"TestControlCreate",
"TestObjectiveCreate",
"TestContractEdit",
"TestControlEdit",
"TestDataAssetEdit",
"TestFacilityEdit",
"TestMarketEdit",
"TestOrgGroupEdit",
"TestPolicyEdit",
"TestProcessEdit",
"TestProductEdit",
"TestProgramEdit",
"TestProjectEdit",
"TestRegulationEdit",
"TestSystemEdit",
"TestObjectiveEdit",
"TestProgramMapLHN",
"TestProgramMapWidget",
"TestContractMapLHN",
"TestContractMapWidget",
"TestPolicyMapLHN",
"TestPolicyMapWidget",
"TestRegulationMapLHN",
"TestRegulationMapWidget",
"TestSystemsMapLHN",
"TestProcessMapLHN",
"TestDataAssetMapLHN",
"TestProductMapLHN",
"TestProjectMapLHN",
"TestFacilityMapLHN",
"TestMarketMapLHN",
"TestOrgGroupMapLHN",
"TestSystemMapWidget",
"TestProcessMapWidget",
"TestDataAssetMapWidget",
"TestProductMapWidget",
"TestProjectMapWidget",
"TestFacilityMapWidget",
"TestMarketMapWidget",
"TestOrgGroupMapWidget",
"TestControlMapLHN",
"TestControlMapWidget",
"TestProgramAudit",
]

if __name__ == "__main__":
    c = Collector()
    c.generate_report()
