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
      const checked = res[1].trim().toLocaleLowerCase() === 'x';
      const name = res[2].trim();
      return helper(regex, [...labels, { name, checked }]);
    }
    return labels;
  }
  return helper(new RegExp(labelPattern, 'gm'));
}

export function getName({ name }: { name: string }): string {
  return name;
}

export function getChecked({ checked }: { checked: boolean }): boolean {
  return checked;
}

export function logAsList(strArray: string[]): void {
  console.log(
    strArray.map(s => `- ${s}`).join('\n') + (strArray.length > 0 ? '\n' : ''),
  );
}

export function validateEnums<T>(key: T, val: T, enums: T[]): never | void {
  if (!enums.includes(val)) {
    const wrap = (s: T): string => `"${s}"`;
    const joined = enums.map(wrap).join(', ');
    throw new Error(
      `\`${key}\` must be one of [${joined}], but got ${wrap(val)}`,
    );
  }
}

async function main(): Promise<void> {
  try {
    const token = core.getInput('repo-token', { required: true });
    const labelPattern = core.getInput('label-pattern', { required: true });
    const q = core.getInput('quiet', { required: true });

    validateEnums('quiet', q, ['true', 'false']);
    const quiet = q === 'true';

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

        if (!quiet) {
          console.log(`<<< ${html_url} >>>`);
        }

        // Labels attached on the PR
        const labelsOnIssueResp = await octokit.issues.listLabelsOnIssue({
          owner,
          repo,
          issue_number,
        });
        const labelsOnIssue = labelsOnIssueResp.data.map(getName);

        // Labels registered in the repository
        const labelsForRepoResp = await octokit.issues.listLabelsForRepo({
          owner,
          repo,
        });
        const labelsForRepo = labelsForRepoResp.data.map(getName);

        // Labels in the PR description
        const labels = extractLabels(body, labelPattern).filter(({ name }) =>
          // Remove labels that are not registered in the repo.
          labelsForRepo.includes(name),
        );

        if (!quiet) {
          console.log('Checked labels:');
          logAsList(labels.filter(getChecked).map(getName));
        }

        // Remove unchecked labels
        const labelsToRemove = labels
          .filter(
            ({ name, checked }) => !checked && labelsOnIssue.includes(name),
          )
          .map(getName);

        if (!quiet) {
          console.log('Labels to remove:');
          logAsList(labelsToRemove);
        }

        if (labelsToRemove.length > 0) {
          labelsToRemove.forEach(async name => {
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
          .map(getName);

        if (!quiet) {
          console.log('Labels to add:');
          logAsList(labelsToAdd);
        }

        if (labelsToAdd.length > 0) {
          await octokit.issues.addLabels({
            owner,
            repo,
            issue_number,
            labels: labelsToAdd,
          });
        }
      }
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

main();
