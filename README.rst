sqalp
=====


Apache Log Parser


Description
===========

Command line tool that parses the apache logs log and presents the following (somewhat contrived) info to the user:

- Number of requests served by day
- 3 most frequent User Agents by day
- ratio of GET's to POST's by OS by day

Rationale: Excuse to play with SqlAlchemy and pypi packaging.


Installation
============

Stable:

.. code-block::

    pip install sqalp

Latest:

.. code-block::

    pip install git@github.com:bedge/sqalp.git

Create `sqalp` executable.


Documentation
=============

Help:

.. code-block::

    usage: sqalp [-h] [--version] [-i [INPUT]] -f {common,combined} [-c] [-u] [-r]
               [-O] [-F FLOAT_FORMAT] [-s] [-o OUTPUT_FORMAT] [-v] [-vv]

    Log file parser

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -i [INPUT], --input [INPUT]
                            Files to input, default to stdin
      -f {common,combined}, --format {common,combined}
                            Input formatsee:
                            https://httpd.apache.org/docs/1.3/logs.html#accesslog
      -c, --count           Requests per day
      -u, --ua_frequency    User-agent stats by day
      -r, --ratio           Ratio of GET to POST by day by OS
      -O, --os_approximate  Approximate OS to family grouping (Win XP == Win, etc)
      -o OUTPUT_FORMAT, --output_format OUTPUT_FORMAT
                            table/output formats, one of ['fancy_grid', 'grid',
                            'html', 'jira', 'latex', 'latex_booktabs',
                            'latex_raw', 'mediawiki', 'moinmoin', 'orgtbl',
                            'pipe', 'plain', 'presto', 'psql', 'rst', 'simple',
                            'textile', 'tsv', 'youtrack', 'json']
      -v, --verbose         set loglevel to INFO
      -vv, --very-verbose   set loglevel to DEBUG


- Input

  default to stdin for commandline filter in the unix pipe philosophy

- Output

  Supports all formats provided by tabulate package, and, json for piping to other scripts


Main commands
=============

These are samples of easily added functionality

- count

  Count by day the number of requests

.. code-block::

    %> sqalp -i data/sample.log -f combined -c
    +--------------+--------------+--------------+
    |   2011-12-01 |   2011-12-02 |   2011-12-03 |
    +==============+==============+==============+
    |         2822 |         2572 |          604 |
    +--------------+--------------+--------------+

    %> sqalp -i data/sample.log -f combined -o fancy_grid  -c
    ╒══════════════╤══════════════╤══════════════╕
    │   2011-12-01 │   2011-12-02 │   2011-12-03 │
    ╞══════════════╪══════════════╪══════════════╡
    │         2822 │         2572 │          604 │
    ╘══════════════╧══════════════╧══════════════╛

    %> bin/sqalp -i data/sample.log -f combined -o json  -c
    {"2011-12-01": [2822], "2011-12-02": [2572], "2011-12-03": [604]}



- user-agent frequency

  Show 3 most frequent user-agents by day

.. code-block::

    %> sqalp -i data/sample.log -f combined -o fancy_grid  -u
    ╒═══════════════════════╤═══════════════════════╤══════════════════════╕
    │ 2011-12-01            │ 2011-12-02            │ 2011-12-03           │
    ╞═══════════════════════╪═══════════════════════╪══════════════════════╡
    │ ['IE', 516]           │ ['IE', 469]           │ ['Googlebot', 142]   │
    ├───────────────────────┼───────────────────────┼──────────────────────┤
    │ ['Googlebot', 456]    │ ['Googlebot', 364]    │ ['IE', 100]          │
    ├───────────────────────┼───────────────────────┼──────────────────────┤
    │ ['Yahoo! Slurp', 324] │ ['Yahoo! Slurp', 281] │ ['Yahoo! Slurp', 68] │
    ╘═══════════════════════╧═══════════════════════╧══════════════════════╛


    %> bin/sqalp -i data/sample.log -f combined -o html  -u
    <table>
    <thead>
    <tr><th>2011-12-01           </th><th>2011-12-02           </th><th>2011-12-03          </th></tr>
    </thead>
    <tbody>
    <tr><td>['IE', 516]          </td><td>['IE', 469]          </td><td>['Googlebot', 142]  </td></tr>
    <tr><td>['Googlebot', 456]   </td><td>['Googlebot', 364]   </td><td>['IE', 100]         </td></tr>
    <tr><td>['Yahoo! Slurp', 324]</td><td>['Yahoo! Slurp', 281]</td><td>['Yahoo! Slurp', 68]</td></tr>
    </tbody>
    </table>


