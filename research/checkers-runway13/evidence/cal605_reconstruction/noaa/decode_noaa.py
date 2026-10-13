#!/usr/bin/env python3
"""Decode retained NOAA ISD 1993 record, never overwrite the original archive.

Python stdlib only. Format: retained isd-format-document.pdf, control/mandatory
pp. 5–12; ADD identifiers AA pp.13, AG pp.18–19, ED p.58, GA pp.59–61,
MA pp.95–96, MW pp.103–107, OC p.111. Unsupported ADD IDs fail closed.
"""
import collections
import csv
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / 'weather_feasibility_2026-10-13/NOAA_450070-99999-1993.gz'
EXPECTED_SOURCE_SHA256 = '617c7db4f19c3aaacef91ae8a688c0aab196cdfc7ddfba72857c8e70056d66e0'
EXPECTED_METADATA = {'usaf': '450070', 'wban': '99999', 'latitude_raw': '+22333',
                     'longitude_raw': '+114183', 'elevation_raw': '+0024', 'call_sign_raw': 'VHHH '}
STRICT_QUALITY = {'1', '5'}
MPS_PER_KNOT = 1852 / 3600
GROUP_LENGTHS = {'AG1': 7, 'ED1': 11, 'MA1': 15, 'OC1': 8,
                 **{f'GA{i}': 16 for i in range(1, 7)},
                 **{f'MW{i}': 6 for i in range(1, 8)},
                 **{f'AA{i}': 11 for i in range(1, 5)}}
# (zero-based start, end, missing token, scale divisor, quality index)
FIELDS = {
    'wind_direction_deg': (60, 63, '999', 1, 63),
    'wind_speed_mps': (65, 69, '9999', 10, 69),
    'ceiling_m': (70, 75, '99999', 1, 75),
    'visibility_m': (78, 84, '999999', 1, 84),
    'temperature_c': (87, 92, '+9999', 10, 92),
    'dewpoint_c': (93, 98, '+9999', 10, 98),
    'sea_level_pressure_hpa': (99, 104, '99999', 10, 104),
}


def measurement(raw, missing_token, divisor, quality):
    missing = raw is None or raw == missing_token
    value = None if missing else int(raw) / divisor
    return {'raw': raw, 'value': value, 'missing': missing,
            'quality': quality, 'strict_qc_accepted': not missing and quality in STRICT_QUALITY}


def add_measurement(row, name, raw, sentinel, scale, quality):
    m = measurement(raw, sentinel, scale, quality)
    row[name] = m.pop('value')
    for k, v in m.items():
        row[name + '_' + k] = v


def parse_additional(tail):
    groups = {}
    if not tail.startswith('ADD'):
        if tail and not tail.startswith(('REM', 'EQD')):
            raise ValueError('unknown variable-section marker')
        return groups, tail
    pos = 3
    while pos < len(tail) and tail[pos:pos+3] not in ('REM', 'EQD'):
        ident = tail[pos:pos+3]
        if ident not in GROUP_LENGTHS:
            raise ValueError('unsupported ADD group: ' + ident)
        length = GROUP_LENGTHS[ident]
        if pos + length > len(tail) or ident in groups:
            raise ValueError('truncated or duplicated ADD group: ' + ident)
        groups[ident] = tail[pos:pos+length]
        pos += length
    return groups, tail[pos:]


