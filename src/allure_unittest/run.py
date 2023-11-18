import shutil
from multiprocessing import Pool, cpu_count
from pathlib import Path
from unittest import TestSuite

from .result import Result


class Run:

    def __init__(self, report_source_path, *suites: TestSuite, clean=False):
        self.report_source_path = Path(report_source_path).absolute()
        if self.report_source_path.is_dir() and clean:
            shutil.rmtree(self.report_source_path)
        self.suites = self._get_async_suites(suites)
        self._start()

    @staticmethod
    def _get_async_suites(suites):
        cases = {}
        for s in suites:
            for c in getattr(s, '_tests'):
                if hasattr(c, 'sync'):
                    cases.setdefault(c.sync, []).append(c)
                    continue
                cases.setdefault('async', []).append(c)
        return cases

    def _start(self):
        pool = Pool(processes=cpu_count() - 2)
        for sync, case_list in self.suites.items():
            if sync == 'async':
                pool.starmap(self._execute_case, [(c, self.report_source_path) for c in case_list])
            else:
                pool.apply(self._execute_case_list, (case_list, self.report_source_path))

        pool.close()
        pool.join()

    @staticmethod
    def _execute_case_list(case_list, report_source_path):
        for case in case_list:
            Run._execute_case(case, report_source_path)

    @staticmethod
    def _execute_case(case, report_source_path):
        r = Result(report_source_path)
        case.run(r)
