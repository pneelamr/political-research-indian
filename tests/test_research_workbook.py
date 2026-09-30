import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'workflow/indian-political-figure-research/scripts'


def module(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name+'.py'))
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


pipeline = module('research_workbook')
checker = module('check_recalculation')


class ResearchPipelineTests(unittest.TestCase):
    def setUp(self):
        directory = ROOT / 'research/atal-bihari-vajpayee'
        self.data = json.loads((directory/'research.json').read_text())
        self.retrievals = json.loads((directory/'retrievals.json').read_text())

    def test_input_provenance_and_coverage(self):
        self.assertTrue(pipeline.validate_data(self.data, self.retrievals))

    def test_source_presence_cannot_be_promoted_to_support(self):
        c = next(c for c in self.data['claims'] if c['status'] == 'Not reviewed')
        c['status'] = 'Supported'
        with self.assertRaisesRegex(ValueError, 'Unsupported verification'):
            pipeline.validate_data(self.data, self.retrievals)

    def test_changed_claim_invalidates_review(self):
        c = self.data['claims'][0]
        c['statement'] += ' changed'
        with self.assertRaisesRegex(ValueError, 'Stale claim'):
            pipeline.validate_data(self.data, self.retrievals)

    def test_unread_source_cannot_be_support(self):
        self.retrievals[0]['access_status'] = 'Search extract only'
        with self.assertRaisesRegex(ValueError, 'unread source'):
            pipeline.validate_data(self.data, self.retrievals)

    def test_same_origin_mirror_is_not_independent(self):
        c = next(c for c in self.data['claims'] if c['status'] == 'Supported')
        c['requires_independent_corroboration'] = True
        e = next(e for e in self.data['evidence'] if e['id'] == c['evidence_ids'][0]).copy()
        e['id'] = 'TEST'
        self.data['evidence'].append(e)
        c['evidence_ids'].append(e['id'])
        with self.assertRaisesRegex(ValueError, 'Independent corroboration'):
            pipeline.validate_data(self.data, self.retrievals)

    def test_unresolved_contradiction_blocks_supported_status(self):
        c = next(c for c in self.data['claims'] if c['status'] == 'Supported')
        c['contradictions'] = ['Conflicting primary account']
        with self.assertRaisesRegex(ValueError, 'unresolved contradiction'):
            pipeline.validate_data(self.data, self.retrievals)

    def test_unknown_citation_rejected(self):
        self.data['tables']['Overview']['rows'][0]['Source IDs'] = 'S999'
        with self.assertRaisesRegex(ValueError, 'Unknown source'):
            pipeline.validate_data(self.data, self.retrievals)

    def test_blanket_ranges_rejected(self):
        with self.assertRaisesRegex(ValueError, 'blanket ranges'):
            pipeline.source_ids('S01–S83')

    def test_missing_context_item_rejected(self):
        self.data['coverage']['Era'].append('Missing required dimension')
        with self.assertRaisesRegex(ValueError, 'context coverage'):
            pipeline.validate_data(self.data, self.retrievals)

    def test_method_rows_do_not_inflate_usage(self):
        tables, _ = pipeline.make_tables(self.data, self.retrievals)
        self.assertFalse(any(r['Record ID'] in ['V16','V17','V22','V23','V24','V25'] for r in tables['Citations']['rows']))
        self.assertTrue(any('Overview' not in s['Used in'] for s in tables['Sources']['rows']))

    def test_direct_contest_gaps_include_assembly_and_exclude_indirect(self):
        template = self.data['tables']['Elections']['rows'][0]
        self.data['tables']['Elections']['rows'] = [
            {**template, 'Election ID': 'TEST-LS', 'Source IDs': '',
             'House / route': 'Lok Sabha / direct',
             'Candidate votes': None, 'Vote share': None},
            {**template, 'Election ID': 'TEST-AS', 'Source IDs': '',
             'House / route': 'Assembly / direct',
             'Candidate votes': 100, 'Vote share': None},
            {**template, 'Election ID': 'TEST-RS', 'Source IDs': '',
             'House / route': 'Rajya Sabha / indirect',
             'Candidate votes': None, 'Vote share': None},
        ]
        _, metrics = pipeline.make_tables(self.data, self.retrievals)
        self.assertEqual(dict(metrics)['Direct contests missing candidate votes'], 1)
        self.assertEqual(dict(metrics)['Direct contests missing vote share'], 2)

    def test_build_is_reorderable_and_does_not_fake_engine_pass(self):
        self.data['subject'] = 'Independent fixture title'
        self.data['tables']['Elections']['rows'].reverse()
        with tempfile.TemporaryDirectory() as temp:
            output, report = Path(temp)/'profile.xlsx', Path(temp)/'qa.json'
            result = pipeline.build(self.data, self.retrievals, output, report)
            wb = load_workbook(output)
            self.assertIn('Independent fixture title', wb['Overview']['A1'].value)
            self.assertEqual(result['checks']['application_recalculation'], 'NOT RUN')
            self.assertEqual(result['checks']['visual_inspection'], 'NOT RUN')
            with self.assertRaisesRegex(ValueError, 'Engine result mismatch'):
                checker.compare(output, result['formula_checks'])
            self.assertEqual(wb['Elections']['A6'].value, 'EL20')
            self.assertEqual(wb['Overview'].column_dimensions['G'].hidden, True)


if __name__ == '__main__':
    unittest.main()