def decode(line, line_number):
    if len(line) < 105 or len(line) != 105 + int(line[:4]):
        raise ValueError('record length mismatch at line ' + str(line_number))
    timestamp = dt.datetime.strptime(line[15:27], '%Y%m%d%H%M').replace(tzinfo=dt.timezone.utc)
    row = {'source_line': line_number, 'datetime_utc': timestamp.isoformat().replace('+00:00', 'Z'),
           'date_utc': timestamp.date().isoformat(), 'time_utc': timestamp.strftime('%H:%M'),
           'usaf': line[4:10], 'wban': line[10:15], 'source_flag': line[27],
           'latitude_raw': line[28:34], 'longitude_raw': line[34:41],
           'elevation_raw': line[46:51], 'call_sign_raw': line[51:56],
           'report_type': line[41:46], 'qc_process': line[56:60],
           'wind_type': line[64], 'wind_direction_variable': line[64] == 'V',
           'visibility_variability': line[85], 'visibility_variability_quality': line[86]}
    for name, (start, end, sentinel, scale, qi) in FIELDS.items():
        add_measurement(row, name, line[start:end], sentinel, scale, line[qi])
    groups, remarks = parse_additional(line[105:])
    oc = groups.get('OC1')
    add_measurement(row, 'gust_mps', oc[3:7] if oc else None, '9999', 10, oc[7] if oc else None)
    row['gust_group_present'] = oc is not None
    ma = groups.get('MA1')
    add_measurement(row, 'altimeter_setting_hpa', ma[3:8] if ma else None, '99999', 10, ma[8] if ma else None)
    add_measurement(row, 'station_pressure_hpa', ma[9:14] if ma else None, '99999', 10, ma[14] if ma else None)
    for name in ('wind_speed', 'gust'):
        v = row[name + '_mps']
        row[name + '_kt'] = v / MPS_PER_KNOT if v is not None else None
    row['partial_weather_row'] = all(row[k + '_missing'] for k in ('temperature_c', 'visibility_m'))
    row['additional_groups_json'] = json.dumps(groups, sort_keys=True, separators=(',', ':'))
    row['remarks_and_quality_raw'] = remarks
    row['raw_record'] = line
    return row


def write_csv(name, rows):
    with (HERE / name).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def rank(values, threshold):
    n = len(values)
    below = sum(v < threshold for v in values)
    equal = sum(v == threshold for v in values)
    return {'n': n, 'threshold_mps': threshold, 'below': below, 'equal': equal,
            'above': n - below - equal, 'percent_below': below/n*100,
            'percent_at_or_below': (below+equal)/n*100,
            'meaning': 'empirical record rank in declared observed subset; no probability interpretation'}


def load_pinned_source(source):
    # Decode the same bytes that were hashed: no reopen race or hash-only logging.
    archive = source.read_bytes()
    actual_hash = hashlib.sha256(archive).hexdigest()
    if actual_hash != EXPECTED_SOURCE_SHA256:
        raise ValueError('retained source SHA256 mismatch; refusing substituted or changed archive')
    return gzip.decompress(archive).decode('ascii').splitlines(), actual_hash


def validate_source_identity(rows):
    if not rows:
        raise ValueError('retained source has no rows')
    for row in rows:
        for key, expected in EXPECTED_METADATA.items():
            if row[key] != expected:
                raise ValueError(f"retained source metadata mismatch: {key}, line {row['source_line']}")
        if row['date_utc'][:4] != '1993':
            raise ValueError(f"retained source year mismatch, line {row['source_line']}")


