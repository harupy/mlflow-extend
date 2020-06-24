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

    const { repo, owner } = github.context.repo;
    console.log(repo);
    console.log(owner);

    const { data: pullRequest } = await octokit.pulls.get({
      owner,
      repo,
      pull_number: 112,
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
