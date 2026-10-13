import gzip
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import decode_noaa
from decode_noaa import SOURCE, decode, measurement, parse_additional, load_pinned_source, validate_source_identity


class DecoderTests(unittest.TestCase):
    def test_pinned_source_accepts_original(self):
        lines, digest = load_pinned_source(SOURCE)
        self.assertEqual(len(lines), 8549)
        self.assertEqual(digest, decode_noaa.EXPECTED_SOURCE_SHA256)

    def test_tampered_source_refused_without_output_mutation(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = directory / 'substituted.gz'
            source.write_bytes(SOURCE.read_bytes() + b'changed')
            old_output = directory / 'observations_1993.csv'
            old_output.write_text('preserve me')
            with patch.object(decode_noaa, 'SOURCE', source), patch.object(decode_noaa, 'HERE', directory):
                with self.assertRaisesRegex(ValueError, 'SHA256 mismatch'):
                    decode_noaa.main()
            self.assertEqual(old_output.read_text(), 'preserve me')
            self.assertEqual({p.name for p in directory.iterdir()}, {'substituted.gz', 'observations_1993.csv'})

    def test_every_row_metadata_and_year_checked(self):
        lines, _ = load_pinned_source(SOURCE)
        good = decode(lines[0], 1)
        for key, bad in {'usaf':'450080', 'wban':'00001', 'latitude_raw':'+22309',
                         'longitude_raw':'+113915', 'elevation_raw':'+0025',
                         'call_sign_raw':'VHHX ', 'date_utc':'1994-01-01'}.items():
            with self.subTest(key=key):
                altered = {**good, key: bad, 'source_line': 2}
                with self.assertRaisesRegex(ValueError, 'mismatch'):
                    validate_source_identity([good, altered])
        validate_source_identity([good])

    def test_metadata_failure_precedes_output_mutation(self):
        lines, digest = load_pinned_source(SOURCE)
        # Isolate defence-in-depth metadata validation after the hash gate.
        changed_line = lines[0][:4] + '450080' + lines[0][10:]
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            output = directory / 'observations_1993.csv'
            output.write_text('preserve me')
            with patch.object(decode_noaa, 'load_pinned_source', return_value=([changed_line], digest)), patch.object(decode_noaa, 'HERE', directory):
                with self.assertRaisesRegex(ValueError, 'metadata mismatch'):
                    decode_noaa.main()
            self.assertEqual(output.read_text(), 'preserve me')
            self.assertEqual(len(list(directory.iterdir())), 1)

    def test_empty_source_identity_refused(self):
        with self.assertRaisesRegex(ValueError, 'no rows'):
            validate_source_identity([])

    def test_missing_sentinels_not_numeric_extremes(self):
        for token in ('999', '9999', '+9999', '99999', '999999'):
            m = measurement(token, token, 10, '1')
            self.assertIsNone(m['value'])
            self.assertTrue(m['missing'])
            self.assertFalse(m['strict_qc_accepted'])

    def test_negative_temperature_and_scale(self):
        self.assertEqual(measurement('-0123', '+9999', 10, '1')['value'], -12.3)
        self.assertEqual(measurement('10113', '99999', 10, '1')['value'], 1011.3)

    def test_zero_is_not_missing(self):
        m = measurement('0000', '9999', 10, '1')
        self.assertEqual(m['value'], 0)
        self.assertFalse(m['missing'])
        self.assertTrue(m['strict_qc_accepted'])

    def test_suspect_retained_but_not_accepted(self):
        for quality in ('0', '2', '3', '4', '6', '7', '9', 'M'):
            m = measurement('0108', '9999', 10, quality)
            self.assertEqual(m['value'], 10.8)
            self.assertFalse(m['strict_qc_accepted'])
        self.assertTrue(measurement('0108', '9999', 10, '5')['strict_qc_accepted'])

    def test_gust_not_parsed_from_remarks(self):
        groups, _ = parse_additional('ADDAG11999REMMET008OC101751')
        self.assertNotIn('OC1', groups)
        groups, _ = parse_additional('ADDOC101751REMMET000')
        self.assertEqual(groups['OC1'], 'OC101751')

    def test_unknown_and_truncated_additional_fail(self):
        for text in ('ADDXX100000', 'ADDOC1017'):
            with self.assertRaises(ValueError):
                parse_additional(text)

    def test_actual_event_fields_and_lengths(self):
        with gzip.open(SOURCE, 'rt') as f:
            line = next(l.rstrip('\n') for l in f if l[15:27] == '199311040300')
        row = decode(line, 1)
        self.assertEqual(row['datetime_utc'], '1993-11-04T03:00:00Z')
        self.assertEqual(row['wind_direction_deg'], 70)
        self.assertEqual(row['wind_speed_mps'], 10.8)
        self.assertEqual(row['gust_mps'], 17.5)
        self.assertEqual(row['altimeter_setting_hpa'], 1011.9)
        self.assertEqual(row['temperature_c'], 24)
        self.assertEqual(row['visibility_m'], 6000)
        self.assertIsNone(row['sea_level_pressure_hpa'])
        with self.assertRaises(ValueError):
            decode(line[:-1], 1)


if __name__ == '__main__':
    unittest.main()
