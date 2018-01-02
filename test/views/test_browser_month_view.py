from timereporter.__main__ import main

def test_basic(mock_browser):
    main('9 16')
    main('yesterday 10 18')
    main('show december html --show-weekend')
    assert mock_browser.url.endswith('.html')
    with open(mock_browser.url) as f:
        s = f.read()
        assert '2016-12-01' in s
        assert '2016-12-31' in s

