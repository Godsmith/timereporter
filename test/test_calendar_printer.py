from timereporter.calendar_printer import CalendarPrinter


class TestHighlightDifferenceInLine:
    def test_no_change(self):
        assert CalendarPrinter(None, None, None).highlight_difference_in_line(
            '00 00 00', '00 00 00') == '00 00 00'

    def test_entire_word_changed(self):
        assert CalendarPrinter(None, None, None).highlight_difference_in_line(
            '00 00 00', '00 xx 00') == '00 \x1b[1mxx\x1b[0m 00'

    def test_part_of_word_changed(self):
        assert CalendarPrinter(None, None, None).highlight_difference_in_line(
            '00 0000 00', '00 00xx 00') == '00 \x1b[1m00xx\x1b[0m 00'


class TestHighlightDifferenceInLines:
    def test_simple(self):
        assert CalendarPrinter(None, None, None).highlight_difference_in_lines(
            '0\n00\n0', '0\nXX\n0') == '0\n\x1b[1mXX\x1b[0m\n0'

    def test_one_line_is_longer(self):
        assert CalendarPrinter(None, None, None).highlight_difference_in_lines(
            '00\n\n00', '00\nxx\n00') == '00\n\x1b[1mxx\x1b[0m\n00'
