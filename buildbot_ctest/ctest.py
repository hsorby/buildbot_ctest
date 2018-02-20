import re

from twisted.internet import defer

from buildbot.process import results
from buildbot.process.buildstep import BuildStep
from buildbot.process.buildstep import ShellMixin
from buildbot.process.logobserver import BufferLogObserver

class CTest(ShellMixin, BuildStep):

    name = 'ctest'
    haltOnFailure = 1
    flunkOnFailure = 1
    description = ['running', 'ctest']
    descriptionDone = 'ctest'
    command = ['ctest', '-V']

    def __init__(self, **kwargs):
        super(CTest, self).__init__(**kwargs)
        test_results_parser = LineConsumerLogObserver(self.logConsumer)
        self.addLogObserver('stdio', test_results_parser)
        self._failed = None
        self._total = None

    def logConsumer(self):
        re_test_results = re.compile("[0-9]+% tests passed, ([0-9]+) tests failed out of ([0-9]+)");

        while True:
            stream, line = yield
            if stream == 'o':
                groups = re_test_results.search(line)
                if groups:
                    self._failed = int(groups.group(1))
                    self._total = int(groups.group(2))

    def getResultSummary(self):
        if self._total is not None:
            if self._failed == 0:
                summary = u'all (%s) tests passed' % (self._total)
            else:
                summary = u'%s test%s failed out of %s test%s' % (self._failed, 's' if self._failed > 1 else '', self._total, 's' if self._total > 1 else '')
        else:
            summary = u'no tests detected'

        s = {'step': summary}

        return s

    @defer.inlineCallbacks
    def run(self):
        command = self.command

        cmd = yield self.makeRemoteShellCommand(command=command)

        yield self.runCommand(cmd)

        rc = cmd.results()
        if rc == results.SUCCESS:
            if self._total is not None and self._failed == 0 and self._total > 0:
                rc = results.SUCCESS
            else:
                rc = results.FAILURE

        defer.returnValue(rc)
