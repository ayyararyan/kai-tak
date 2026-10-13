#!/usr/bin/env python3
"""Reproduce Appendix 7 tables and descriptive checks from manual visual anchors.
No network, fitting, interpolation, UTC alignment, or statistical interval estimation.
"""
from pathlib import Path
import csv, hashlib, json, io, os, tempfile

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[4]
PDF = WORKSPACE / 'data/kai-tak-2026-10-13/sources/CAD_1-95_CAL605_wayback.pdf'
TXT = PDF.with_name('CAD_1-95_CAL605.txt')
SENSORS = ['SE', 'NW', 'MID', 'LYM', 'YYC']
FIELDS = {'A': 'maximum 1-second speed and its associated direction in 5-second period',
          'B': 'preceding 2-minute arithmetic mean speed; mean direction per Attachment II',
          'C': 'preceding 10-minute arithmetic mean speed; mean direction per Attachment II'}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def signed_angle(a, b):
    return None if a is None or b is None else (a - b + 180) % 360 - 180

def difference(a, b):
    return None if a is None or b is None else a - b

def max_record(rows, key):
    valid = [r for r in rows if r[key] is not None]
    return max(valid, key=lambda r: r[key]) if valid else None

def finite_extreme(values, fn):
    valid = [v for v in values if v is not None]
    return fn(valid) if valid else None

def parse_value(raw):
    return None if raw == '?' else int(raw)

def manual_lines(name, root):
    return [line for line in (root/name).read_text().splitlines() if line and not line.startswith('#')]

def commit_outputs(root, tables, documents):
    # Finish derivation AND serialization before replacing any previous output.
    # Stage all bytes first; an I/O failure during final multi-file replacement
    # is not a transactional directory swap, and is not claimed to be one.
    output = {}
    for name, rows in tables.items():
        stream = io.StringIO(newline='')
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
        output[name] = stream.getvalue()
    for name, document in documents.items():
        output[name] = json.dumps(document, indent=2, allow_nan=False) + '\n'
    with tempfile.TemporaryDirectory(prefix='.wind-stage-', dir=root) as tmp:
        for name, contents in output.items():
            (Path(tmp)/name).write_text(contents)
        for name in output:
            os.replace(Path(tmp)/name, root/name)