- ratio of GET/PUT by OS

Optional -O flag for OS aggregation to reduce number of OS variants.

ie: count all Win XX = Win.

.. code-block::

    %> sqalp -i data/sample.log -f combined -o plain  -r
    2011-12-01                 2011-12-02                   2011-12-03
    ['Fedora', inf]            ['Android', inf]             ['Android', inf]
    ['FreeBSD', inf]           ['FreeBSD', inf]             ['Linux', inf]
    ['Linux', inf]             ['Linux', inf]               ['Mac OS X', inf]
    ['Mac OS X', inf]          ['Mac OS X', inf]            ['Other', '14.6']
    ['Other', '15.48']         ['Other', '13.91']           ['Ubuntu', '2.0']
    ['Symbian OS', inf]        ['Symbian OS', inf]          ['Windows', '2.333']
    ['Ubuntu', '2.0']          ['Ubuntu', '1.0']            ['Windows 2000', '2.5']
    ['Windows', '10.5']        ['Windows', '2.231']         ['Windows 3.1', '3.0']
    ['Windows 2000', '2.773']  ['Windows 2000', '3.043']    ['Windows 7', '5.0']
    ['Windows 3.1', '6.0']     ['Windows 7', '3.0']         ['Windows 95', '2.0']
    ['Windows 7', '29.5']      ['Windows 95', '2.667']      ['Windows 98', '2.0']
    ['Windows 95', '2.667']    ['Windows 98', '2.333']      ['Windows CE', '2.0']
    ['Windows 98', '3.5']      ['Windows CE', '2.5']        ['Windows Vista', '3.0']
    ['Windows CE', '3.0']      ['Windows ME', '3.125']      ['Windows XP', '3.091']
    ['Windows ME', '4.667']    ['Windows NT 4.0', '2.167']  ['iOS', inf]
    ['Windows NT 4.0', '3.0']  ['Windows Vista', '3.0']
    ['Windows Phone', inf]     ['Windows XP', '3.631']
    ['Windows Vista', '10.5']  ['iOS', inf]
    ['Windows XP', '3.305']
    ['iOS', inf]


    %> sqalp -i data/sample.log -f combined -o fancy_grid -O -r
    ╒══════════════════════╤══════════════════════╤══════════════════════╕
    │ 2011-12-01           │ 2011-12-02           │ 2011-12-03           │
    ╞══════════════════════╪══════════════════════╪══════════════════════╡
    │ ['Fedora', inf]      │ ['Android', inf]     │ ['Android', inf]     │
    ├──────────────────────┼──────────────────────┼──────────────────────┤
    │ ['FreeBSD', inf]     │ ['FreeBSD', inf]     │ ['Linux', inf]       │
    ├──────────────────────┼──────────────────────┼──────────────────────┤
    │ ['Linux', inf]       │ ['Linux', inf]       │ ['Mac', inf]         │
    ├──────────────────────┼──────────────────────┼──────────────────────┤
    │ ['Mac', inf]         │ ['Mac', inf]         │ ['Other', '14.6']    │
    ├──────────────────────┼──────────────────────┼──────────────────────┤
    │ ['Other', '15.48']   │ ['Other', '13.91']   │ ['Ubuntu', '2.0']    │
    ├──────────────────────┼──────────────────────┼──────────────────────┤
    │ ['Symbian', inf]     │ ['Symbian', inf]     │ ['Windows', '3.025'] │
    ├──────────────────────┼──────────────────────┼──────────────────────┤
    │ ['Ubuntu', '2.0']    │ ['Ubuntu', '1.0']    │ ['iOS', inf]         │
    ├──────────────────────┼──────────────────────┼──────────────────────┤
    │ ['Windows', '3.904'] │ ['Windows', '3.269'] │                      │
    ├──────────────────────┼──────────────────────┼──────────────────────┤
    │ ['iOS', inf]         │ ['iOS', inf]         │                      │
    ╘══════════════════════╧══════════════════════╧══════════════════════╛


