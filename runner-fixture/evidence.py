import glob, json, os, pathlib, re, sys, time
root = pathlib.Path(os.environ['RUNNER_TEMP'])
record = root / 'summary-evidence.json'
stop = root / 'summary-evidence-stop'
if sys.argv[1] == 'watch':
    found = {}
    while not stop.exists():
        for name in glob.glob(str(root / '_runner_file_commands' / 'step_summary_*')):
            try:
                text = pathlib.Path(name).read_text()
                if text.strip():
                    found[name] = text
            except OSError:
                pass
        record.write_text(json.dumps(list(found.values())))
        time.sleep(.05)
elif sys.argv[1] == 'inspect':
    for name in ['../lib/go/go.mod', 'runner-fixture/go/go.mod']:
        data = pathlib.Path(name).read_bytes()
        print(name, 'first-line=', repr(data.split(b'\n')[0]), 'CRLF=', b'\r\n' in data)
    print('generated root go.work exists=', pathlib.Path('../go.work').exists())
else:
    stop.touch()
    time.sleep(.2)
    texts = json.loads(record.read_text())
    body = '\n'.join(texts)
    print('CAPTURED JOB SUMMARIES\n' + body)
    assert '## Stackspace CI' in body, 'actual stack summary missing'
    assert os.environ['EXPECTED'] in body, 'checkout SHA missing from summary'
    assert not re.search(r'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]+|https?://[^\s/]+@', body), 'credential-shaped summary content'
    provenance = json.loads((root / 'stack-provenance.json').read_text())
    assert provenance['app']['commit'] == os.environ['EXPECTED']
    assert not re.search(r'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]+|https?://[^\s/]+@', json.dumps(provenance))
    if '_seed' in provenance:
        assert provenance['_seed']['reference'] == 'rigsmith/stack-examples@runner-test-seed'
        assert provenance['_seed']['commit'] in body
    print('Summary/provenance assertions passed')
