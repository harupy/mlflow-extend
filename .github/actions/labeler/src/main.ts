import * as core from '@actions/core';
import * as github from '@actions/github';

export function sample(): string {
  return 'sample';
}

async function run(): Promise<void> {
  try {
    // const token: string = core.getInput('github-token');
    const token = core.getInput('repo-token', { required: true });
    const octokit = github.getOctokit(token);

    const { data: pullRequest } = await octokit.pulls.get({
      owner: 'octokit',
      repo: 'rest.js',
      pull_number: 123,
      mediaType: {
        format: 'diff',
      },
    });

    console.log(pullRequest);
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
