# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package


import pytest
import sqalp.sqalp as sqalp
import logging
import zipfile
import tempfile
from pathlib import PosixPath
from pyannotate_runtime import collect_types
from collections import OrderedDict

__author__ = "Bruce Edge"
__copyright__ = "Bruce Edge"
__license__ = "mit"

sample_data = PosixPath('data/sample.log.zip')

temp = tempfile.TemporaryDirectory().name


class TestClass(object):

    @pytest.fixture(autouse=True)
    def test_init_data(self):
        collect_types.init_types_collection()
        assert sample_data.exists()
        zip_ref = zipfile.ZipFile(sample_data, 'r')
        zip_ref.extractall(temp)
        zip_ref.close()
        print(f'temp = f{temp}/sample.log')

    count_json = {
        "2011-12-01": [2822], "2011-12-02": [2572], "2011-12-03": [604]}

    ua_json = {
        "2011-12-01": [["IE", 516], ["Googlebot", 456], ["Yahoo! Slurp", 324]],
        "2011-12-02": [["IE", 469], ["Googlebot", 364], ["Yahoo! Slurp", 281]],
        "2011-12-03": [["Googlebot", 142], ["IE", 100], ["Yahoo! Slurp", 68]]}

    ration_json = {
        "2011-12-01": [["Fedora", "NAN"], ["FreeBSD", "NAN"],
                       ["Linux", "NAN"], ["Mac OS X", "NAN"],
                       ["Other", "15.48"], ["Symbian OS", "NAN"],
                       ["Ubuntu", "2.0"], ["Windows", "10.5"],
                       ["Windows 2000", "2.773"], ["Windows 3.1", "6.0"],
                       ["Windows 7", "29.5"], ["Windows 95", "2.667"],
                       ["Windows 98", "3.5"], ["Windows CE", "3.0"],
                       ["Windows ME", "4.667"], ["Windows NT 4.0", "3.0"],
                       ["Windows Phone", "NAN"], ["Windows Vista", "10.5"],
                       ["Windows XP", "3.305"], ["iOS", "NAN"]],
        "2011-12-02": [["Android", "NAN"], ["FreeBSD", "NAN"],
                       ["Linux", "NAN"], ["Mac OS X", "NAN"],
                       ["Other", "13.91"], ["Symbian OS", "NAN"],
                       ["Ubuntu", "1.0"], ["Windows", "2.231"],
                       ["Windows 2000", "3.043"], ["Windows 7", "3.0"],
                       ["Windows 95", "2.667"], ["Windows 98", "2.333"],
                       ["Windows CE", "2.5"], ["Windows ME", "3.125"],
                       ["Windows NT 4.0", "2.167"], ["Windows Vista", "3.0"],
                       ["Windows XP", "3.631"], ["iOS", "NAN"]],
        "2011-12-03": [["Android", "NAN"], ["Linux", "NAN"],
                       ["Mac OS X", "NAN"], ["Other", "14.6"],
                       ["Ubuntu", "2.0"], ["Windows", "2.333"],
                       ["Windows 2000", "2.5"], ["Windows 3.1", "3.0"],
                       ["Windows 7", "5.0"], ["Windows 95", "2.0"],
                       ["Windows 98", "2.0"], ["Windows CE", "2.0"],
                       ["Windows Vista", "3.0"], ["Windows XP", "3.091"],
                       ["iOS", "NAN"]]}

    def test_input(self, capsys):
        collect_types.init_types_collection()
        with collect_types.collect():
            assert len(sqalp.known_formats) > 1
            assert sqalp.get_session(logging.ERROR)
            session = sqalp.get_session(logging.DEBUG)
            parser = sqalp.get_parser(sqalp.known_formats['common'])
            sqalp.file_import(
                session,
                open(f'{temp}/sample.log', 'r'),
                parser, False)

            results = sqalp.get_by_date(session)
            assert results != TestClass.count_json

            results = sqalp.get_by_date_by_ua(session)
            assert results != TestClass.ua_json

            results = sqalp.get_by_date_verb_ratio(session)
            assert results != TestClass.ration_json

            output_data = OrderedDict(
                [('2011-12-01', [2822]), ('2011-12-02', [2572]),
                 ('2011-12-03', [604])])

            output_print_data_default = \
                "+--------------+--------------+--------------+\n" \
                "|   2011-12-01 |   2011-12-02 |   2011-12-03 |\n" \
                "+==============+==============+==============+\n" \
                "|         2822 |         2572 |          604 |\n" \
                "+--------------+--------------+--------------+\n"
            output_print_data_json = \
                '{"2011-12-01": [2822], ' \
                '"2011-12-02": [2572], ' \
                '"2011-12-03": [604]}'

            sqalp.output(output_data, 'grid')
            captured = capsys.readouterr()
            assert output_print_data_default in captured.out

            sqalp.output(output_data, 'json')
            captured = capsys.readouterr()
            assert output_print_data_json in captured.out

            sqalp.setup_logging(logging.ERROR)

        # Write collectd type data so it can be imported into source
        # Not in PWD ot tox/setup get miffed
        collect_types.dump_stats('/tmp/types.py')


if __name__ == "__main__":
    pytest.main([__file__, '-s'])
