import * as core from '@actions/core';
import * as github from '@actions/github';
import * as types from '@octokit/types';

type Label = {
  name: string;
  checked: boolean;
};

export function extractLabels(body: string, labelPattern: string): Label[] {
  function helper(regex: RegExp, labels: Label[] = []): Label[] {
    const res = regex.exec(body);
    if (res) {
      const checked = /[xX]/.test(res[1].trim());
      const name = res[2].trim();
      return helper(regex, [...labels, { name, checked }]);
    }
    return labels;
  }
  return helper(new RegExp(labelPattern, 'gm'));
}

async function main(): Promise<void> {
  try {
    const token = core.getInput('repo-token', { required: true });
    const labelPattern = core.getInput('label-pattern', { required: true });

    const octokit = github.getOctokit(token);
    const { repo, owner } = github.context.repo;

    // Iterate over all the open PRs
    for await (const page of octokit.paginate.iterator(
      octokit.issues.listForRepo,
      { owner, repo },
    )) {
      for (const issue of page.data) {
        const {
          body,
          number: issue_number,
          html_url,
        } = issue as types.IssuesGetResponseData;

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
        const labels = extractLabels(body, labelPattern).filter(({ name }) =>
          // Remove labels that are not registered in the repo.
          labelsForRepo.includes(name),
        );

        // Remove unchecked labels
        const labelsToRemove = labels.filter(
          ({ name, checked }) => !checked && labelsOnIssue.includes(name),
        );

        if (labelsToRemove.length > 0) {
          labelsToRemove.forEach(async ({ name }) => {
            await octokit.issues.removeLabel({
              owner,
              repo,
              issue_number,
              name,
            });
          });
        }

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

        if (labelsToRemove.length > 0 || labelsToAdd.length > 0) {
          console.log(`Updated: ${html_url}`);
        }
      }
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

main();
