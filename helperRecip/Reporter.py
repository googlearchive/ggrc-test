'''
Created on Apr 09, 2014

@author: silas@reciprocitylabs.com

Interface for reporting results from the json
'''

from testcase import base_metrics_dir

class Reporter(object):

    def single_function_recent_history(self, result_dicts, lastn=5):
        """Given list of benchmark dicts of the same test, return dict with lastn test results for it; leave blank if none, average it if there are multiple.
        """
        ordered_dicts = sorted(result_dicts, key=lambda x: x['timestamp'])
        out_dict = {}
        for single_dict in ordered_dicts:
            for key in single_dict["results"]:
                if not isinstance(single_dict["results"][key], list):
                    continue
                if key in out_dict:
                    out_dict[key] += single_dict["results"][key]
                else:
                    out_dict[key] = single_dict["results"][key]
                # just save the lastn values
                out_dict[key] = out_dict[key][-lastn:]
        return out_dict


class Collector(object):
    """for getting and parsing the relevant subset of the result files"""


TEST_LIST = [
TestContractCreate
TestDataAssetCreate
TestFacilityCreate
TestMarketCreate
TestOrgGroupCreate
TestPolicyCreate
TestProcessCreate
TestProductCreate
TestProjectCreate
TestProgramCreate
TestRegulationCreate
TestSystemCreate
TestControlCreate
TestObjectiveCreate
from Edit.TestContractEdit import TestContractEdit
from Edit.TestControlEdit import TestControlEdit
from Edit.TestDataAssetEdit import TestDataAssetEdit
from Edit.TestFacilityEdit import TestFacilityEdit
from Edit.TestMarketEdit import TestMarketEdit
from Edit.TestOrgGroupEdit import TestOrgGroupEdit
from Edit.TestPolicyEdit import TestPolicyEdit
from Edit.TestProcessEdit import TestProcessEdit
from Edit.TestProductEdit import TestProductEdit
from Edit.TestProgramEdit import TestProgramEdit
from Edit.TestProjectEdit import TestProjectEdit
from Edit.TestRegulationEdit import TestRegulationEdit
from Edit.TestSystemEdit import TestSystemEdit
from Edit.TestObjectiveEdit import TestObjectiveEdit
from Mapping.TestProgramMapLHN import TestProgramMapLHN
from Mapping.TestProgramMapWidget import TestProgramMapWidget
from Mapping.TestContractMapLHN import TestContractMapLHN
from Mapping.TestContractMapWidget import TestContractMapWidget
from Mapping.TestPolicyMapLHN import TestPolicyMapLHN
from Mapping.TestPolicyMapWidget import TestPolicyMapWidget
from Mapping.TestRegulationMapLHN import TestRegulationMapLHN
from Mapping.TestRegulationMapWidget import TestRegulationMapWidget
from Mapping.TestSystemsMapLHN import TestSystemsMapLHN
from Mapping.TestProcessMapLHN import TestProcessMapLHN
from Mapping.TestDataAssetMapLHN import TestDataAssetMapLHN
from Mapping.TestProductMapLHN import TestProductMapLHN
from Mapping.TestProjectMapLHN import TestProjectMapLHN
from Mapping.TestFacilityMapLHN import TestFacilityMapLHN
from Mapping.TestMarketMapLHN import TestMarketMapLHN
from Mapping.TestOrgGroupMapLHN import TestOrgGroupMapLHN
from Mapping.TestSystemMapWidget import TestSystemMapWidget
from Mapping.TestProcessMapWidget import TestProcessMapWidget
from Mapping.TestDataAssetMapWidget import TestDataAssetMapWidget
from Mapping.TestProductMapWidget import TestProductMapWidget
from Mapping.TestProjectMapWidget import TestProjectMapWidget
from Mapping.TestFacilityMapWidget import TestFacilityMapWidget
from Mapping.TestMarketMapWidget import TestMarketMapWidget
from Mapping.TestOrgGroupMapWidget import TestOrgGroupMapWidget
from Mapping.TestControlMapLHN import TestControlMapLHN
from Mapping.TestControlMapWidget import TestControlMapWidget
from Audit.TestProgramAudit import TestProgramAudit
]

