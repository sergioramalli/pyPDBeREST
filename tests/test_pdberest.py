#!/local/bin/python
# -*- coding: utf-8 -*-

"""
Created on 10/06/2015

"""

import sys
import unittest
import logging

from pdbe import pyPDBeREST
from pdbe import config
from pdbe import exceptions


class TestPDBeREST(unittest.TestCase):
    """Test the PDBe REST functionality."""

    def setUp(self):
        """Initialize the framework for testing."""

        self.p = pyPDBeREST()
        self.pdb = self.p.PDB

    def tearDown(self):
        """Remove testing framework."""

        self.p = None
        self.pdb = None

    def test_loading_config_values_pyPDBeREST(self):
        """
        Testing whether we can access values defined in the config.
        """

        self.assertIsInstance(config.api_endpoints, dict)
        self.assertIsInstance(config.default_url, str)
        self.assertIsInstance(config.http_status_codes, dict)
        self.assertIsInstance(config.user_agent, dict)
        self.assertIsInstance(config.content_type, dict)

    def test_asserting_config_values_pyPDBeREST(self):
        """
        Testing whether we can access values defined in the config.
        """

        self.assertIn('PDB', config.api_endpoints)
        self.assertIn('getSummary', config.api_endpoints['PDB'])
        self.assertIn('method', config.api_endpoints['PDB']['getSummary'])
        self.assertEqual(config.api_endpoints['PDB']['getSummary']['method'],
                         ['GET', 'POST'])

    def test_loading_custom_exceptions_pyPDBeREST(self):
        """
        Testing loading custom exceptions.
        """

        self.assertIsInstance(exceptions.RestError, object)
        self.assertIsInstance(exceptions.RestRateLimitError, object)
        self.assertIsInstance(exceptions.RestServiceUnavailable, object)
        self.assertIsInstance(exceptions.RestPostNotSupported, object)

    def test_loading_module_pyPDBeREST(self):
        """
        Testing whether we could load the module.
        """

        self.assertIsInstance(self.p, object)

    def test_subclass_generation_pyPDBeREST(self):
        """
        Testing whether we successfully generate the subclass as
        based on the naming defined in the config dictionaries.
        """

        self.assertIn('PDB', self.p.__dict__)
        self.assertIn('COMPOUNDS', self.p.__dict__)
        self.assertNotIn('TEST', self.p.__dict__)

    def test_validity_default_values_pyPDBeREST(self):
        """
        Testing whether defined values are still valid
        """

        self.assertEqual(self.p.reqs_per_sec, 15)
        self.assertEqual(self.p.method, 'GET')
        self.assertEqual(self.p.pretty_json, True)

    def test_updating_default_values_pyPDBeREST(self):
        """
        Testing whether defined values are still valid
        """

        # updating session values
        # limited to some attributes: base_url, method and pretty_json
        self.p = pyPDBeREST(method='POST')
        self.assertEqual(self.p.method, 'POST')
        self.p = pyPDBeREST(pretty_json=False)
        self.assertEqual(self.p.pretty_json, False)
        self.p = pyPDBeREST(base_url='http://some.address.com/')
        self.assertEqual(self.p.base_url, 'http://some.address.com/')

        # or simply setting class attributes
        self.p.reqs_per_sec = 30
        self.assertEqual(self.p.reqs_per_sec, 30)

    def test_outputting_available_endpoints_pyPDBeREST(self):
        """
        Testing whether the endpoint methods are available.
        """

        # endpoints() is based on the values stored in self.values
        self.assertIsInstance(self.p.values, list)
        self.assertIsInstance(self.pdb.values, list)

        self.assertIn('PDB', self.p.values)
        self.assertIn('COMPOUNDS', self.p.values)
        self.assertIn('getSummary', self.pdb.values)
        self.assertIn('getLigands', self.pdb.values)

        # prints out the available endpoints
        self.assertIsInstance(self.p.endpoints(), object)
        self.assertIsInstance(self.pdb.endpoints(), object)

    def test_available_endpoints_pyPDBeREST(self):
        """
        Testing whether some endpoints are available as methods.
        """

        self.assertIsInstance(self.p.PDB.getSummary, object)
        self.assertIsInstance(self.p.PDB.getLigands, object)
        self.assertIsInstance(self.pdb.getSummary, object)
        self.assertIsInstance(self.pdb.getLigands, object)

    def test_other_attributes_for_endpoints_pyPDBeREST(self):
        """
        Testing whether some endpoints have additional attributes.
        """

        self.assertIsInstance(self.p.PDB.getSummary.var, dict)
        self.assertIsInstance(self.p.PDB.getSummary.url, str)
        self.assertEqual(self.p.PDB.getSummary.url, 'api/pdb/entry/summary/{{pdbid}}')
        self.assertIsInstance(self.p.PDB.getSummary.doc, str)
        self.assertIn('This call provides a summary of properties of a PDB', self.p.PDB.getSummary.doc)
        self.assertIsInstance(self.p.PDB.getSummary.method, list)
        self.assertEqual(self.p.PDB.getSummary.method, ['GET', 'POST'])
        self.assertIsInstance(self.p.PDB.getSummary.content_type, str)
        self.assertEqual(self.p.PDB.getSummary.content_type, 'application/json')

    def test_wrong_method_endpoint_pyPDBeREST(self):
        """
        Testing the behaviour of calling an unavailable method.
        """

        with self.assertRaises(AttributeError):
            self.p.PDB.wrongMethod()

        with self.assertRaises(AttributeError):
            self.TEST.unavailableMethod()

    def test_various_example_requests_pyPDBeREST(self):
        """
        Testing several valid requests to the PDBe REST API.
        Testing both 'GET' and 'POST' requests.

        Note: Since the output can vary over time, I am not checking
        if the results are valid.
        """

        msg = "===Calling all the available endpoints...===\n" \
              "** This will fail if the service is down! **"
        print(msg)

        # PDB
        self.assertTrue(self.p.PDB.getReleaseStatus(pdbid='2pah'))
        self.assertTrue(self.p.PDB.getSummary(pdbid='2pah'))
        self.assertTrue(self.p.PDB.getBindingSites(pdbid='2pah'))
        self.assertTrue(self.p.PDB.getObservedRanges(pdbid='2pah'))
        self.assertTrue(self.p.PDB.getRelatedPublications(pdbid='2pah'))
        self.assertTrue(self.p.PDB.getResidueListingChain(pdbid='2pah', chainid='A'))
        # needs a NMR structure
        self.assertTrue(self.p.PDB.getNmrResources(pdbid='2k8v'))
        self.assertTrue(self.p.PDB.getExperiments(pdbid='2pah'))
        self.assertTrue(self.p.PDB.getVariousUrls(pdbid='2pah'))
        # needs a pdbid with DNA or RNA
        self.assertTrue(self.p.PDB.getModifiedResidues(pdbid='4v5j'))
        self.assertTrue(self.p.PDB.getResidueListing(pdbid='2pah'))
        self.assertTrue(self.p.PDB.getExperiments(pdbid='2pah'))
        self.assertTrue(self.p.PDB.getPublications(pdbid='2pah'))
        # needs a structure with mutated residues
        self.assertTrue(self.p.PDB.getMutatedResidues(pdbid='1bgj'))
        self.assertTrue(self.p.PDB.getMolecules(pdbid='2pah'))
        # post method
        self.assertTrue(self.p.PDB.getSummary(pdbid='2pah, 1cbs', method='POST'))

        # COMPOUNDS
        self.assertTrue(self.p.COMPOUNDS.getBounds(compid='ATP'))
        self.assertTrue(self.p.COMPOUNDS.getAtoms(compid='ATP'))
        self.assertTrue(self.p.COMPOUNDS.getSummary(compid='ATP'))
        self.assertTrue(self.p.COMPOUNDS.getInPdbs(compid='ATP'))
        # post method
        self.assertTrue(self.p.COMPOUNDS.getSummary(compid='ATP, HEM', method='POST'))

        # EMDB
        self.assertTrue(self.p.EMDB.getInfo(property='summary', emdbid='EMD-1200'))

        # SIFTS
        self.assertTrue(self.p.SIFTS.getMappings(accession='1cbs'))
        self.assertTrue(self.p.SIFTS.getPdbPfam(pdbid='1cbs'))
        self.assertTrue(self.p.SIFTS.getPdbGo(pdbid='1cbs'))
        self.assertTrue(self.p.SIFTS.getPdbInterpro(pdbid='1cbs'))
        self.assertTrue(self.p.SIFTS.getPdbUniprot(pdbid='1cbs'))
        self.assertTrue(self.p.SIFTS.getPdbCath(pdbid='1cbs'))
        self.assertTrue(self.p.SIFTS.getPdbEc(pdbid='2pah'))
        self.assertTrue(self.p.SIFTS.getPdbScop(pdbid='1cbs'))
        self.assertTrue(self.p.SIFTS.getSequenceDomains(pdbid='1cbs'))
        self.assertTrue(self.p.SIFTS.getStructuralDomains(pdbid='1cbs'))
        self.assertTrue(self.p.SIFTS.getBestStructures(uniprotid='P29373'))
        self.assertTrue(self.p.SIFTS.getHomologene(pdbid='1cbs', entity='1'))

        # PISA
        self.assertTrue(self.p.PISA.getVersion())
        self.assertTrue(self.p.PISA.getNumberEntries())
        self.assertTrue(self.p.PISA.getPdbsList())
        self.assertTrue(self.p.PISA.getAsisList(pdbid='3gcb'))
        self.assertTrue(self.p.PISA.getAsisDetails(pdbid='3gcb', assemblyid='0'))
        self.assertTrue(self.p.PISA.getAsisSummary(pdbid='3gcb', assemblyid='0'))
        self.assertTrue(self.p.PISA.getAsisComponent(pdbid='3gcb', assemblyid='0',
                                                     assembly_component='energetics'))
        self.assertTrue(self.p.PISA.getAssembly(pdbid='3gcb', assemblyid='0',
                                                set=0, assembly_index=0))
        self.assertTrue(self.p.PISA.getAnalysis(pdbid='3gcb', assemblyid='0'))
        self.assertTrue(self.p.PISA.getAssembliesList(pdbid='3gcb', assemblyid='0'))
        self.assertTrue(self.p.PISA.getAssemblyDetails(pdbid='3gcb', assemblyid='0',
                                                       assembly_index=0))
        self.assertTrue(self.p.PISA.getAssemblyComponent(pdbid='3gcb', assemblyid='0',
                                                         assembly_index=0,
                                                         assembly_component='energetics'))

        self.assertTrue(self.p.PISA.getMonomersList(pdbid='3gcb', assemblyid='0'))
        self.assertTrue(self.p.PISA.getMonomerDetails(pdbid='3gcb', assemblyid='0',
                                                      monomer_index=1))
        self.assertTrue(self.p.PISA.getMonomerComponent(pdbid='3gcb', assemblyid='0',
                                                        monomer_index=1,
                                                        monomer_component='energetics'))

        self.assertTrue(self.p.PISA.getInterfaces(pdbid='3gcb', assemblyid='0'))
        self.assertTrue(self.p.PISA.getNumberInterfaces(pdbid='3gcb', assemblyid='0'))
        self.assertTrue(self.p.PISA.getInterfacesList(pdbid='3gcb', assemblyid='0'))
        self.assertTrue(self.p.PISA.getInterfaceDetails(pdbid='3gcb', assemblyid='0',
                                                        interface_index=1))
        self.assertTrue(self.p.PISA.getInterfaceComponent(pdbid='3gcb', assemblyid='0',
                                                          interface_index=1,
                                                          interface_component='energetics'))

        # SSM
        self.assertTrue(self.p.SSM.getVersion())
        self.assertTrue(self.p.SSM.getMatchStandard(pdbid='3gcb'))
        self.assertTrue(self.p.SSM.getNumberMatches(pdbid='3gcb'))
        self.assertTrue(self.p.SSM.getMatchSummary(pdbid='3gcb'))
        self.assertTrue(self.p.SSM.getMatchDetail(pdbid='3gcb', ssm_index=1))

        # VALIDATION
        self.assertTrue(self.p.VALIDATION.getGlobalRelativePercentiles(pdbid='1cbs'))
        self.assertTrue(self.p.VALIDATION.getGlobalAbsolutePercentilesSummary(pdbid='1cbs'))
        self.assertTrue(self.p.VALIDATION.getGlobalPercentilesDetails(pdbid='1cbs'))
        self.assertTrue(self.p.VALIDATION.getDiffractionRefinementDescriptors(pdbid='1cbs'))
        self.assertTrue(self.p.VALIDATION.getRamachandranSidechainOutliers(pdbid='1cbs'))
        self.assertTrue(self.p.VALIDATION.getBackboneSidechainQuality(pdbid='1cbs'))
        self.assertTrue(self.p.VALIDATION.getSuitePuckerRnaOutliers(pdbid='1cbs'))
        self.assertTrue(self.p.VALIDATION.getOutlierTypesResidues(pdbid='1cbs'))
        self.assertTrue(self.p.VALIDATION.getVanDerWaalOverlaps(pdbid='1cbs'))
        self.assertTrue(self.p.VALIDATION.getGeometryOutliers(pdbid='1cbs'))
        self.assertTrue(self.p.VALIDATION.getAllOutliersUnitId(pdbid='1cbs'))
        # post method
        self.assertTrue(self.p.VALIDATION.getAllOutliersUnitId(pdbid='2pah, 1cbs', method='POST'))

        # TOPOLOGY
        self.assertTrue(self.p.TOPOLOGY.getTopology(pdbid='1csb'))
        self.assertTrue(self.p.TOPOLOGY.getTopologyPerChain(pdbid='1csb', chainid='A'))

        # SEARCH
        self.assertTrue(self.p.SEARCH.getSearch(query='q=pfam_name:Lipocalin&wt=json'))

    def test_wrong_parameter_for_endpoint_pyPDBeREST(self):
        """
        Testing when the user provides a wrong param for a endpoint.
        """

        with self.assertRaises(Exception):
            self.pdb.getSummary(wrong_param='2pah')

    def test_wrongly_formatted_url_request_pyPDBeREST(self):
        """
        Testing when everything is correct but the input values.
        """

        with self.assertRaises(exceptions.RestError):
            self.pdb.getSummary(pdbid='invalid_id')

    def test_wrong_request_method_pyPDBeREST(self):
        """
        Testing when the method provided is not 'GET' or 'POST'.
        """

        with self.assertRaises(NotImplementedError):
            self.pdb.getSummary(pdbid='2pah', method='PULL')

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("pyPDBeREST").setLevel(logging.DEBUG)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPDBeREST)
    unittest.TextTestRunner(verbosity=2, buffer=False).run(suite)