def build(root=ROOT):
    root = Path(root)
    records, anchors = [], []
    pages = TXT.read_text().split('\f')
    for i, line in enumerate(manual_lines('manual_readings.txt', root)):
        time, *groups = line.split()
        assert len(groups) == 5
        page = 138 if i < 12 else 139
        block = i+1 if i < 12 else i-11
        h,m,s = map(int,time.split(':'))
        second = h*3600+m*60+s-(3*3600+30*60)
        rawblock = pages[page-1].split(time,1)[1].split('\n\n',1)[0].strip()
        anchors.append({'wind_clock_time':time,'pdf_page_1_based':page,
                        'printed_page':f'A7-{page-136}', 'record_block_1_based':block,
                        'manual_normalized_abc_line':line,
                        'machine_text_aid_not_authority':rawblock,
                        'visual_evidence':f'source_pages/wind-{page}.png'})
        for sensor, group in zip(SENSORS, groups):
            pairs=group.split(','); assert len(pairs)==3
            for field, pair in zip(FIELDS, pairs):
                rawdir, rawspeed = pair.split('/')
                direction = parse_value(rawdir)
                speed = parse_value(rawspeed)
                note = ''
                if time == '03:35:30' and sensor=='LYM' and field=='A':
                    note='360 is visually printed; retained as printed, not silently changed to 060. Possible source anomaly remains unresolved.'
                if time == '03:38:00' and sensor=='NW' and field=='C':
                    note='Actual p138 printout reads 17; p137 illustrative example at same clock reads 19. Actual record retained; discrepancy unresolved.'
                records.append({'date':'1993-11-04','wind_clock_time':time,
                  'seconds_since_wind_clock_033000':second,'sensor':sensor,'field':field,
                  'direction_deg_printed':direction,'speed_kt_printed':speed,
                  'pdf_page_1_based':page,'printed_page':f'A7-{page-136}',
                  'record_block_1_based':block,'row_in_block':{'SE':1,'NW':2,'MID':3,'LYM':1,'YYC':2}[sensor],
                  'column_group':'right' if sensor in ['LYM','YYC'] else 'left',
                  'raw_reading':field+pair,'reading_status':'unambiguous_printed_value' if direction is not None and speed is not None else 'ambiguous_null',
                  'reading_note':note})
    extrema=[]
    for i,line in enumerate(manual_lines('manual_extrema.txt', root)):
        time,*groups=line.split()
        for sensor,pair in zip(['SE','NW'],groups):
            low,high=map(parse_value,pair.split('/'))
            extrema.append({'wind_clock_time':time,'sensor':sensor,'field':'E',
              'preceding_10min_min_1sec_speed_kt':low,'preceding_10min_max_1sec_speed_kt':high,
              'pdf_page_1_based':138 if i<12 else 139,'record_block_1_based':i+1 if i<12 else i-11,
              'raw_reading':'E '+pair.replace('/','-')})
    metadata={'source_pdf':str(PDF.relative_to(WORKSPACE)),'source_pdf_sha256':sha(PDF),
      'source_notes_pdf_page_1_based':137,'record_pdf_pages_1_based':[138,139],
      'method':'Human-model visual transcription from Poppler-rendered primary PDF pages, checked against machine text; machine text is not authority.',
      'render_command':'pdftoppm -f 137 -l 139 -scale-to 3000 -png <source.pdf> source_pages/wind',
      'field_semantics':FIELDS,
      'sensor_names':dict(zip(SENSORS,['Southeast','Northwest','Mid-runway','Lei Yue Mun','Yau Yat Chuen'])),
      'time_semantics':'Printout labels UTC. Offset to DFDR/ATC clock not identified here. All time comparisons remain within wind-system clock.',
      'selection_semantics':'Notes say significant windshear activates 30-second printouts, otherwise updated every 10 minutes. Preserve 15 actual printed records, not a complete evenly spaced time series.',
      'direction_semantics':'Degrees as printed, 360 preserved. No true/magnetic conversion or runway-component inference made here.',
      'uncertainty':{'display_resolution_observed':{'speed_kt':1,'direction_degrees':10},
       'rounding_rule':'Unknown; display increments alone do not establish rounding error bounds.',
       'physical_instrument_error':'Unidentified from these pages; not set equal to display precision.',
       'ambiguous_cells':f"Null if unreadable. {sum(r[k] is None for r in records for k in ('direction_deg_printed','speed_kt_printed'))} of {2*len(records)} A/B/C numerical cells are null; source-level anomalies flagged separately.",
       'confidence_intervals':'None estimated. No 95% statistical or physical error bounds claimed.'},
      'not_extracted':['D direction extrema','F crosswind extrema','G trackwind extrema','printed shear flags'],
      'anchors':anchors}
    index={(r['wind_clock_time'],r['sensor'],r['field']):r for r in records}
    times=list(dict.fromkeys(r['wind_clock_time'] for r in records))
    differences=[]
    for time in times:
        for sensor in SENSORS:
            a=index[time,sensor,'A']
            for field in ('B','C'):
                b=index[time,sensor,field]
                differences.append({'wind_clock_time':time,'sensor':sensor,'comparison':'A-'+field,
                  'speed_difference_kt':difference(a['speed_kt_printed'],b['speed_kt_printed']),
                  'direction_circular_difference_deg':signed_angle(a['direction_deg_printed'],b['direction_deg_printed'])})
    cross=[]
    for time in times:
        for field in FIELDS:
            vals=[index[time,sensor,field] for sensor in SENSORS]
            speedvals=[r for r in vals if r['speed_kt_printed'] is not None]
            directionvals=[r for r in vals if r['direction_deg_printed'] is not None]
            lo=min(speedvals,key=lambda x:x['speed_kt_printed']) if speedvals else None
            hi=max(speedvals,key=lambda x:x['speed_kt_printed']) if speedvals else None
            cross.append({'wind_clock_time':time,'field':field,
               'min_speed_kt':lo['speed_kt_printed'] if lo else None,
               'max_speed_kt':hi['speed_kt_printed'] if hi else None,
               'speed_range_kt':hi['speed_kt_printed']-lo['speed_kt_printed'] if len(speedvals)==len(SENSORS) else None,
               'min_sensor':lo['sensor'] if lo else None,'max_sensor':hi['sensor'] if hi else None,
               'max_pairwise_circular_direction_difference_deg':max(abs(signed_angle(a['direction_deg_printed'],b['direction_deg_printed'])) for a in vals for b in vals) if len(directionvals)==len(SENSORS) else None,
               'valid_speed_sensor_count':len(speedvals),'valid_direction_sensor_count':len(directionvals)})
    summary={'classification':'Descriptive diagnostics of printed event-selected records, not population inference.',
      'counts':{'timestamps':len(times),'sensors':len(SENSORS),'direction_speed_pairs':len(records),'printed_E_extrema_pairs':len(extrema),'ambiguous_abc_numeric_cells':sum(r[k] is None for r in records for k in ('direction_deg_printed','speed_kt_printed'))},
      'times':times,'consecutive_gaps_seconds':[records[(i+1)*15]['seconds_since_wind_clock_033000']-records[i*15]['seconds_since_wind_clock_033000'] for i in range(len(times)-1)],
      'within_sensor_speed_differences':{},
      'max_across_sensor_speed_range':{field:max_record([r for r in cross if r['field']==field],'speed_range_kt') for field in FIELDS},
      'max_present_speed_record':max_record([r for r in records if r['field']=='A'],'speed_kt_printed'),
      'printed_rolling_extrema_summary':{sensor:{'minimum_kt':finite_extreme((r['preceding_10min_min_1sec_speed_kt'] for r in extrema if r['sensor']==sensor),min),'maximum_kt':finite_extreme((r['preceding_10min_max_1sec_speed_kt'] for r in extrema if r['sensor']==sensor),max)} for sensor in ['SE','NW']},
      'cautions':['A is 5-second maximum 1-second speed, not an instantaneous or mean wind.', 'B/C rolling means overlap. No independent sample count, standard error, p-value, or CI is inferred.', 'Event-dependent sparse timestamps cannot estimate unbiased time averages or gust frequencies.', 'Ground sensors do not measure flight-path winds or vertical wind. No causal accident inference.', 'No alignment to flight/ATC clock; 360 LYM direction and NW17/19 source discrepancy retained.']}
    for sensor in SENSORS:
        summary['within_sensor_speed_differences'][sensor]={}
        for field in ('B','C'):
            values=[r for r in differences if r['sensor']==sensor and r['comparison']=='A-'+field]
            summary['within_sensor_speed_differences'][sensor]['A-'+field]={'min_kt':finite_extreme((r['speed_difference_kt'] for r in values),min),'max_kt':finite_extreme((r['speed_difference_kt'] for r in values),max),'max_record':max_record(values,'speed_difference_kt'),'valid_pair_count':sum(r['speed_difference_kt'] is not None for r in values)}
    commit_outputs(root, {'wind_records.csv':records,'wind_extrema.csv':extrema,
        'within_sensor_differences.csv':differences,'across_sensor_variability.csv':cross},
        {'wind_extraction.json':metadata,'summary.json':summary})
    return records,summary

if __name__=='__main__':
    records,summary=build()
    print(json.dumps(summary,indent=2))