def main():
    lines, source_hash = load_pinned_source(SOURCE)
    rows = [decode(line, i) for i, line in enumerate(lines, 1)]
    # Check every row before opening any derived output. Never silently filter a
    # substituted station or year into the historical ranking denominator.
    validate_source_identity(rows)
    event_day = [r for r in rows if r['date_utc'] == '1993-11-04']
    write_csv('observations_1993.csv', rows)
    write_csv('observations_1993-11-04.csv', event_day)
    timestamps = collections.Counter(r['datetime_utc'] for r in rows)
    regular = [r for r in rows if r['report_type'] == 'FM-15' and r['source_flag'] == '4'
               and r['time_utc'].endswith(':00') and r['wind_type'] == 'N'
               and r['wind_speed_mps_strict_qc_accepted'] and not r['partial_weather_row']]
    event = [r for r in event_day if r['time_utc'] in ('03:00', '04:00')]
    comparisons = []
    for r in event:
        assert r in regular
        same_clock = [v for v in regular if v['time_utc'] == r['time_utc']]
        comparisons.append({'datetime_utc': r['datetime_utc'], 'noaa_direction_deg': r['wind_direction_deg'],
                            'noaa_speed_kt': r['wind_speed_kt'], 'noaa_gust_kt': r['gust_kt'],
                            'cad_appendix5_direction_deg': 70, 'cad_appendix5_mean_speed_kt': 21,
                            'difference_speed_kt': r['wind_speed_kt'] - 21,
                            'scope': 'consistency only; same reporting stream may feed both sources; clocks/instruments not independently established',
                            'all_year_normal_routine_rank': rank([v['wind_speed_mps'] for v in regular], r['wind_speed_mps']),
                            'same_clock_hour_normal_routine_rank': rank([v['wind_speed_mps'] for v in same_clock], r['wind_speed_mps'])})
    start = dt.datetime(1993, 1, 1, tzinfo=dt.timezone.utc)
    expected = {(start + dt.timedelta(hours=h)).isoformat().replace('+00:00','Z') for h in range(8760)}
    quality = {}
    for name in list(FIELDS) + ['gust_mps', 'altimeter_setting_hpa', 'station_pressure_hpa']:
        quality[name] = {'missing': sum(r[name+'_missing'] for r in rows),
                         'strict_qc_accepted': sum(r[name+'_strict_qc_accepted'] for r in rows),
                         'quality_codes': dict(collections.Counter(str(r[name+'_quality']) for r in rows))}
    verification = {
        'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'source_path': str(SOURCE), 'source_sha256': source_hash,
        'source_sha256_expected': EXPECTED_SOURCE_SHA256,
        'source_identity_verified_before_output': True,
        'source_identity_rule': {'year': 1993, **EXPECTED_METADATA},
        'documentation_url': 'https://www.ncei.noaa.gov/pub/data/noaa/isd-format-document.pdf',
        'documentation_sha256': hashlib.sha256((HERE/'isd-format-document.pdf').read_bytes()).hexdigest(),
        'record_count': len(rows), 'nov4_count': len(event_day),
        'date_min': min(r['datetime_utc'] for r in rows), 'date_max': max(r['datetime_utc'] for r in rows),
        'observed_dates_count': len({r['date_utc'] for r in rows}),
        'report_types': dict(collections.Counter(r['report_type'] for r in rows)),
        'source_flags': dict(collections.Counter(r['source_flag'] for r in rows)),
        'wind_types': dict(collections.Counter(r['wind_type'] for r in rows)),
        'duplicate_raw_records': len(lines)-len(set(lines)),
        'duplicate_timestamp_extra_rows': sum(n-1 for n in timestamps.values()),
        'duplicate_timestamps': {k:v for k,v in timestamps.items() if v>1},
        'missing_calendar_hour_count': len(expected - set(timestamps)),
        'off_hour_records': sum(not r['time_utc'].endswith(':00') for r in rows),
        'metadata_tuples': sorted(set(tuple(r[k] for k in ('usaf','wban','latitude_raw','longitude_raw','elevation_raw','call_sign_raw')) for r in rows)),
        'quality_rule': 'Strict analysis acceptance requires present numeric value and quality 1 or 5 (all QC checks passed). Values with other codes retained but not accepted; no imputation. This is flag filtering, not independent meteorological or station-history validation.',
        'field_qc': quality, 'gust_group_count': sum(r['gust_group_present'] for r in rows),
        'partial_weather_row_count': sum(r['partial_weather_row'] for r in rows),
        'nov4_partial_weather_rows': [r['datetime_utc'] for r in event_day if r['partial_weather_row']],
        'rank_subset_rule': 'FM-15, source flag 4, exact hour, normal wind type N, strict speed QC, non-partial weather row. All 1993; observed records only; missing hours are not imputed. Also report same UTC hour subset.',
        'rank_subset_count': len(regular), 'event_comparisons': comparisons,
        'limitations': ['station/anemometer history not reconciled', 'NOAA reported surface gusts are not aircraft gust encounters',
                        'gust absence is missing not zero', 'remarks are retained, never decoded as current observations',
                        'hourly observations do not reconstruct 03:35 aircraft-local wind',
                        'rank is descriptive, not accident probability, return period, or population quantile with a CI'],
    }
    for name in ('observations_1993.csv', 'observations_1993-11-04.csv'):
        verification.setdefault('output_sha256', {})[name] = hashlib.sha256((HERE/name).read_bytes()).hexdigest()
    (HERE/'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
    print(json.dumps({k: verification[k] for k in ('record_count','nov4_count','rank_subset_count','event_comparisons')}, indent=2))


if __name__ == '__main__':
    main()
