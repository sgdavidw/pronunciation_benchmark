"""
Convert YouTube subtitles(vtt) to human readable text.

Download only subtitles from YouTube with youtube-dl:
youtube-dl  --skip-download --convert-subs vtt <video_url>

Note that default subtitle format provided by YouTube is ass, which is hard
to process with simple regex. Luckily youtube-dl can convert ass to vtt, which
is easier to process.

To conver all vtt files inside a directory:
find . -name "*.vtt" -exec python vtt2text.py {} \;
"""

import sys
import re
import os
import subprocess


def remove_newline(text):
    """
    Remove newline
    """
    text = re.sub(r'\n', ' ', text, flags=re.MULTILINE)
    return text


def remove_zoom_tags(text):
    """
    Remove vtt markup tags
    """
    text = re.sub(r'David Wang:\s', '', text)

    # extract timestamp, only kep HH:MM
    text = re.sub(
        r'\d{2}:\d{2}:\d{2}\.\d{3}\s-->\s.*',
        '',
        text
    )
    text = re.sub(r'^\d+$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s+$', '', text, flags=re.MULTILINE)
    return text


def remove_tags(text):
    """
    Remove vtt markup tags
    """
    tags = [
        r'</c>',
        r'<c(\.color\w+)?>',
        r'<\d{2}:\d{2}:\d{2}\.\d{3}>',

    ]

    for pat in tags:
        text = re.sub(pat, '', text)

    # extract timestamp, only kep HH:MM
    text = re.sub(
        r'(\d{2}:\d{2}):\d{2}\.\d{3} --> .* align:start position:0%',
        r'\g<1>',
        text
    )

    text = re.sub(r'^\s+$', '', text, flags=re.MULTILINE)
    return text


def remove_header(lines):
    """
    Remove vtt file header
    """
    pos = -1
    for mark in ('##', 'Language: en',):
        if mark in lines:
            pos = lines.index(mark)
    lines = lines[pos+1:]
    return lines


def merge_duplicates(lines):
    """
    Remove duplicated subtitles. Duplicates are always adjacent.
    """
    last_timestamp = ''
    last_cap = ''
    for line in lines:
        if line == "":
            continue
        if re.match('^\d{2}:\d{2}$', line):
            if line != last_timestamp:
                yield line
                last_timestamp = line
        else:
            if line != last_cap:
                yield line
                last_cap = line


def merge_short_lines(lines):
    buffer = ''
    for line in lines:
        if line == "" or re.match('^\d{2}:\d{2}$', line):
            yield '\n' + line
            continue

        if len(line+buffer) < 80:
            buffer += ' ' + line
        else:
            yield buffer.strip()
            buffer = line
    yield buffer


def main():

    ref_file = sys.argv[1]
    ref_file_path, ref_file_name = os.path.split(ref_file)
    ref_txt_file = "./files/" + re.sub(r'.org$', '.txt', ref_file_name)
    with open(ref_file) as f:
        text = f.read()
    # remove_newline(text)
    lines = text.splitlines()
    with open(ref_txt_file, 'w') as f:
        for line in lines:
            line = re.sub(r'\n', ' ', line)
            f.write(line)
            # f.write("\n")
            f.write(' ')
        # f.write(text)
    vtt_file = sys.argv[2]
    vtt_file_path, vtt_file_name = os.path.split(vtt_file)
    hyp_txt_file = "./files/hyp_" + re.sub(r'.vtt$', '.txt', vtt_file_name)
    with open(vtt_file) as f:
        text = f.read()

    text = remove_zoom_tags(text)

    #text = remove_tags(text)
    lines = text.splitlines()
    #lines = remove_header(lines)

    lines = merge_duplicates(lines)
    lines = list(lines)
    lines = merge_short_lines(lines)
    lines = list(lines)

    with open(hyp_txt_file, 'w') as f:
        for line in lines:
            line = re.sub(r'\n', ' ', line)
            f.write(line)
            # f.write("\n")
            f.write(' ')
    print('wer -i -a {} {}'.format(ref_txt_file, hyp_txt_file))
    subprocess.run(["wer", "-i", "-a", ref_txt_file, hyp_txt_file])


if __name__ == "__main__":
    main()
