"""Check the rendered grayscale deliverables without changing source imagery."""
from pathlib import Path
import base64
import hashlib
import io
import json
import re
import xml.etree.ElementTree as ET

import numpy as np
import pymupdf
from PIL import Image, ImageColor

P = Path(__file__).resolve().parents[1]


def neutral_pixels(image, context, tolerance=0):
    rgb = np.asarray(image.convert('RGB'), dtype=np.int16)
    spread = rgb.max(axis=2) - rgb.min(axis=2)
    maximum = int(spread.max())
    if maximum > tolerance:
        raise ValueError(f'{context}: non-gray pixels, maximum RGB spread {maximum}')
    return maximum


def main():
    # Test the encoded neutral colours, not a viewer's device-profile transform.
    # MuPDF's default ICC conversion can tint a neutral DeviceGray edge by 2/255.
    pymupdf.TOOLS.set_icc(False)
    records = json.loads((P / 'qa/figure_provenance.json').read_text())
    if len(records) != 15 or len({r['figure'] for r in records}) != 15:
        raise ValueError('Expected all 15 V5 figure masters')
    verified = []
    for record in records:
        stem = record['figure']
        if record.get('color_mode') != 'grayscale':
            raise ValueError(f'{stem}: missing grayscale provenance')
        for relative in [f'figures/{stem}.png', f'presentation/{stem}.png']:
            with Image.open(P / relative) as image:
                neutral_pixels(image, relative)
            verified.append(relative)
        relative = f'figures/{stem}.pdf'
        with pymupdf.open(P / relative) as pdf:
            if len(pdf) != 1 or not pdf[0].get_text().strip():
                raise ValueError(f'{relative}: vector labels missing')
            expected = np.asarray(record['master_inches']) * 72
            if not np.allclose([pdf[0].rect.width, pdf[0].rect.height], expected, atol=.01):
                raise ValueError(f'{relative}: figure canvas changed')
            pix = pdf[0].get_pixmap(matrix=pymupdf.Matrix(2, 2), colorspace=pymupdf.csRGB, alpha=False)
            neutral_pixels(Image.frombytes('RGB', [pix.width, pix.height], pix.samples), relative)
        verified.append(relative)
        relative = f'figures/{stem}.svg'
        tree = ET.parse(P / relative)
        for node in tree.iter():
            paints = [node.attrib.get(name, '') for name in ['fill', 'stroke', 'color']]
            paints += re.findall(r'(?:^|;)\s*(?:fill|stroke|color)\s*:\s*([^;]+)', node.attrib.get('style', ''))
            for paint in paints:
                if paint in ['', 'none', 'currentColor'] or paint.startswith('url('):
                    continue
                rgb = ImageColor.getrgb(paint)[:3]
                if len(set(rgb)) != 1:
                    raise ValueError(f'{relative}: colored vector paint {paint}')
            if node.tag.endswith('}image'):
                href = node.attrib.get('{http://www.w3.org/1999/xlink}href', node.attrib.get('href', ''))
                if not href.startswith('data:image/') or ';base64,' not in href:
                    raise ValueError(f'{relative}: image is not self-contained')
                with Image.open(io.BytesIO(base64.b64decode(href.split(',', 1)[1]))) as image:
                    neutral_pixels(image, relative + ':embedded image')
        verified.append(relative)
    receipt = {
        'status': 'passed', 'figure_count': len(records), 'exports_checked': len(verified),
        'checks': ['PNG RGB channels exactly equal', 'PDF rendered RGB channels exactly equal with viewer ICC conversion disabled',
                   'SVG vector paints and embedded rasters neutral', 'vector text and original canvas retained'],
        'files': [{'path': path, 'sha256': hashlib.sha256((P / path).read_bytes()).hexdigest()} for path in verified],
    }
    (P / 'qa/grayscale_exports.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Grayscale verified: {len(records)} figures, {len(verified)} exports.')


if __name__ == '__main__':
    main()
