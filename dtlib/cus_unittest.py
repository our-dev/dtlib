#!coding=utf8
"""
Customer Unitest自定义的test Runner 和result类,用来将结果和报告服务器打通,自动生成报表
"""
import unittest
import time
import sys

from dtlib import jsontool

__author__ = 'zheng'


def load_tests_from_cls(test_case_cls):
    """
    从类中加载所有的测试用例
    :param test_case_cls:
    :return:
    """
    return unittest.TestLoader().loadTestsFromTestCase(test_case_cls)


class CusTestRunner(object):
    """
    Customer Test Runner
    """

    def __init__(self, stream=sys.stderr, verbosity=0):
        self.stream = stream
        self.verbosity = verbosity

    def writeUpdate(self, message):
        self.stream.write(message)

    def run(self, test):
        "Run the given test case or test suite."
        result = CusTestResult(self)

        startTime = time.time()

        self.writeUpdate("<TestRun>\n")
        self.writeUpdate("\n<!-- Individual results -->\n")

        test.run(result)

        stopTime = time.time()
        timeTaken = float(stopTime - startTime)
        self.writeUpdate("\n<!-- run time:%s(s) -->\n" % timeTaken)
        self.writeUpdate("\n<!-- Error/Failure details -->\n")
        self.writeUpdate("\n<!-- total run %s tests -->\n" % result.testsRun)

        result.printErrors()
        self.writeUpdate("</TestRun>\n")
        return result


class CusTestResult(unittest.TestResult):
    """A test result class that can print

    CustomTestRunner.edit the TextTestResult,can edit the verbose
    """

    def __init__(self, runner):
        unittest.TestResult.__init__(self)
        self.runner = runner
        self.success_cnt = 0  # 成功量统计
        self.showAll = runner.verbosity > 1
        self.dots = runner.verbosity == 1

    def startTest(self, test):
        unittest.TestResult.startTest(self, test)
        # we should escape quotes here
        self.runner.writeUpdate('<TestCase name="%s-%s" ' % (test._testMethodName,
                                                             test.shortDescription()))

    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        self.runner.writeUpdate('result="ok" />\n')

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        self.runner.writeUpdate('result="error" />\n')

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        self.runner.writeUpdate('result="fail" />\n')

    def printErrors(self):
        self.printErrorList('Error', self.errors)
        self.printErrorList('Failure', self.failures)

    def printErrorList(self, flavor, errors):
        for test, err in errors:
            self.runner.writeUpdate('<%s testcase="%s-%s">\n' %
                                    (flavor, test._testMethodName, test.shortDescription()))
            self.runner.writeUpdate('<' + '![CDATA[')
            self.runner.writeUpdate("%s" % err)
            self.runner.writeUpdate(']]' + '>')
            self.runner.writeUpdate("</%s>\n" % flavor)
