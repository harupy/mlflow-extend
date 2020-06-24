import * as core from '@actions/core';
import * as github from '@actions/github';
import * as types from '@octokit/types';

type Label = {
  name: string;
  checked: boolean;
};

export function extractLabels(body: string): Label[] {
  function helper(regex: RegExp, labels: Label[] = []): Label[] {
    const res = regex.exec(body);
    if (res) {
      const checked = /[xX]/.test(res[1].trim());
      const name = res[2].trim();
      return helper(regex, [...labels, { name, checked }]);
    }
    return labels;
  }
  return helper(/- \[([ xX]*)\] ?`(.+)`/gm);
}

async function run(): Promise<void> {
  try {
    const token = core.getInput('repo-token', { required: true });
    const octokit = github.getOctokit(token);

    const { repo, owner } = github.context.repo;
    const { number: issue_number } = github.context.issue;

    const options = octokit.pulls.list.endpoint.merge({
      owner,
      repo,
    });

    for await (const page of octokit.paginate.iterator(options)) {
      for (const pull of page.data) {
        // Labels attached on the PR
        const labelsOnIssueResp = await octokit.issues.listLabelsOnIssue({
          owner,
          repo,
          issue_number,
        });
        const labelsOnIssue = labelsOnIssueResp.data.map(({ name }) => name);

        // Labels registered in the repository
        const labelsForRepoResp = await octokit.issues.listLabelsForRepo({
          owner,
          repo,
        });
        const labelsForRepo = labelsForRepoResp.data.map(({ name }) => name);

        // Labels in the PR description
        const { body } = pull as types.PullsGetResponseData;
        const labels = extractLabels(body).filter(({ name }) =>
          labelsForRepo.includes(name),
        );

        // Remove unchecked labels
        const labelsToRemove = labels.filter(
          ({ name, checked }) => !checked && labelsOnIssue.includes(name),
        );
        labelsToRemove.forEach(async ({ name }) => {
          await octokit.issues.removeLabel({
            owner,
            repo,
            issue_number,
            name,
          });
        });

        // Add checked labels
        const labelsToAdd = labels
          .filter(
            ({ name, checked }) => checked && !labelsOnIssue.includes(name),
          )
          .map(({ name }) => name);

        if (labelsToAdd.length > 0) {
          await octokit.issues.addLabels({
            owner,
            repo,
            issue_number,
            labels: labelsToAdd,
          });
        }

        console.log(`issue_number: ${issue_number}`);
      }
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
