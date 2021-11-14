module.exports = {
  extends: ['@commitlint/configconventional'],
  rules: {
    'type-enum': [2, 'always', ['build', 'chore', 'ci', 'docs', 'feat', 'fix', 'perf', 'refactor', 'revert', 'style', 'test']],
    'subject-full-stop': [0, 'never'],
    'subjectcase': [0, 'never']
  }
}
