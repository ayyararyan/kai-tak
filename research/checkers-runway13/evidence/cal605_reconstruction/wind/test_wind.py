import unittest
from reconstruct_wind import build, signed_angle

class WindChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows,cls.summary=build()
        cls.i={(r['wind_clock_time'],r['sensor'],r['field']):r for r in cls.rows}

    def test_actual_printed_coverage(self):
        self.assertEqual(len(self.rows),225)
        self.assertEqual(len(self.i),225)
        self.assertEqual(len({r['wind_clock_time'] for r in self.rows}),15)
        self.assertEqual({r['sensor'] for r in self.rows},{'SE','NW','MID','LYM','YYC'})
        self.assertTrue(all(0 <= r['direction_deg_printed'] <= 360 and 0 <= r['speed_kt_printed'] for r in self.rows))

    def test_event_selected_gap_not_filled(self):
        self.assertNotIn('03:36:00',self.summary['times'])
        self.assertIn(120,self.summary['consecutive_gaps_seconds'])
        self.assertEqual(sum(self.summary['consecutive_gaps_seconds']),600)

    def test_source_anomalies_retained(self):
        r=self.i['03:35:30','LYM','A']
        self.assertEqual(r['direction_deg_printed'],360)
        self.assertIn('not silently',r['reading_note'])
        r=self.i['03:38:00','NW','C']
        self.assertEqual(r['speed_kt_printed'],17)
        self.assertIn('19',r['reading_note'])

    def test_circular_direction(self):
        self.assertEqual(signed_angle(360,60),-60)
        self.assertEqual(signed_angle(350,10),-20)
        self.assertEqual(signed_angle(10,350),20)

    def test_visually_verified_key_findings(self):
        self.assertEqual(self.i['03:35:30','NW','A']['speed_kt_printed'],37)
        self.assertEqual(self.i['03:35:30','NW','C']['speed_kt_printed'],19)
        self.assertEqual(self.summary['max_across_sensor_speed_range']['A']['speed_range_kt'],25)
        self.assertEqual(self.summary['max_across_sensor_speed_range']['B']['speed_range_kt'],21)
        self.assertEqual(self.summary['max_across_sensor_speed_range']['C']['speed_range_kt'],16)

    def test_page_transition_and_distinct_clock(self):
        self.assertEqual(self.i['03:38:00','SE','A']['pdf_page_1_based'],138)
        self.assertEqual(self.i['03:38:30','SE','A']['pdf_page_1_based'],139)
        self.assertTrue(all('wind_clock_time' in r and 'flight_time' not in r for r in self.rows))


class MissingWindChecks(unittest.TestCase):
    def fixture(self, mode):
        from pathlib import Path
        import tempfile
        from reconstruct_wind import ROOT
        temporary=tempfile.TemporaryDirectory()
        root=Path(temporary.name)
        source=(ROOT/'manual_readings.txt').read_text()
        if mode=='speed': source=source.replace('080/20','080/?',1)
        elif mode=='direction': source=source.replace('080/20','?/20',1)
        elif mode=='sparse_allmissing':
            source='03:30:00 '+' '.join(['?/?,?/?,?/?']*5)+'\n'
        (root/'manual_readings.txt').write_text(source)
        extrema=(ROOT/'manual_extrema.txt').read_text()
        if mode=='sparse_allmissing': extrema='03:30:00 ?/? ?/?\n'
        (root/'manual_extrema.txt').write_text(extrema)
        return temporary, root

    def test_missing_speed_propagates_without_losing_direction(self):
        import csv
        temporary,root=self.fixture('speed')
        with temporary:
            rows,summary=build(root)
            self.assertIsNone(rows[0]['speed_kt_printed'])
            self.assertEqual(summary['counts']['ambiguous_abc_numeric_cells'],1)
            differences=list(csv.DictReader((root/'within_sensor_differences.csv').read_text().splitlines()))
            self.assertEqual(differences[0]['speed_difference_kt'],'')
            self.assertEqual(differences[0]['direction_circular_difference_deg'],'0')
            cross=list(csv.DictReader((root/'across_sensor_variability.csv').read_text().splitlines()))
            self.assertEqual(cross[0]['speed_range_kt'],'')
            self.assertEqual(cross[0]['valid_speed_sensor_count'],'4')

    def test_missing_direction_preserves_speed(self):
        import csv
        temporary,root=self.fixture('direction')
        with temporary:
            rows,summary=build(root)
            self.assertIsNone(rows[0]['direction_deg_printed'])
            self.assertEqual(summary['counts']['ambiguous_abc_numeric_cells'],1)
            differences=list(csv.DictReader((root/'within_sensor_differences.csv').read_text().splitlines()))
            self.assertEqual(differences[0]['speed_difference_kt'],'-2')
            self.assertEqual(differences[0]['direction_circular_difference_deg'],'')

    def test_sparse_allmissing_no_zero_or_empty_extrema_error(self):
        temporary,root=self.fixture('sparse_allmissing')
        with temporary:
            rows,summary=build(root)
            self.assertEqual(len(rows),15)
            self.assertEqual(summary['counts']['ambiguous_abc_numeric_cells'],30)
            self.assertIsNone(summary['max_present_speed_record'])
            self.assertTrue(all(v is None for v in summary['max_across_sensor_speed_range'].values()))
            for fields in summary['within_sensor_speed_differences'].values():
                for value in fields.values():
                    self.assertIsNone(value['min_kt']); self.assertIsNone(value['max_kt'])
                    self.assertEqual(value['valid_pair_count'],0)
            self.assertIsNone(summary['printed_rolling_extrema_summary']['SE']['maximum_kt'])

    def test_bad_input_does_not_replace_outputs(self):
        temporary,root=self.fixture('speed')
        with temporary:
            build(root)
            before={p.name:p.read_bytes() for p in root.iterdir() if p.suffix in ('.csv','.json')}
            with (root/'manual_extrema.txt').open('a') as f: f.write('03:40:00 malformed malformed\n')
            with self.assertRaises(ValueError): build(root)
            self.assertEqual(before,{p.name:p.read_bytes() for p in root.iterdir() if p.suffix in ('.csv','.json')})

    def test_plot_missing_speed_direction_and_allmissing(self):
        from plot_wind import plot
        for mode in ('speed','direction','sparse_allmissing'):
            temporary,root=self.fixture(mode)
            with temporary:
                build(root); plot(root)
                self.assertGreater((root/'wind_windows.png').stat().st_size,1000)

if __name__=='__main__':
    unittest.main()