Functional Notes
================

- User Agent definition

  Use 'browser family', good balance between overly specific/general.
  it could have been the full browser string, or even the full UA string itself,
  but that becomes less meaningful as there are then so many unique UAs.

- Operating system detection

  Use 'OS family prefix', IOW combine Win XX into Win, otherwise ratio has little data.

  "--os_approximate" option collapses OS's into fewer families.

Implementation Notes
====================

- python 3.6 required

  f-strings & type annotations !!

- SqlAlchemy

  Overkill for this specific need, but for the case of many GB's of log data this provides a more useful framework.
  If a non-sqlite backend is used, much of the sorting is done server-side.

  Currently uses 'sqlite:///:memory:', but could be easily changed to using any
  supported SQL-ish back-end

  Allows multiple instances to write to same back-end to aggregate data from many sources.
  (Although, may need to bounce the session transaction a bit more frequently for that case)

- pyannotate

  Generate type data to apply to source for static type checking.

  Use `pyannotate -w --type-info types.py sqsqalp/sqsqalp.py` to apply type info generated in pytest

- apache-log-parser

  https://github.com/rory/apache-log-parser

  Uses this instead of regex based parsing. No need to duplicate the effort, although I basically had by the time I realized that this existed. My WIP left in source in case this needs to diverge.

- tox test config

- Logging

  Logs to stderr with -v option, so does not impact pipe commands and is still visible.

.. code-block::

    %> sqsqalp -i data/sample.log -f combined -o json  -u -v   | json_pp
    [2018-03-18 16:53:52] INFO:sqsqalp:Parse failed: 'Foo' for log message: 127.0.0.1 - - [01/Foo/2011:06:31:44 -0500] "GET /post/at-the-apple-store-trying-out HTTP/1.0" 301 339 "-" "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
    .
    [2018-03-18 16:53:55] INFO:sqsqalp:Parse failed: invalid literal for int() with base 10: '011:' for log message: 127.0.0.1 - - [03/De/2011:04:52:18 -0500] "GET /wp-content/themes/carrington-text/carrington-core/lightbox/css/thickbox.css HTTP/1.0" 304 173 "http://aviflax.com/post/some-good-news-this-morning/" "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)"
    .
    [2018-03-18 16:53:56] INFO:sqsqalp:Unparseable message count: 2.
    {
       "2011-12-03" : [
          [
             "Googlebot",
             142
          ],
          [
             "IE",
             100
          ],
          [
             "Yahoo! Slurp",
             68
          ]
       ],
       "2011-12-01" : [
          [
             "IE",
             516
          ],
          [
             "Googlebot",
             456
          ],
          [
             "Yahoo! Slurp",
             324
          ]
       ],
       "2011-12-02" : [
          [
             "IE",
             469
          ],
          [
             "Googlebot",
             364
          ],
          [
             "Yahoo! Slurp",
             281
          ]
       ]
    }

Releases
========

Release process

.. code-block::

    bumpversion -v --feature
    python setup.py bdist_wheel
    twine upload -r pypitest dist/sqalp-<version>-py3-none-any.whl
    twine upload -r pypi dist/sqalp-<version>-py3-none-any.whl


Improvements
============

- Use hierarchical regex parsers to zero in on the specific aspect of a log message that failed to parse.

  ie: bad date, illegal IP addr, invalid http verb, etc.

- Change json output format

  Provide element names rather than raw, unlabelled data.

- Support different persistence implementations. Currently uses sqlite:///:memory.

  Using 'real' backend DB allows:

  - Multiple instances to write data into a common DB.

- Break up 'ingest data' option from 'reporting' options.
