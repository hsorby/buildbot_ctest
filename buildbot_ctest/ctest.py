
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

    def evaluateCommand(self, cmd):
        lo = BufferLogObserver()
        lines = lo.getStdout()
        re_test_results = re.compile("[0-9]+% tests passed, ([0-9]+) tests failed out of ([0-9]+)");

        passed_groups = map(lambda line: re_test_results.search(line), lines)
        failed = 0
        total = 0
        for passed_group in passed_groups:
            if passed_group:
                failed = int(passed_group.group(1))
                total = int(passed_group.group(2))

        self.setTestResults(failed=failed, total=total)

        if failed == 0 and total > 0:
            rc = results.SUCCESS
        else:
            rc = results.FAILURE

        return rc

    @defer.inlineCallbacks
    def run(self):
        command = self.command

        cmd = yield self.makeRemoteShellCommand(command=command)

        yield self.runCommand(cmd)

        defer.returnValue(cmd.results())
