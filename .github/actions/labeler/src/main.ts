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

    const options = octokit.pulls.list.endpoint.merge({
      owner: github.context.repo.owner,
      repo: github.context.repo.repo,
    });

    for await (const pageResponse of octokit.paginate.iterator(options)) {
      for (const pullResponse of pageResponse.data) {
        console.log(pullResponse);
      }
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
